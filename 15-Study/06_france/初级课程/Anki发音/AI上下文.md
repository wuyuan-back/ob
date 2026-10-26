# Anki 法语发音：后续对话上下文

> 用途：把这份文档贴给新的 AI 对话，或让 AI 先读它，就能继续维护这套法语 Anki 发音系统。
> 最后更新：2026-10-26
> 详细原理与回滚见同目录的 `方案.md`。
> 工具目录：`E:\ob\-first\-first\15-Study\06_france\初级课程\Anki发音\`

---

## 一句话概况

法语卡的发音存在 Anki 的独立 `Audio` 字段里，由 `add_audio.py` 用 edge-tts 生成、通过 AnkiConnect 写入；Obsidian 的 Flashcards 插件只管理 `Front`、`Back`、`Context`、`Source`，不会覆盖 `Audio`。

---

## 给 AI 的最短提示（可直接复制）

```text
你在维护我的法语 Anki 发音系统。先读：
E:\ob\-first\-first\15-Study\06_france\初级课程\Anki发音\方案.md
E:\ob\-first\-first\15-Study\06_france\初级课程\Anki发音\AI上下文.md

关键约束：
1. 发音只写 Audio 字段（[sound:fr_<hash>.mp3]），绝对不要写进 Back/Front/Context/Source，否则 Flashcards 插件下次同步会覆盖。
2. 不要运行 Obsidian 命令面板里的 "Apply v2 Anki card style"，它会重置模板并删掉 {{Audio}}。误按后重跑 run.bat --apply 可补回。
3. 生成音频必须用 edge-tts 7.3.1：run.bat 已经封装为 uv run --with edge-tts==7.3.1；系统自带的 7.2.7 会 403。
4. Anki 必须开着，AnkiConnect 在 127.0.0.1:8765。
5. 写操作前先跑 run.bat --dry-run；确认后再 run.bat --apply。
6. 当前状态：56 张法语卡，55 张有音频，1 张跳过（note id 1792841304235，只讲词尾变化）。不要盲信这个数字，先跑 dry-run 获取实时状态。

常用命令（在工具目录执行）：
run.bat --dry-run
run.bat --apply
run.bat --apply --note-id <id>
run.bat --apply --force --voice fr-FR-HenriNeural --rate "-5%"
```

---

## 环境与路径

| 项目 | 值 |
|---|---|
| Obsidian vault | `E:\ob\-first\-first` |
| 法语课程目录 | `E:\ob\-first\-first\15-Study\06_france\初级课程` |
| 工具目录 | `E:\ob\-first\-first\15-Study\06_france\初级课程\Anki发音` |
| Anki 配置目录 | `C:\Users\15198\AppData\Roaming\Anki2\2` |
| Anki 数据库 | `C:\Users\15198\AppData\Roaming\Anki2\2\collection.anki2` |
| Anki 媒体库 | `C:\Users\15198\AppData\Roaming\Anki2\2\collection.media` |
| AnkiConnect | `http://127.0.0.1:8765`，version 6 |
| 笔记模型 | `Obsidian-basic` |
| 音频字段 | `Audio` |
| 卡组 | `法语::初级课程::Unit 2`、`Unit 3`、`Unit 4` |
| Obsidian 插件 | `flashcards-obsidian` v2.2.0（Flashcards） |
| 音色 | `fr-FR-DeniseNeural`，语速 `-10%` |

AnkiBridge 监听的是 `28765`，和 AnkiConnect 的 `8765` 无关，不用管它。

---

## 不可违反的约束

1. **发音只写 `Audio` 字段。**
   - 写成 `[sound:fr_xxxxxxxxxxxx.mp3]`。
   - 不要写进 `Back`、`Front`、`Context`、`Source`。
   - 原因：Flashcards 插件同步时只更新这四个字段，写进去会被 Markdown 原内容覆盖。

2. **不要运行 `Apply v2 Anki card style`。**
   - 它会重置四个 Obsidian 模板和 CSS，删掉 `{{Audio}}`。
   - 正常同步（`Update Anki from current note` / `Update Anki from vault`）不会触发它。
   - 误按后重跑 `run.bat --apply`，脚本会自动补回模板。

3. **edge-tts 必须是 7.3.x。**
   - 系统 Python 里是 7.2.7，微软接口会返回 403。
   - 统一用 `run.bat`，它封装了 `uv run --with edge-tts==7.3.1`。

4. **Anki 必须保持打开。**
   - 脚本通过 AnkiConnect 读写，Anki 关闭会报连接失败。
   - 批量写入期间不要关闭 Anki。

5. **不要手动改源笔记 frontmatter 里的 `flashcards:` 条目。**
   - 那些 `nid`、`hash`、`sync` 是插件用来定位 Anki 笔记的。
   - 改坏了插件会重建笔记，音频会丢。

6. **不要改字段名 `Audio`，也不要删模板里的 `<!-- anki-audio -->` 标记。**
   - 模板引用 `{{Audio}}`；标记用于脚本幂等判断。

7. **不要在 Obsidian 运行时直接改插件的 `data.json`。**
   - 需要调整同步范围时，用插件设置界面。

8. **写操作前先备份。**
   - 脚本在 `--apply` 时会自动导出一份 `.apkg` 到 `backup/`。
   - 大改动前可以再手动复制 `collection.media` 或整个配置。

---

## 当前状态（2026-10-26）

- 法语卡总数：56 张。
- 已生成音频：55 张。
- 跳过：1 张，note id `1792841304235`（Unit 2，只讲 `-e, -es, -e, -ons, -ez, -ent` 词尾，没有可读的完整法语词）。
- 媒体文件：55 个 `fr_*.mp3`，约 927 KB。
- 模型字段：`Front`、`Back`、`Context`、`Source`、`Audio`。
- 背面模板包含：`{{#Audio}}<div class="fc-audio">{{Audio}}</div>{{/Audio}}<!-- anki-audio -->`。
- 原有四个字段与改动前逐条比对：0 处变化。
- 模拟插件同步（只写四个字段）后 `Audio` 仍在：已验证。
- 插件新建卡（只传四个字段）能正常创建，`Audio` 为空：已验证。

**不要盲信上面的数字。** 先运行 `run.bat --dry-run`，以输出为准。

---

## 常用命令

在工具目录执行：

```bat
cd /d "E:\ob\-first\-first\15-Study\06_france\初级课程\Anki发音"

rem 只看计划，不修改
run.bat --dry-run

rem 批量生成/更新
run.bat --apply

rem 只处理一张卡
run.bat --apply --note-id 1792841304500

rem 只处理前 5 张
run.bat --apply --limit 5

rem 强制重新生成（换了音色/语速时用）
run.bat --apply --force

rem 换男声、语速 -5%
run.bat --apply --force --voice fr-FR-HenriNeural --rate "-5%"
```

等价的完整写法：

```bash
uv run --with edge-tts==7.3.1 python add_audio.py --apply
```

### 参数说明

| 参数 | 作用 |
|---|---|
| `--dry-run` | 只打印计划，默认行为 |
| `--apply` | 真正修改 Anki |
| `--note-id` | 只处理指定 note id，可重复 |
| `--limit N` | 只处理前 N 张 |
| `--deck-root` | 卡组前缀，默认 `法语` |
| `--deck` | 精确卡组名，可重复 |
| `--voice` | edge-tts 音色，默认 `fr-FR-DeniseNeural` |
| `--rate` | 语速，默认 `-10%` |
| `--force` | 即使已存在也重新生成 |
| `--no-backup` | 跳过 `.apkg` 备份（不建议） |
| `--engine` | `edge`（默认）或 `youdao`（仅短文本备用） |

---

## 维护流程

### 修改了法语卡片文字

1. 在 Obsidian 里改 `unit2.md` / `Unit3.md` / `Unit 4 -Lesson G.md`。
2. 用 Flashcards 的 `Update Anki from current note` 或 `Update Anki from vault` 同步。
3. 运行 `run.bat --apply`。
4. 脚本按新文本生成新哈希文件名，旧音频会自动不再被引用。

### 新增了法语卡片

1. Obsidian 里加卡并同步到 Anki。
2. 运行 `run.bat --apply`。
3. 新卡的 `Audio` 为空，脚本会自动补。

### 新增了一个法语子卡组

默认 `--deck-root 法语` 会匹配所有以 `法语::` 开头的卡组，通常不用改。如果卡组不在 `法语` 下，用 `--deck-root <前缀>` 或 `--deck <完整卡组名>`。

### 换了音色或语速

```bat
run.bat --apply --force --voice fr-FR-HenriNeural --rate "-5%"
```

文件名只由文本决定，所以会覆盖同名 mp3。如果希望保留旧音色，需要改脚本的命名规则。

### 想给某张卡单独加音

```bat
run.bat --apply --note-id <note-id>
```

note id 可以在 Anki 浏览器的卡片信息里看到，或通过 AnkiConnect 的 `findNotes` / `notesInfo` 查询。

---

## 验证与排错

### 快速验证实时状态

```bat
run.bat --dry-run
```

- `[OK]`：已存在且媒体可读。
- `[PLAN]`：需要生成。
- `[SKIP]`：没有可读法语片段。

正常情况下应该是 `OK=55 PLAN=0 SKIP=1`（截至 2026-10-26）。如果新增了卡，`PLAN` 会大于 0。

### 常见错误

| 现象 | 原因 | 处理 |
|---|---|---|
| `Invalid response status` 403 | edge-tts 7.2.7 | 用 `run.bat` 或 `uv run --with edge-tts==7.3.1` |
| `无法连接 AnkiConnect` | Anki 没开 | 打开 Anki，确认 8765 可访问 |
| 卡片背面没有播放器 | `Audio` 为空或模板被重置 | 跑 `run.bat --apply`；检查模板里的 `{{Audio}}` |
| Obsidian 同步后发音没了 | 音频被写进四个托管字段，或 note 被重建 | 检查 `Audio` 字段；重跑脚本 |
| `Check Media` 报未使用文件 | 文本改过后旧 mp3 残留 | 确认新音频正常后，用 Anki 的检查媒体删除未使用文件 |

### 手动检查某个 note

用 AnkiConnect 查询：

```text
action: notesInfo
params: {"notes":[<note-id>]}
```

看返回的 `fields.Audio.value` 是否为 `[sound:fr_xxxxxxxxxxxx.mp3]`。

---

## 文件地图

| 文件 | 作用 |
|---|---|
| `方案.md` | 完整方案、插件边界、回滚、FAQ |
| `AI上下文.md` | 本文件，给后续对话复用 |
| `add_audio.py` | 提取法语、edge-tts 生成、AnkiConnect 写入 |
| `run.bat` | 快捷启动，封装 edge-tts 7.3.1 |
| `audio_manifest.json` | 已生成音频清单（note id、文本、文件、音色、时间） |
| `anki_audio.log` | 每次运行的日志 |
| `backup/` | 改动前备份（`.colpkg` 和 `.apkg`） |
| `tmp/` | 运行时临时目录，脚本会自动重建 |

---

## 插件行为备忘（为什么这样设计）

- `flashcards-obsidian` v2.2.0 建卡时只写 `Front`、`Back`、`Context`、`Source`。
- 更新时只调用 `updateNoteFields` 并传入这四个字段。
- 读取现有笔记做比较时，`la()` 只取这四个字段参与哈希，`Audio` 被忽略。
- 正常同步只在缺少 `Context` / `Source` 时补模板，不会重建整个模板，所以 `{{Audio}}` 保留。
- `Apply v2 Anki card style` 是唯一会重置模板和 CSS 的手动命令。
- 卡片类型改变、note 丢失后恢复、删卡后重建，都会新建 note，新 note 的 `Audio` 为空，需要重跑脚本。

---

## 变更记录

| 日期 | 内容 |
|---|---|
| 2026-10-26 | 建立方案；新增 `Audio` 字段与 `{{Audio}}` 模板；55/56 张卡生成发音；1 张词尾卡跳过；建立备份、manifest、日志、`run.bat` |
