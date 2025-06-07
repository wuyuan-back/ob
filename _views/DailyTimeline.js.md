// 增强版时间轴视图
const { moment } = dv.app.plugins.plugins['templater-obsidian'].templater.current_functions_object;
const now = moment().format("HH:mm");

dv.paragraph(`⏰ **时间轴 | 当前时间: ${now}**`);

const tasks = dv.pages('"00-Daily"')
    .where(p => p.file.name == dv.current().file.name)
    .file.tasks
    .where(t => !t.completed);

if (tasks.length > 0) {
    dv.table(["⌚ 时间", "✅ 任务", "🏷️ 标签"],
        tasks.map(t => [
            t.due ? moment(t.due).format("HH:mm") : "全天",
            t.text.replace(/@\w+\([^)]+\)/g, ""), // 移除任务语法
            t.tags.join(", ")
        ])
    );
} else {
    dv.paragraph("> 今日尚无计划任务");
}

// 添加时间块建议
dv.paragraph("### ⏳ 推荐时间分配\n- 上午8-12点：深度学习\n- 下午2-5点：实践练习\n- 晚上7-9点：复习整理");