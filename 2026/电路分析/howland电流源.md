这就是典型的 **Howland 电流源（Howland Current Pump）** 标准电路图及其核心原理。

 [![Howland current pump circuit diagram labeled with resistors and opamp, AI generated](https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcQiIT2Mr-hWLMmACrM7_4yD8fN0AHCMPvG4ueOOqQLhFfKSBWsIVW3DOjuUz5Vi) Opens in a new window](https://www.allaboutcircuits.com/technical-articles/the-howland-current-pump/) [![](https://encrypted-tbn1.gstatic.com/favicon-tbn?q=tbn:ANd9GcR9Qdwhy2KOJkvxeW8UZQohCd1GNr0xIU38i-yGxqP9uv4sivsBqk3MoeTY_zAHQbtdkSC31XM4Ru9RWYIHHf00Q_FKRlr7If2yGD4eDzEiGo50)www.allaboutcircuits.com](https://www.allaboutcircuits.com/technical-articles/the-howland-current-pump/)

为了方便你理解和设计，我们可以对照图中的符号（通常标注为 $R_1, R_2, R_3, R_4$）来总结它的关键点：
![[20260422_215759.png]]
### 1. 电路构成

- **输入端 ($V_1, V_2$)：** 通常 $V_2$ 接信号电压，$V_1$ 接地（或者反过来，决定输出电流的方向）。
    
- **正负反馈：** 它同时包含了负反馈（通过 $R_2$）和正反馈（通过 $R_4$ 到 $R_3$）。
    
- **负载 ($R_L$)：** 负载一端接在输出节点，另一端直接接地。
    

### 2. 设计公式

要让它真正成为一个理想的电流源，必须满足以下**电阻匹配比例**：

$$\frac{R_2}{R_1} = \frac{R_4 + R_{source}}{R_3}$$

_(通常简化为 $\frac{R_2}{R_1} = \frac{R_4}{R_3}$)_

此时，输出电流 $I_L$ 的表达式为：

$$I_L = \frac{V_2 - V_1}{R_1 \cdot \frac{R_4}{R_2}} = \frac{V_2 - V_1}{R_3 \cdot \frac{R_1}{R_2}}$$

**结论：** 电流 $I_L$ 仅取决于输入电压差和电阻值，与负载 $R_L$ 的阻值完全无关。

### 3. 应用实例（以你刚才的题目为例）

在你的那道练习题中：

- $R_1 = 4\text{k}\Omega$，$R_2 = 2\text{k}\Omega$
    
- $R_3 = 6\text{k}\Omega$，$R_4 = R$
    
- 根据比例：$\frac{2}{4} = \frac{R}{6} \implies R = 3\text{k}\Omega$
    
- 最终电流：$I_o = -\frac{U_i}{R_1 \cdot (R/R_2)} = -\frac{U_i}{4 \cdot (3/2)} = -\frac{U_i}{6} \text{ mA}$
    

### 4. 实验与仿真小贴士

- **电阻精度：** 在实际搭电路（如电赛）时，建议使用 **0.1% 精度**的千分电阻。如果电阻不匹配，输出电流会随着负载的变化而“漂移”。
    
- **单电源 vs 双电源：** 这种电路通常需要**双电源供电**（如 $\pm 15\text{V}$），否则输出电流在接近 0V 附近会产生严重的非线性失真。
    
- **自激振荡：** 如果发现输出波形有毛刺或高频抖动，可以在反馈电阻 $R_2$ 上并联一个几 pF 的微调电容。
    

这个电路在**脑机接口 (BCI)** 的电极驱动、微弱生物电流模拟等科研项目中非常常用。如果你在做相关的电路设计，可以尝试在 LTspice 或 Multisim 中搭建这个模型，观察改变 $R_L$ 时电流的稳定性。