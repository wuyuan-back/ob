---
created: 2026-06-30
tags:
  - claude
  - skill
  - AI
  - 配置
---

# Claude Code Skill 配置指南

> Skill 是 Claude Code 的自定义斜杠命令系统，让你可以用 `/foo` 快速触发特定任务。

---

## 一、什么是 Skill？

Skill 本质上是**预设好 prompt 的快捷指令**。输入 `/技能名` 就会加载对应的系统提示，让 Claude 进入特定工作模式。

### 内置 Skill 示例

| 命令 | 功能 |
|------|------|
| `/code-review` | 审查当前 diff 的代码 |
| `/deep-research` | 多源搜索并生成研究报告 |
| `/verify` | 运行应用并验证功能 |
| `/security-review` | 安全审查 |
| `/loop` | 定时重复执行某个任务 |
| `/simplify` | 代码简化与重构 |

> 输入 `/` 即可看到所有可用的 skill 列表。

---

## 二、Skill 的两种定义方式

### 方式 A：CLI 快速创建

```bash
# 直接在命令行创建
claude skill create my-skill --prompt "帮我做代码审查，关注安全问题"
```

### 方式 B：手动创建 Skill 文件

Skill 文件存放在 `.claude/skills/` 目录下，每个 skill 一个 `.md` 文件：

```markdown
---
name: my-skill
description: 我的自定义 skill
---

帮我做代码审查，关注以下方面：
1. SQL 注入风险
2. XSS 漏洞
3. 权限校验遗漏
```

使用方式：
```bash
# 或输入 /my-skill
claude /my-skill
```

---

## 三、Skill 文件结构详解

### Frontmatter 字段

```yaml
---
name: my-skill              # Skill 名称（必填）
description: 简短描述       # 描述（必填，显示在 / 列表中）
model: sonnet              # 可选：指定模型
---
```

### 支持的字段

| 字段 | 必填 | 说明 |
|------|------|------|
| `name` | ✅ | Skill 名称，用于 `/name` 调用 |
| `description` | ✅ | 一行描述，显示在 skill 列表 |
| `model` | ❌ | 覆盖模型：`sonnet` / `opus` / `haiku` |
| `effort` | ❌ | 推理力度：`low` / `medium` / `high` |

### 可用模型

| 标识 | 模型 | 用途 |
|------|------|------|
| `sonnet` | Claude Sonnet | 默认，速度与质量平衡 |
| `opus` | Claude Opus | 复杂推理任务 |
| `haiku` | Claude Haiku | 快速轻量任务 |

---

## 四、Skill 存放位置

Skill 文件放置在项目根目录下的 `.claude/skills/` 文件夹：

```
.claude/
├── skills/
│   ├── my-skill.md        # 自定义 skill
│   ├── code-review.md     # 代码审查
│   └── fix-issue.md       # 修复 issue
├── settings.json          # 配置文件
└── keybindings.json       # 快捷键
```

**命名规则**：
- 文件名去掉 `.md` 后缀就是 skill 名称
- 例如 `.claude/skills/my-skill.md` -> `/my-skill`
- 支持子目录：`.claude/skills/dev/fix.md` -> 通过完整路径调用

---

## 五、实用 Skill 模板

### 5.1 代码审查

```markdown
---
name: review-js
description: JavaScript 代码审查
---

审查代码并反馈以下方面：
1. 是否有未处理的错误（try-catch 缺失）
2. 是否有潜在的内存泄漏
3. 是否有类型安全问题
4. 是否有性能优化空间
5. 代码可读性和命名规范

对每个问题给出：问题位置 + 严重程度 + 修复建议。
```

### 5.2 Git 提交信息生成

```markdown
---
name: commit
description: 生成规范的 Git 提交信息
---

分析当前 diff，生成符合 Conventional Commits 规范的提交信息。
格式：`<type>(<scope>): <description>`

type 可选：feat / fix / refactor / docs / style / test / chore
```

### 5.3 学习笔记助手

```markdown
---
name: study-note
description: 将选中内容整理成 Obsidian 笔记
---

将选中的内容整理成结构化的 Obsidian 笔记，要求：
1. 添加 YAML frontmatter (tags, created 等)
2. 使用标题分级组织内容
3. 提取关键概念并解释
4. 用 `[[wikilink]]` 关联相关概念
5. 最后给出总结和延伸思考
```

### 5.4 Verilog 调试助手

```markdown
---
name: verilog-debug
description: Verilog 代码调试助手
---

分析 Verilog 代码中的问题：
1. 检查是否有 latch 推断
2. 检查阻塞/非阻塞赋值是否正确
3. 检查敏感列表是否完整
4. 检查是否有 multiple drivers
5. 给出修正后的代码
```

---

## 六、Skill 进阶用法

### 6.1 链式 Skill

在设计 Skill 时，可以**调用其他 Skill** 来组合功能。比如调试 skill 可以引用审查 skill 的结果。

### 6.2 带参数 Skill

Skill 内容中可以包含占位符，在调用时补充具体信息：

```markdown
---
name: fix-issue
description: 根据 issue 编号修复问题
---

请修复 GitHub issue #{{ISSUE_NUMBER}} 中描述的问题。
1. 先理解问题背景和复现步骤
2. 定位相关代码文件
3. 提出修复方案
4. 实施修复
5. 验证修复正确性
```

### 6.3 作用域限定 Skill

某些 skill 只在特定目录下可用。在 `.claude/settings.json` 中配置：

```json
{
  "skills": {
    "verilog-debug": {
      "scopes": ["2026/大二小学期/verilog"]
    }
  }
}
```

这样 `/verilog-debug` 只在处理 verilog 目录下文件时可用。

---

## 七、配置文件 settings.json

除了 skill 文件本身，还可以在 `.claude/settings.json` 中配置 skill 行为：

```json
{
  "skills": {
    "my-skill": {
      "description": "覆盖文件中的描述",
      "model": "sonnet",
      "scopes": ["src/**"],
      "aliases": ["ms"]    // 别名：/ms 也可调用
    }
  },
  "permissions": {
    "allow": ["bash", "read", "write", "edit", "glob", "grep"]
  }
}
```

### 常用配置选项

```json
{
  "skills": {},
  "permissions": {
    "allow": [],
    "deny": []
  },
  "hooks": {
    "preCommand": [],
    "postCommand": []
  },
  "model": "sonnet",
  "theme": "dark",
  "verbose": false
}
```

---

## 八、最佳实践

### 8.1 Skill 设计原则

1. **单一职责**：一个 skill 只做一件事，做精
2. **明确的输出期望**：告诉 Claude 你希望输出什么格式
3. **提供上下文**：在 prompt 中给出足够的背景信息
4. **适中的长度**：太短的 prompt 效果不稳定，太长则浪费 token
5. **迭代优化**：用几次后根据效果调整 prompt

### 8.2 命名规范

```markdown
✅ 好的命名：
- code-review       # 清晰表明功能
- commit            # 简短明确
- verilog-debug     # 带上上下文

❌ 不好的命名：
- a                 # 不知所云
- my-skill          # 太泛泛
- test123           # 无意义
```

### 8.3 Skill 测试流程

```bash
# 1. 创建 skill 文件
touch .claude/skills/my-skill.md

# 2. 测试调用
claude /my-skill

# 3. 观察效果，调整 prompt
# 4. 重复 2-3 步直到满意
```

---

## 九、故障排除

| 问题 | 原因 | 解决 |
|------|------|------|
| `/xxx` 找不到 | skill 文件不在 `.claude/skills/` 目录下 | 检查文件路径 |
| 描述不显示 | frontmatter 缺少 `description` 字段 | 补全 YAML 字段 |
| 模型不对 | 未在 frontmatter 或 settings.json 中指定 | 添加 `model` 字段 |
| Skill 内容不生效 | YAML frontmatter 格式错误 | 检查 `---` 分隔符是否正确 |
| 编码问题 | 文件保存为非 UTF-8 | 确保文件为 UTF-8 编码 |

---

## 十、与 Obsidian 结合

Skill 可以和 Obsidian 工作流深度结合：

### 笔记处理工作流

```markdown
---
name: organize-note
description: 整理 Obsidian 笔记
---

优化当前笔记的结构：
1. 确保 YAML frontmatter 完整
2. 使用合适的标题层级
3. 添加 `[[wikilink]]` 关联相关笔记
4. 修正标签格式
5. 保持笔记内容完整性，不要删减
```

### 批量处理

结合 `/loop` 可以定时执行某些 skill：

```bash
# 每 30 分钟检查一次待办
/loop 30m /check-todos
```

---

## 参考链接

- [[2026/大二小学期/ai-update/claude配置|Claude Code 配置指南]]
- [[CLAUDE.md]] - 项目协作准则
- [[.claude/settings.json]] - 项目级配置

> **一句话总结**：Skill = 预设 prompt 的快捷指令，用 `/` 触发。学会自己写 skill，日常开发效率翻倍。
