# CC Switch + OpenCode Go：后续对话上下文

> 用途：把这份文档贴给新的 AI 对话，或让 AI 先读它，就能继续维护这套 Claude Code 供应商配置。
> 最后更新：2026-10-26
> 详细方案、回滚与排错见同目录的 `CC-Switch与OpenCodeGo.md`。

---

## 一句话概况

Claude Code 通过 CC Switch v4.0.20 的本地代理（`127.0.0.1:15721`）访问 OpenCode Go（`https://opencode.ai/zen/go`，模型 `deepseek-v4.1-flash`）；真实密钥存在 `cc-switch.db`，`settings.json` 里只有 `PROXY_MANAGED` 占位符。

---

## 给 AI 的最短提示（可直接复制）

```text
你在维护我的 Claude Code 供应商配置。先读：
E:\ob\-first\-first\06-生产赋能\CC-Switch\CC-Switch与OpenCodeGo.md
E:\ob\-first\-first\06-生产赋能\CC-Switch\AI上下文.md

关键约束：
1. 不要手动往 ~/.claude/settings.json 里填真实 API key，那里应该是 PROXY_MANAGED。
2. 不要在 CC Switch 运行时改 settings.json，它会在切换供应商时覆盖你的修改。
3. 改供应商配置优先在 CC Switch 界面里改；必须改数据库时先退出 CC Switch 并备份。
4. apiFormat 必须是 anthropic；OpenCode Go 的 /zen/go 只认 x-api-key，不认 Bearer。
5. 模型名不要带 [1M] 后缀，OpenCode Go 会返回 400 Model is unavailable。
6. 切供应商后必须完整重启 Claude Code（claude --continue），再用 /status 确认。
7. 判断是否真的走 OpenCode Go，只看代理日志：
   C:\Users\15198\.cc-switch\logs\cc-switch.log
   找 "请求目标: https://opencode.ai/zen/go/v1/messages"。
8. 界面上显示 claude-opus-5 之类的名字是本地标签，实际执行的是 deepseek-v4.1-flash。
```

---

## 环境与路径

| 项目 | 值 |
|---|---|
| Claude Code | 2.1.310 |
| CC Switch | v4.0.20，`C:\Users\15198\AppData\Local\Programs\CC Switch\cc-switch.exe` |
| CC Switch 数据目录 | `C:\Users\15198\.cc-switch\` |
| 数据库 | `C:\Users\15198\.cc-switch\cc-switch.db` |
| 日志 | `C:\Users\15198\.cc-switch\logs\cc-switch.log` |
| Claude 配置 | `C:\Users\15198\.claude\settings.json` |
| 配置备份 | `C:\Users\15198\Downloads\cc-switch-backup-20261026\` |
| 代理端口 | `127.0.0.1:15721` |
| 当前供应商 | OpenCode Go（`is_current=1`，`apiFormat=anthropic`） |
| 上游模型 | `deepseek-v4.1-flash` |

---

## 不可违反的约束

1. **`settings.json` 里不写真实密钥。**
   - 应该是 `"ANTHROPIC_API_KEY": "PROXY_MANAGED"`。
   - 真 key 由 CC Switch 注入，存在数据库里。

2. **不要在 CC Switch 运行时手改 `settings.json`。**
   - 切换供应商时它会把文件重写一遍。
   - 要手改就先退出 CC Switch。

3. **改数据库前先退出 CC Switch 并备份。**
   - SQLite 被占用时写入可能失败或冲突。

4. **`apiFormat` 保持 `anthropic`。**
   - OpenCode Go 用 Anthropic Messages 协议，`openai_chat` 会转发失败。

5. **认证用 `x-api-key`（`ANTHROPIC_API_KEY`）。**
   - `/zen/go` 会静默忽略 Bearer，表现为 401。
   - 官方文档另有 `https://opencode.ai/inference/go/anthropic` + `ANTHROPIC_AUTH_TOKEN` 的写法，两种不要混用。

6. **模型名不带 `[1M]`。**
   - `deepseek-v4.1-flash[1M]` 会返回 400。
   - 用 `deepseek-v4.1-flash`。

7. **不要在响应里打印完整密钥。**
   - 只看前缀 `oc_sk_` 和后 4 位。

8. **代理只监听 `127.0.0.1`。**
   - 不要改成 `0.0.0.0`，否则局域网可访问你的密钥。

---

## 当前状态（2026-10-26）

- CC Switch v4.0.20 运行中，代理启用，日志开，自动故障转移关，最大重试 6。
- `providers` 表里两条 Claude 供应商：OpenCode Go（当前）、DeepSeek。
- OpenCode Go 的 key 形如 `oc_sk_...`（51 位），存在数据库里。
- 已验证：代理日志里每轮请求都指向 `zen/go`，模型 `deepseek-v4.1-flash`。
- DeepSeek 那条的模型名仍是 `deepseek-v4-flash[1M]`，切回去若报 400，去掉 `[1M]`。

**不要盲信上面的数字。** 用下面的命令取实时状态。

---

## 常用命令

```bash
# 当前供应商 / API 格式（只读）
sqlite3 -header -column "C:\Users\15198\.cc-switch\cc-switch.db" \
  "select name,is_current,json_extract(meta,'\$.apiFormat') from providers where app_type='claude' order by is_current desc;"

# 代理是否在监听
netstat -ano | grep 15721

# 最近转发目标
tail -5 "C:\Users\15198\.cc-switch\logs\cc-switch.log"

# CC Switch 版本
powershell -NoProfile -Command '(Get-Item "C:\Users\15198\AppData\Local\Programs\CC Switch\cc-switch.exe").VersionInfo.ProductVersion'
```

Windows 下 `sqlite3` 若报 `no such collation sequence: unicase`，改用 Python：

```python
import sqlite3, json
c = sqlite3.connect(r"C:\Users\15198\.cc-switch\cc-switch.db")
for row in c.execute("select name,is_current,meta from providers where app_type='claude'"):
    print(row)
```

---

## 维护流程

### 换供应商

1. CC Switch 里点目标卡片。
2. 退出并重启 Claude Code（`claude --continue`）。
3. `/status` 看 `ANTHROPIC_BASE_URL`。
4. `tail` 代理日志确认转发目标。

### 新增供应商

1. CC Switch 里新增，填 base URL、密钥、模型名。
2. `apiFormat` 选 `anthropic`。
3. 点卡片启用 → 重启 Claude Code → 看日志验证。

### OpenCode Go 换模型

在 CC Switch 界面的供应商里改模型名，或在数据库 `settings_config` 的 `env` 里改 `ANTHROPIC_MODEL` 与 `ANTHROPIC_DEFAULT_*_MODEL`（先退出 CC Switch）。

### 升级 CC Switch

1. 关掉 CC Switch，复制 `cc-switch.db` 到备份目录。
2. 装新版本，启动，确认供应商与代理设置还在。
3. 检查 `settings.json` 是否被重写、`apiFormat` 是否仍是 `anthropic`。

---

## 排错速查

| 现象 | 原因 | 处理 |
|---|---|---|
| `Connection refused 127.0.0.1:15721` | CC Switch 退出或代理关闭 | 启动 CC Switch / 开启代理 |
| 401 / 403 | 密钥错或认证头用错 | 确认用 `ANTHROPIC_API_KEY`；检查 `apiFormat` |
| 400 `MissingSessionID` | 手测时缺 `x-opencode-session` | 加该请求头；Claude Code 原生会带 |
| 400 `Model is unavailable` | 模型名不可用 / 带 `[1M]` | 改成 `deepseek-v4.1-flash` |
| 显示 Opus 但明显不是 Opus | 代理模型映射 | 正常，看日志 |
| 手改 settings 被还原 | CC Switch 在运行 | 先退出再改 |
| 日志没有 zen/go 行 | 请求走了别的供应商或别的 base | 检查 `is_current` 与 `ANTHROPIC_BASE_URL` |

---

## 文件地图

| 文件 | 作用 |
|---|---|
| `CC-Switch与OpenCodeGo.md` | 完整方案、架构、配置、同步功能、回滚、排错 |
| `AI上下文.md` | 本文件，给后续对话复用 |
| `C:\Users\15198\Downloads\cc-switch-backup-20261026\` | 升级前 DB、升级后 DB、settings 备份 |
| `C:\Users\15198\.claude\settings.json.before-opencode-go.bak` | 切到 OpenCode Go 之前的配置 |

---

## 设计说明（为什么这样配）

- **为什么用代理而不是直连**：密钥不落文件、切换不改文件、有重试与日志。代价是 Claude Code 依赖 CC Switch 进程。
- **为什么 `settings.json` 里模型名是 claude-opus-5**：代理按真实 Claude 名字接收请求，再用 `*_MODEL_NAME` 映射到上游模型。这样切换供应商时不用改 Claude Code 的模型偏好。
- **为什么 `CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1`**：第三方网关不支持 Claude 的实验性 beta 头，开着容易报错。
- **为什么 haiku 还是 claude-haiku-5-5**：后台小任务走 haiku 通道，保留原名便于代理侧识别；如果某天报模型不可用，也改成 `deepseek-v4.1-flash`。

---

## 变更记录

| 日期 | 内容 |
|---|---|
| 2026-10-26 | 建立文档；记录 v4.0.20 升级、OpenCode Go 接入、代理接管、验证方法与回滚路径 |
