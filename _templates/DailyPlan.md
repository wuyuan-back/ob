---
created: {{date:YYYY-MM-DD}} {{time:HH:mm}}
tags: [daily, plan]
---

# 🌞 {{date:YYYY年MM月DD日}} dddd

```button
name 添加今日课表
type command
action Templater: Insert template
command DailySchedule
templater true
^button-add-schedule