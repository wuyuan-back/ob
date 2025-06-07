---
created: {{date:YYYY-MM-DD}} {time:HH:mm}}
tags: [daily, plan]
aliases: [{{date:YYYY-MM-DD}}]
---

# 🌞 {{date:YYYY年MM月DD日}} dddd

```button
name 添加今日课表
type command
action Templater: Insert template
command DailySchedule
templater true
## 📅 今日核心任务 (MITs)
- [ ] #学习 示例任务1 @due(今天 18:00) ^mit-1
- [ ] #生活 示例任务2 ^mit-2
- [ ] #项目 示例任务3 ^mit-3

## 📚 学习计划
### 🎓 课程学习
```dataview
TASK FROM "01-Courses"
WHERE !completed AND due = date(this.file.name)
SORT priority DESC
```

### 📖 自主学习
- [ ] 英语学习 @after(14:00)
- [ ] 专业技能学习 @duration(45min)

## 🧠 灵感笔记
- ![[Inbox]]

## 💼 事务清单
```dataview
TASK FROM "待办事项"
WHERE !completed AND due <= date(this.file.name) + dur(1 day)
```

## 🎯 今日复盘
### ✅ 成就记录
- 

### ❌ 未完成事项
- 

### 📈 效率分析
> 

### 🔁 明日优化
1. 
