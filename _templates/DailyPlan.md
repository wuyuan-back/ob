
---

## 📅 {{date}} 智能任务看板
// 获取当前文件的所有任务
let tasks = dv.current().file.tasks;
let total = tasks.length;
let completed = tasks.where(t => t.completed).length;
let progress = total > 0 ? Math.round((completed / total) * 100) : 0;

// 设置进度条颜色：低于 30% 红色，30-70% 黄色，70% 以上绿色
let color = progress < 30 ? "#ff5555" : (progress < 70 ? "#f1fa8c" : "#50fa7b");

// 渲染 HTML 进度条
dv.el("div", `
    <div style="background-color: #333; border-radius: 10px; width: 100%; height: 20px; border: 1px solid #555;">
        <div style="background-color: ${color}; width: ${progress}%; height: 100%; border-radius: 8px; transition: width 0.3s ease-in-out;">
        </div>
    </div>
    <div style="text-align: right; font-size: 0.8em; margin-top: 5px;">
        ${completed} / ${total} 任务已完成 (${progress}%)
    </div>
`);

### 🚀 核心象限

> [!multi-column]
> 
> > ### 🔴 1. 重要且紧急
> > 
> > Code snippet
> > 
> > ```
> > TASK
> > WHERE file.path = this.file.path
> > AND priority = 1
> > AND !completed
> > ```
> 
> > ### 🟡 2. 重要不紧急
> > 
> > Code snippet
> > 
> > ```
> > TASK
> > WHERE file.path = this.file.path
> > AND priority = 2
> > AND !completed
> > ```

> [!multi-column]
> 
> > ### 🔵 3. 紧急不重要
> > 
> > Code snippet
> > 
> > ```
> > TASK
> > WHERE file.path = this.file.path
> > AND priority = 3
> > AND !completed
> > ```
> 
> > ### ⚪ 4. 不重要不紧急
> > 
> > Code snippet
> > 
> > ```
> > TASK
> > WHERE file.path = this.file.path
> > AND priority = 4
> > AND !completed
> > ```

---

## ⚡ 任务输入区

> 在这里输入你的任务，并使用 `[priority:: 数字]` 进行分类（1-4 分别对应四个象限）。

- [ ] 示例：复习信号与系统笔记 [priority:: 1]
    
- [ ] 示例：吉他爬音阶练习 15 分钟 [priority:: 2]
    
- [ ] 示例：回复社团群聊消息 [priority:: 3]
    
- [ ] 示例：整理电子零件收纳盒 [priority:: 4]
    
- [ ]
    

---

## 📊 今日统计

Code snippet

```
TABLE count(rows) as 数量
WHERE file.path = this.file.path
GROUP BY priority
```

---
