#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
给 Obsidian Flashcards 生成的法语卡批量添加发音。

设计要点
--------
1. 只在 Obsidian-basic 模型里新增一个 Audio 字段，发音写成 [sound:xxx.mp3]。
   Flashcards 插件同步时只读写 Front/Back/Context/Source 四个字段，
   不会碰 Audio，所以不会覆盖发音。
2. 卡片背面的 Back 模板会插入 {{Audio}} 播放器（只在有音频时显示）。
3. 文本优先从 Back 的 <code> 片段提取；如果只有词尾/词干这类片段，
   再退回到 Back 的纯文本；仍然没有就从 Front 提取。
4. 音频文件名 = fr_ + sha1(文本)[:12].mp3，文本变了文件名就变，便于增量重跑。
5. 默认只做 dry-run；必须显式加 --apply 才会修改 Anki。

运行方式（必须用 edge-tts >= 7.3.0，系统自带的 7.2.7 会被微软接口拒绝）：
    uv run --with edge-tts==7.3.1 python add_audio.py --dry-run
    uv run --with edge-tts==7.3.1 python add_audio.py --apply
"""

from __future__ import annotations

import argparse
import asyncio
import base64
import hashlib
import html
import json
import logging
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
ANKI_URL = "http://127.0.0.1:8765"
DEFAULT_DECK_ROOT = "法语"
DEFAULT_MODEL = "Obsidian-basic"
DEFAULT_FIELD = "Audio"
DEFAULT_VOICE = "fr-FR-DeniseNeural"
DEFAULT_RATE = "-10%"

TEMPLATE_MARKER = "<!-- anki-audio -->"
TEMPLATE_SNIPPET = '{{#Audio}}<div class="fc-audio">{{Audio}}</div>{{/Audio}}' + TEMPLATE_MARKER

CJK_RE = re.compile(r"[一-鿿㐀-䶿　-〿＀-￯]+")
LATIN_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ]")
VOWEL_RE = re.compile(r"[aeiouyàâäéèêëîïôöùûüÿœæ]", re.I)
CODE_RE = re.compile(r"<code[^>]*>(.*?)</code>", re.S | re.I)
TAG_RE = re.compile(r"<[^>]+>")

LOG = logging.getLogger("anki_audio")


# ---------------------------------------------------------------------------
# AnkiConnect
# ---------------------------------------------------------------------------
def anki(action: str, **params):
    payload = json.dumps({"action": action, "version": 6, "params": params}).encode("utf-8")
    req = urllib.request.Request(
        ANKI_URL, data=payload, headers={"Content-Type": "application/json"}
    )
    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            data = json.load(resp)
    except urllib.error.URLError as exc:
        raise RuntimeError(
            f"无法连接 AnkiConnect（{ANKI_URL}）。请先打开 Anki，并确认 AnkiConnect 已启用。"
        ) from exc
    if data.get("error"):
        raise RuntimeError(f"AnkiConnect {action} 失败：{data['error']}")
    return data.get("result")


# ---------------------------------------------------------------------------
# 文本处理
# ---------------------------------------------------------------------------
def html_to_text(value: str) -> str:
    value = html.unescape(value or "")
    value = TAG_RE.sub(" ", value)
    value = value.replace(" ", " ")
    return re.sub(r"\s+", " ", value).strip()


def normalize_segment(raw: str) -> str:
    """把 HTML 片段清理成适合 TTS 的法语文本。"""
    s = html.unescape(raw or "")
    s = TAG_RE.sub(" ", s)
    s = s.replace(" ", " ")
    s = s.replace("…", "...").replace("→", ", ").replace("–", "-").replace("—", "-")
    # marié(e) -> mariée；veuf (veuve) -> veuf, veuve
    s = re.sub(r"\(e\)", "e", s, flags=re.I)
    s = re.sub(r"\(([^)]+)\)", r", \1", s)
    # il/elle -> il, elle
    s = re.sub(r"\s*/\s*", ", ", s)
    # 去掉中文和中文标点
    s = CJK_RE.sub(" ", s)
    # 去掉 ⚠、箭头、加号、emoji 等非文字符号
    s = re.sub(r"[^\w\s.,;:!?'’()\-–—]", " ", s, flags=re.UNICODE)
    # "Il faut +" -> "Il faut"
    s = re.sub(r"\s*\+\s*$", "", s)
    s = re.sub(r"\s+([,.;:!?])", r"\1", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def is_useful(s: str) -> bool:
    """过滤词尾、词干、单字母、纯标点之类的片段。"""
    if not s:
        return False
    if s.startswith("-") or s.endswith("-") or s.endswith("'"):
        return False
    core = s.strip(" \t\r\n,.;:!?+")
    if len(core) < 2:
        return False
    if not LATIN_RE.search(core):
        return False
    if not VOWEL_RE.search(core):
        return False
    return True


def finalize_segment(s: str) -> str:
    s = s.strip(" \t\r\n,.;:!?+")
    return re.sub(r"\s+", " ", s).strip()


def code_segments(value: str) -> list[str]:
    out: list[str] = []
    for raw in CODE_RE.findall(value or ""):
        s = normalize_segment(raw)
        if is_useful(s):
            out.append(finalize_segment(s))
    return out


def plain_chunks(value: str) -> list[str]:
    """从纯文本里抽取法语片段；用于没有 <code> 或只有词尾的卡片。"""
    text = html_to_text(value)
    out: list[str] = []
    for part in CJK_RE.split(text):
        p = " " + part.strip() + " "
        # 去掉 -e / -ent / -iss- / -x 这类独立词尾
        p = re.sub(r"(?<=\s)-[A-Za-zÀ-ÿ]{1,8}(?=[\s,\-]|$)", " ", p)
        p = re.sub(r"(?<=\s)-+(?=\s|$)", " ", p)
        # 去掉 peu- / pouv- / vienn- 这类词干
        p = re.sub(r"\b[A-Za-zÀ-ÿ]{1,6}-(?=\s|$)", " ", p)
        p = re.sub(r"(?:\s*,\s*)+", ", ", p).strip(" ,")
        if not p:
            continue
        s = normalize_segment(p)
        if is_useful(s):
            out.append(finalize_segment(s))
    return out


def dedupe(seq: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for s in seq:
        key = s.casefold()
        if key in seen:
            continue
        seen.add(key)
        out.append(s)
    return out


def extract_segments(note: dict) -> tuple[list[str], str]:
    fields = note.get("fields", {})
    back = fields.get("Back", {}).get("value", "")
    front = fields.get("Front", {}).get("value", "")

    segs = code_segments(back)
    if segs:
        return dedupe(segs), "Back/<code>"
    segs = plain_chunks(back)
    if segs:
        return dedupe(segs), "Back/plain"
    segs = code_segments(front)
    if segs:
        return dedupe(segs), "Front/<code>"
    segs = plain_chunks(front)
    if segs:
        return dedupe(segs), "Front/plain"
    return [], "none"


def build_tts_text(segments: list[str]) -> str:
    parts = [s.rstrip(" .,;:!?") for s in segments]
    parts = [p for p in parts if p]
    text = ", ".join(parts)
    if text and not text.endswith((".", "!", "?")):
        text += "."
    return text


def audio_filename(text: str) -> str:
    digest = hashlib.sha1(text.encode("utf-8")).hexdigest()[:12]
    return f"fr_{digest}.mp3"


# ---------------------------------------------------------------------------
# 模型准备：加字段 + 改模板
# ---------------------------------------------------------------------------
def ensure_schema(model: str, field: str, apply: bool) -> None:
    fields = anki("modelFieldNames", modelName=model)
    LOG.info("模型 %s 现有字段：%s", model, fields)

    if field not in fields:
        LOG.info("需要新增字段 %s（index=%d）", field, len(fields))
        if apply:
            anki("modelFieldAdd", modelName=model, fieldName=field, index=len(fields))
            fields.append(field)
            LOG.info("已新增字段 %s", field)
    else:
        LOG.info("字段 %s 已存在，跳过", field)

    templates = anki("modelTemplates", modelName=model)
    changed = False
    for name, tpl in templates.items():
        back = tpl.get("Back", "")
        if "{{Audio}}" in back or TEMPLATE_MARKER in back:
            LOG.info("模板 %s 已包含 Audio 播放器，跳过", name)
            continue
        snippet = TEMPLATE_SNIPPET
        idx = back.find("<footer")
        if idx >= 0:
            new_back = back[:idx] + snippet + back[idx:]
        else:
            new_back = back + snippet
        LOG.info("模板 %s 将插入 Audio 播放器", name)
        tpl["Back"] = new_back
        changed = True

    if changed and apply:
        anki("updateModelTemplates", model={"name": model, "templates": templates})
        LOG.info("已更新模板")


# ---------------------------------------------------------------------------
# 音频生成
# ---------------------------------------------------------------------------
def check_edge_tts() -> None:
    try:
        import edge_tts
    except ImportError as exc:
        raise RuntimeError(
            "缺少 edge-tts。请用：uv run --with edge-tts==7.3.1 python add_audio.py --apply"
        ) from exc

    version = getattr(edge_tts, "__version__", "0.0.0")
    m = re.match(r"^(\d+)\.(\d+)\.(\d+)", version)
    if not m or tuple(int(x) for x in m.groups()) < (7, 3, 0):
        raise RuntimeError(
            f"edge-tts 版本过旧（{version}），微软接口会返回 403。\n"
            "请改用：uv run --with edge-tts==7.3.1 python add_audio.py --apply"
        )


async def edge_generate(text: str, voice: str, rate: str, out_path: Path) -> None:
    import edge_tts

    communicate = edge_tts.Communicate(text, voice, rate=rate)
    await communicate.save(str(out_path))


def youdao_generate(text: str, out_path: Path) -> None:
    """备用音源：有道词典发音。仅适合短文本；长文本接口会 500。"""
    url = (
        "https://dict.youdao.com/dictvoice?type=2&audio="
        + urllib.parse.quote(text)
    )
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = resp.read()
        content_type = resp.headers.get("Content-Type", "")
    if not content_type.startswith("audio/"):
        raise RuntimeError(f"有道发音返回了非音频内容：{content_type}")
    out_path.write_bytes(data)


def generate_audio(text: str, voice: str, rate: str, engine: str, out_path: Path) -> None:
    if engine == "youdao":
        youdao_generate(text, out_path)
    else:
        asyncio.run(edge_generate(text, voice, rate, out_path))


# ---------------------------------------------------------------------------
# 主流程
# ---------------------------------------------------------------------------
def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="给法语 Anki 卡批量添加发音")
    p.add_argument("--apply", action="store_true", help="真正修改 Anki；不加则只做 dry-run")
    p.add_argument("--dry-run", action="store_true", help="只打印计划，不修改（默认行为）")
    p.add_argument("--note-id", type=int, action="append", default=[], help="只处理指定 note id，可重复")
    p.add_argument("--limit", type=int, default=0, help="只处理前 N 张卡")
    p.add_argument("--deck-root", default=DEFAULT_DECK_ROOT, help=f"卡组前缀，默认 {DEFAULT_DECK_ROOT}")
    p.add_argument("--deck", action="append", default=[], help="精确卡组名，可重复；指定后忽略 --deck-root")
    p.add_argument("--model", default=DEFAULT_MODEL, help=f"笔记模型，默认 {DEFAULT_MODEL}")
    p.add_argument("--field", default=DEFAULT_FIELD, help=f"音频字段，默认 {DEFAULT_FIELD}")
    p.add_argument("--voice", default=DEFAULT_VOICE, help=f"edge-tts 音色，默认 {DEFAULT_VOICE}")
    p.add_argument("--rate", default=DEFAULT_RATE, help=f"语速，默认 {DEFAULT_RATE}")
    p.add_argument("--engine", choices=("edge", "youdao"), default="edge", help="默认 edge")
    p.add_argument("--force", action="store_true", help="即使 Audio 已匹配也重新生成")
    p.add_argument("--no-backup", action="store_true", help="跳过导出 .apkg 备份")
    p.add_argument("--backup-deck", default="法语::初级课程", help="备份用卡组名")
    return p.parse_args()


def make_backup(deck: str) -> Path | None:
    backup_dir = BASE_DIR / "backup"
    backup_dir.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    path = backup_dir / f"pre-audio-{stamp}.apkg"
    try:
        anki(
            "exportPackage",
            deck=deck,
            path=str(path),
            includeSched=True,
            includeMedia=True,
        )
        LOG.info("已导出备份：%s", path)
        return path
    except Exception as exc:  # noqa: BLE001
        LOG.error("备份失败：%s", exc)
        return None


def find_notes(args: argparse.Namespace) -> tuple[list[int], dict[int, str]]:
    if args.note_id:
        return sorted(set(args.note_id)), {}

    if args.deck:
        decks = args.deck
    else:
        all_decks = anki("deckNames")
        decks = [
            d
            for d in all_decks
            if d == args.deck_root or d.startswith(args.deck_root + "::")
        ]
    if not decks:
        raise RuntimeError(f"没有找到以 {args.deck_root!r} 开头的卡组")

    nids: set[int] = set()
    deck_by_nid: dict[int, str] = {}
    for deck in decks:
        ids = anki("findNotes", query=f'deck:"{deck}"')
        LOG.info("卡组 %s：%d 张", deck, len(ids))
        for raw in ids:
            nid = int(raw)
            nids.add(nid)
            # 同一张卡会同时出现在父卡组和子卡组里，保留更具体的名字
            if nid not in deck_by_nid or len(deck) > len(deck_by_nid[nid]):
                deck_by_nid[nid] = deck
    return sorted(nids), deck_by_nid


def load_manifest() -> dict:
    path = BASE_DIR / "audio_manifest.json"
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:  # noqa: BLE001
            LOG.warning("manifest 读取失败，将重建")
    return {"generated": [], "skipped": []}


def save_manifest(manifest: dict) -> None:
    path = BASE_DIR / "audio_manifest.json"
    path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    LOG.info("已写入 manifest：%s", path)


def media_exists(filename: str) -> bool:
    try:
        return bool(anki("retrieveMediaFile", filename=filename))
    except Exception:  # noqa: BLE001
        return False


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    args = parse_args()
    apply = args.apply and not args.dry_run

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        handlers=[
            logging.FileHandler(BASE_DIR / "anki_audio.log", encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )

    LOG.info("AnkiConnect version: %s", anki("version"))
    LOG.info("模式：%s", "APPLY" if apply else "DRY-RUN")

    if apply:
        check_edge_tts()

    if apply and not args.no_backup:
        if make_backup(args.backup_deck) is None:
            LOG.error("备份失败，已中止。可加 --no-backup 跳过备份。")
            return 2

    ensure_schema(args.model, args.field, apply)

    nids, deck_by_nid = find_notes(args)
    if args.limit > 0:
        nids = nids[: args.limit]
    LOG.info("待处理 %d 张卡", len(nids))

    info = []
    for i in range(0, len(nids), 100):
        info.extend(anki("notesInfo", notes=nids[i : i + 100]))

    manifest = load_manifest()
    generated = {int(x["nid"]): x for x in manifest.get("generated", [])}
    skipped = []
    ok = 0
    failed = 0
    unchanged = 0
    tmp_dir = BASE_DIR / "tmp"
    if apply:
        tmp_dir.mkdir(exist_ok=True)

    for note in info:
        nid = int(note["noteId"])
        deck = deck_by_nid.get(nid, note.get("deckName", ""))
        segments, source = extract_segments(note)
        if not segments:
            LOG.info("[SKIP] %s %s：没有找到可读的法语片段", nid, deck)
            skipped.append({"nid": nid, "deck": deck, "reason": "no-french"})
            continue

        text = build_tts_text(segments)
        filename = audio_filename(text)
        desired = f"[sound:{filename}]"
        current = note.get("fields", {}).get(args.field, {}).get("value", "").strip()

        if not args.force and current == desired and media_exists(filename):
            LOG.info("[OK]   %s %s：已存在 %s", nid, deck, filename)
            unchanged += 1
            continue

        if not apply:
            LOG.info(
                "[PLAN] %s %s | %s | %s | %r",
                nid,
                deck,
                source,
                filename,
                text,
            )
            continue

        tmp_path = tmp_dir / f"{nid}.mp3"
        try:
            generate_audio(text, args.voice, args.rate, args.engine, tmp_path)
            data = base64.b64encode(tmp_path.read_bytes()).decode("ascii")
            anki("storeMediaFile", filename=filename, data=data)
            anki(
                "updateNoteFields",
                note={"id": nid, "fields": {args.field: desired}},
            )
            generated[nid] = {
                "nid": nid,
                "deck": deck,
                "source": source,
                "text": text,
                "file": filename,
                "voice": args.voice,
                "rate": args.rate,
                "engine": args.engine,
                "created_at": datetime.now().isoformat(timespec="seconds"),
            }
            ok += 1
            LOG.info("[DONE] %s %s：%s", nid, deck, text)
            time.sleep(0.2)
        except Exception as exc:  # noqa: BLE001
            failed += 1
            LOG.error("[FAIL] %s %s：%s", nid, deck, exc)
        finally:
            try:
                tmp_path.unlink()
            except FileNotFoundError:
                pass

    if apply:
        manifest["generated"] = sorted(generated.values(), key=lambda x: x["nid"])
        manifest["skipped"] = skipped
        save_manifest(manifest)
        LOG.info(
            "完成：生成/更新 %d，已存在 %d，跳过 %d，失败 %d",
            ok,
            unchanged,
            len(skipped),
            failed,
        )
    else:
        LOG.info("dry-run 完成。加 --apply 才会真正写入 Anki。")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
