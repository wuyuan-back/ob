```Latex
\documentclass[UTF8]{ctexart}

\usepackage{array}
\usepackage{booktabs}
\usepackage[table]{xcolor}
\usepackage{geometry}
\geometry{a4paper,left=2.5cm,right=2.5cm,top=2.5cm,bottom=2.5cm}

\definecolor{tableheader}{RGB}{220,230,241}
\definecolor{tablerow}{RGB}{245,248,252}
\definecolor{tablegreen}{RGB}{226,239,218}
\definecolor{tableyellow}{RGB}{255,242,204}
\definecolor{tablered}{RGB}{244,204,204}

\usepackage{hyperref}
\hypersetup{hidelinks,bookmarks=true,bookmarksopen=true,bookmarksnumbered=true}

\begin{document}

\tableofcontents
\newpage

\section{AI工具使用详情}

\subsection{AI工具的名称和版本}

\begin{table}[htbp]
\centering
\caption{AI工具名称及版本}
\small
\setlength{\tabcolsep}{4pt}
\begin{tabular}{p{3cm}p{2.5cm}p{8cm}}
\hline
\rowcolor{tableheader} 工具名称 & 工具版本 & 主要用途 \\
\hline
\rowcolor{tablerow} 示例AI助手 & 未提供 & 辅助背景知识理解、建模思路讨论、论文语言润色与格式检查 \\
\hline
\end{tabular}
\end{table}

\subsection{具体使用目的和环节}

\subsubsection{背景知识}

\begin{table}[htbp]
\centering
\caption{AI在背景知识整理阶段的使用情况}
\small
\setlength{\tabcolsep}{4pt}
\begin{tabular}{p{3cm}p{5.5cm}p{5cm}}
\hline
\rowcolor{tableheader} 使用目的 & AI辅助内容 & 最终使用情况 \\
\hline
\rowcolor{tablerow} 题目背景理解 & 解释碳交易、碳排放配额等基本概念 & 作为辅助理解材料，相关内容经参赛队员进一步核验 \\
\hline
\rowcolor{tablerow} 专业概念解释 & 说明优化模型中常见术语的含义 & 仅用于辅助理解，未直接作为论文事实来源 \\
\hline
\end{tabular}
\end{table}

\subsubsection{初步建模}

\begin{table}[htbp]
\centering
\caption{AI在初步建模阶段的使用情况}
\small
\setlength{\tabcolsep}{4pt}
\begin{tabular}{p{3cm}p{5.5cm}p{5cm}}
\hline
\rowcolor{tableheader} 建模环节 & AI提供的建议 & 队伍最终处理方式 \\
\hline
\rowcolor{tablerow} 变量设计 & 建议引入0-1变量表示设备是否启用 & 参赛队员结合题目约束修改后采用 \\
\hline
\rowcolor{tablerow} 候选算法比较 & 列出遗传算法、混合整数规划等求解思路 & 参赛队员分析数据规模后选择混合整数规划 \\
\hline
\end{tabular}
\end{table}

\subsubsection{论文写作}

\begin{table}[htbp]
\centering
\caption{AI在论文写作阶段的使用情况}
\small
\setlength{\tabcolsep}{4pt}
\begin{tabular}{p{3cm}p{5.5cm}p{5cm}}
\hline
\rowcolor{tableheader} 写作环节 & AI辅助内容 & 最终修改情况 \\
\hline
\rowcolor{tablerow} 语言润色 & 对摘要和引言进行语句通顺性调整 & 仅用于语言表达优化，未改变原有数学含义 \\
\hline
\rowcolor{tablerow} 格式检查 & 检查LaTeX表格与公式排版 & 参赛队员复核后调整，未改变核心内容 \\
\hline
\end{tabular}
\end{table}

\subsection{关键交互记录}

\begin{table}[htbp]
\centering
\caption{AI关键交互记录}
\small
\setlength{\tabcolsep}{4pt}
\begin{tabular}{p{0.8cm}p{2cm}p{4.8cm}p{6cm}}
\hline
\rowcolor{tableheader} 编号 & 使用阶段 & 核心提示词/问题 & AI回答及作用概述 \\
\hline
\rowcolor{tablerow} 1 & 背景知识 & 请简要解释碳交易机制的基本原理。 & 提供概念性解释，队员据此查阅教材后整理 \\
\hline
\rowcolor{tablerow} 2 & 初步建模 & 该优化问题可考虑哪些求解方法？ & 列出若干候选方法，队员分析后选择混合整数规划 \\
\hline
\end{tabular}
\end{table}

\subsection{采纳和修改的情况}

\begin{table}[htbp]
\centering
\caption{AI建议的采纳与修改情况}
\small
\setlength{\tabcolsep}{4pt}
\begin{tabular}{p{2.2cm}p{3.8cm}p{2.2cm}p{5.5cm}}
\hline
\rowcolor{tableheader} 使用环节 & AI建议 & 采纳情况 & 最终修改及原因 \\
\hline
\rowcolor{tablerow} 初步建模 & 采用遗传算法求解 & \cellcolor{tableyellow}部分采纳 & 结合题目规模和数据特点，改为混合整数规划，遗传算法仅作对照 \\
\hline
\rowcolor{tablerow} 论文写作 & 调整摘要句式 & \cellcolor{tablegreen}完全采纳 & 仅作语言润色，未改变数学含义 \\
\hline
\rowcolor{tablerow} 背景知识 & 直接引用某文献结论 & \cellcolor{tablered}未采纳 & 未提供可靠文献来源，未用于论文 \\
\hline
\end{tabular}
\end{table}

\end{document}
```