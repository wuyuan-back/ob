---
created: {{date:YYYY-MM-DD}} {{time:HH:mm}}
tags: [daily, plan]
aliases: [{{date:YYYY-MM-DD}}]
---

# 🌞 
{{date:YYYY-MM-DD}}

```button
name 添加今日课表
type command
action Templater: Insert template
command DailySchedule
templater true
class btn-outline
```
^button-add-schedule

```button
name 打开周视图
type command
action Calendar: Show weekly view
class btn-outline
```
^button-week-view

## 🕒 时间轴规划
```dataviewjs
try {
  await dv.view("_views/DailyTimeline");
} catch (e) {
  dv.paragraph(`> 🔧 时间轴加载错误: ${e.message}`);
}
```

## 📅 今日核心任务 (MITs)
- [ ] #学习 
- [ ] #生活 
- [ ] #项目 

## 📚 学习计划
### 🎓 课程学习
```dataview
TABLE WITHOUT ID
  choice(completed, "✅", "⬜") AS 状态,
  text AS 任务
FROM "01-Courses"
WHERE !completed AND due = date(this.file.name)
SORT priority DESC
```

### 📖 自主学习
- [ ] 英语单词30个
## 🧠 灵感笔记
```button
name + 添加灵感
type command
action QuickAdd: Capture
command 灵感笔记
templater true
class btn-sm
```
- ![[Inbox]]

## 💼 事务清单
```dataview
TASK FROM "待办事项"
WHERE !completed AND due <= date(this.file.name) + dur(1 day)
GROUP BY file.link
```

## 🎯 今日复盘
### ✅ 成就记录
- 

### ❌ 未完成事项
```dataview
TASK FROM ""
WHERE !completed AND due <= date(this.file.name) AND file.path != this.file.path
```

### 📈 效率分析
> 

### 🔁 明日优化
1. 

---
### 🔄 任务迁移
```button
name 将未完成移到明日
type command
action Tasks: Move undone tasks to daily note
command tomorrow
class success
```


