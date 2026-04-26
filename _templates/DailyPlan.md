按照你的要求，在原有的基础上添加了**显示昨日未完成待办**的部分。

Markdown


# 📅 <% tp.date.now("YYYY-MM-DD") %>

## 📊 任务进度
```dataviewjs
let tasks = dv.current().file.tasks;
let total = tasks.length;
let completed = tasks.where(t => t.completed).length;
let progress = total > 0 ? Math.round((completed / total) * 100) : 0;

dv.el("div", `
    <div style="background-color: #333; border-radius: 10px; width: 100%; height: 12px; border: 1px solid #555;">
        <div style="background-color: #50fa7b; width: ${progress}%; height: 100%; border-radius: 8px;"></div>
    </div>
    <div style="text-align: right; font-size: 0.75em; margin-top: 5px;">
        ${progress}% 已完成 (${completed}/${total})
    </div>
`);
````

---

## ⚠️ 昨日未完成


```dataview
TASK
WHERE !completed 
AND file.day = date(today) - dur(1 day)
```

---

## ⚡ 四象限待办清单

### 🔴 第一象限：重要且紧急

- [ ]
    

### 🟡 第二象限：重要不紧急

- [  ]洗澡

    

### 🔵 第三象限：紧急不重要

- [ ]
    

### ⚪ 第四象限：不重要不紧急

- [ ]