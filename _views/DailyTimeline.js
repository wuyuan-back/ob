// JavaScript source code
// 获取当前时间
const now = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });

// 获取今日任务
const todayFile = dv.current().file;
const tasks = dv.pages('"00-Daily"')
    .where(p => p.file.name === todayFile.name)
    .file.tasks
    .where(t => !t.completed);

dv.paragraph(`⏰ **今日时间轴 | 当前时间: ${now}**`);

if (tasks.length > 0) {
    // 按时间段排序
    const sortedTasks = tasks.sort(t => {
        const timeMatch = t.text.match(/@due\((\d{4}-\d{2}-\d{2}T(\d{2}:\d{2}))\)/);
        return timeMatch ? timeMatch[2] : "23:59";
    });

    dv.table(["⌚ 时间", "✅ 任务", "🏷️ 标签"],
        sortedTasks.map(t => {
            const timeMatch = t.text.match(/@due\((\d{4}-\d{2}-\d{2}T(\d{2}:\d{2}))\)/);
            const cleanText = t.text
                .replace(/@\w+\([^)]+\)/g, "")
                .replace(/^\s*-\s*\[\s*\]\s*/, "");

            return [
                timeMatch ? timeMatch[2] : "全天",
                cleanText.length > 30 ? cleanText.slice(0, 27) + "..." : cleanText,
                t.tags.join(", ") || "无标签"
            ];
        })
    );
} else {
    dv.paragraph("> 🎉 今日尚无计划任务，添加些内容吧！");
}

// 添加时间分配建议
dv.paragraph(`\n### ⏳ 最佳学习时段建议
- **8:00-10:00** 高难度学习（数学/编程）
- **14:00-16:00** 实践练习（实验/写作）
- **19:00-21:00** 复习整理（笔记/错题）
`);