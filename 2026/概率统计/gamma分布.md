
---

# 概率论笔记：Gamma 分布 (Gamma Distribution)

## 1. 基本定义

若随机变量 $X$ 的概率密度函数满足以下形式，则称 $X$ 服从参数为 $\alpha, \lambda$ 的 Gamma 分布，记作 $X \sim \Gamma(\alpha, \lambda)$：

$$f(x) = \begin{cases} \frac{\lambda^\alpha}{\Gamma(\alpha)} x^{\alpha-1} e^{- \lambda x}, & x > 0 \\ 0, & x \le 0 \end{cases}$$

### 参数含义：

- **$\alpha$ (形状参数, Shape Parameter)：** 决定分布曲线的形状。
    
- **$\lambda$ (尺度/速率参数, Rate Parameter)：** 决定分布的陡峭程度（有的教材使用 $\theta = 1/\lambda$ 作为尺度参数）。
    
- **$\Gamma(\alpha)$ (Gamma 函数)：** 定义为 $\Gamma(\alpha) = \int_0^\infty t^{\alpha-1} e^{-t} dt$。
    
    - **重要性质：** $\Gamma(n) = (n-1)!$（当 $n$ 为正整数时）。
        

---

## 2. 物理意义与直观理解

Gamma 分布通常被看作是**等待时间**的分布：

- **指数分布**：等 **1** 次随机事件发生所需的时间。
    
- **Gamma 分布**：等 **$\alpha$** 次随机事件发生所需的总时间。
    

> **结论：** 若 $X_1, X_2, \dots, X_n$ 是独立同分布的指数分布随机变量 $X_i \sim Exp(\lambda)$，那么它们的和 $S_n = \sum_{i=1}^n X_i$ 服从 $\Gamma(n, \lambda)$ 分布。

---

## 3. 核心性质（考试/科研常用）

### ① 可加性 (Summation Property)

设 $X \sim \Gamma(\alpha_1, \lambda)$，$Y \sim \Gamma(\alpha_2, \lambda)$，且 $X, Y$ 相互独立，则：

$$X + Y \sim \Gamma(\alpha_1 + \alpha_2, \lambda)$$

_注意：必须是相同的速率参数 $\lambda$ 才能直接相加。_

### ② 期望与方差

- **期望 (Mean):** $E(X) = \frac{\alpha}{\lambda}$
    
- **方差 (Variance):** $D(X) = \frac{\alpha}{\lambda^2}$
    

### ③ 与其他分布的关系

|**分布关系**|**条件**|
|---|---|
|**指数分布**|当 $\alpha = 1$ 时，$\Gamma(1, \lambda) \equiv Exp(\lambda)$|
|**卡方分布 ($\chi^2$)**|当 $\alpha = n/2, \lambda = 1/2$ 时，即为 $\chi^2(n)$|
|**正态分布**|当 $\alpha \to \infty$ 时，根据中心极限定理，Gamma 分布趋于正态分布|

---

## 4. 通信工程中的应用 (专业背景)

在你的专业领域（通信工程），Gamma 分布常用于：

- **信道建模：** 在某些无线通信场景下，信号幅度的平方可能服从 Gamma 分布。
    
- **噪声分析：** 对非高斯噪声的处理。
    
- **排队论：** 数据包在交换机中处理多个任务的总耗时。
    

---

## 相关条目

- [[指数分布]]
    
- [[卡方分布]]
    
- [[卷积公式的应用]]
    

---

