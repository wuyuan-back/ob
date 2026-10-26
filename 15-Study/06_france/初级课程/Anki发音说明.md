# 法语 Anki 发音说明

这套法语卡的发音已接入 Anki 的 `Audio` 字段，背面会自动显示播放器。

- 给后续 AI 对话的完整上下文：[[Anki发音/AI上下文]]
- 方案、原理、回滚与 FAQ：[[Anki发音/方案]]
- 工具目录：`15-Study/06_france/初级课程/Anki发音/`

日常流程：Obsidian 改卡 → Flashcards 同步 → 在工具目录运行 `run.bat --apply`。

两个不要：

1. 不要把 `[sound:...]` 写进 `Back`，只写 `Audio` 字段。
2. 不要运行 `Apply v2 Anki card style`，它会重置模板并删掉 `{{Audio}}`。
