---
created: 2026-06-30
tags:
  - verilog
  - FPGA
  - 数字电路
  - 学习指南
---

# Verilog 学习指南

## 一、Verilog 概述

### 什么是 Verilog？

Verilog HDL（Hardware Description Language）是一种**硬件描述语言**，用于描述数字电路的结构和行为。它与 VHDL 并列为两大主流 HDL，在 **FPGA 开发** 和 **ASIC 设计** 中广泛应用。

### Verilog vs 软件编程语言

| 维度 | C/Python（软件） | Verilog（硬件） |
|------|-----------------|-----------------|
| **执行方式** | 顺序执行 | **并行执行**（所有 always 块同时工作） |
| **时间概念** | 语句一条接一条 | 有 **延迟/时钟** 概念，信号传播需时间 |
| **变量类型** | 变量/数组 | wire（连线）、reg（寄存器） |
| **核心思想** | 算法 + 数据结构 | **并行 + 时序 + 连线** |

> **核心思维转变**：写 Verilog 不是在"编程"，而是在"画电路图"——每个 always 块就是一个硬件模块，综合工具会把它映射成真实的逻辑门和触发器。

---

## 二、基础语法速查

### 2.1 模块结构

```verilog
module module_name (
    input  wire       clk,     // 时钟
    input  wire       rst_n,   // 复位（低有效）
    input  wire [3:0] a,       // 4 位输入
    output reg  [3:0] y        // 4 位输出
);
    // 功能描述
endmodule
```

### 2.2 数据类型

| 类型 | 用法 |
|------|------|
| wire | 连线型，用于 assign 赋值、模块端口连接 |
| reg | 寄存器型，用于 always 块内赋值 |
| integer | 32 位有符号整数，常用于 for 循环 |
| parameter | 常量参数，便于模块复用 |

### 2.3 数值表示

```
4'b1010    // 4 位二进制 1010
8'hFF      // 8 位十六进制 FF
4'd10      // 4 位十进制 10
8'bz       // 高阻态
8'bx       // 未知态
```

### 2.4 常用运算符

```
// 按位运算
& | ~ ^    // AND, OR, NOT, XOR

// 逻辑运算
&& || !    // 逻辑与、或、非

// 算术运算
+ - * / %  // 加减乘除取模

// 关系运算
== != < > <= >=

// 移位运算
<< >>      // 左移、右移（逻辑移位）

// 拼接与复制
{3'b101, 2'b00}     // 拼接 -> 5'b10100
{4{1'b1}}           // 复制 -> 4'b1111
```

---

## 三、组合逻辑

组合逻辑的输出**只取决于当前输入**，没有存储功能。

### 3.1 assign 连续赋值

```verilog
// 全加器
module full_adder (
    input  a, b, cin,
    output sum, cout
);
    assign sum  = a ^ b ^ cin;
    assign cout = (a & b) | (a & cin) | (b & cin);
endmodule
```

### 3.2 always @(*) 组合逻辑块

```verilog
// 4 选 1 多路选择器
module mux4 (
    input  [1:0] sel,
    input  [3:0] d0, d1, d2, d3,
    output reg   y
);
    always @(*) begin
        case (sel)
            2'b00:   y = d0;
            2'b01:   y = d1;
            2'b10:   y = d2;
            2'b11:   y = d3;
            default: y = 1'bx;
        endcase
    end
endmodule
```

### 3.3 三目运算符

```verilog
assign y = sel ? a : b;   // 2 选 1 MUX 的简写
```

---

## 四、时序逻辑

时序逻辑的输出**依赖当前输入和历史状态**，需要时钟驱动。

### 4.1 D 触发器基础

```verilog
// 带异步复位的 D 触发器
always @(posedge clk or negedge rst_n) begin
    if (!rst_n)
        q <= 1'b0;
    else
        q <= d;
end
```

### 4.2 阻塞赋值 `=` vs 非阻塞赋值 `<=`

| 赋值方式 | 含义 | 使用场景 |
|----------|------|----------|
| `=`（阻塞） | 立即赋值，顺序执行 | **组合逻辑** always @(*) |
| `<=`（非阻塞） | 并行赋值，块结束后同时更新 | **时序逻辑** always @(posedge clk) |

> **黄金法则**：组合逻辑用 =，时序逻辑用 <=。混用会导致仿真与综合结果不一致。

### 4.3 计数器

```verilog
// 模 10 计数器（0-9）
module counter_10 (
    input            clk,
    input            rst_n,
    output reg [3:0] cnt
);
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            cnt <= 4'd0;
        else if (cnt == 4'd9)
            cnt <= 4'd0;
        else
            cnt <= cnt + 1'b1;
    end
endmodule
```

### 4.4 分频器

```verilog
// 偶数分频：50MHz -> 1Hz（50_000_000 分频）
module clk_div #(
    parameter DIV_N = 50_000_000
) (
    input  clk_in,
    input  rst_n,
    output reg clk_out
);
    integer cnt;

    always @(posedge clk_in or negedge rst_n) begin
        if (!rst_n) begin
            cnt     <= 0;
            clk_out <= 1'b0;
        end else begin
            if (cnt == DIV_N/2 - 1) begin
                clk_out <= ~clk_out;
                cnt     <= 0;
            end else begin
                cnt <= cnt + 1;
            end
        end
    end
endmodule
```

### 4.5 移位寄存器

```verilog
// 8 位左移寄存器
module shift_reg (
    input            clk,
    input            rst_n,
    input            din,
    output reg [7:0] q
);
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            q <= 8'd0;
        else
            q <= {q[6:0], din};  // 左移，新数据进入最低位
    end
endmodule
```

---

## 五、状态机（FSM）

### 5.1 三段式状态机（推荐写法）

```verilog
module fsm_example (
    input        clk,
    input        rst_n,
    input        start,
    output reg   done
);

    localparam IDLE = 2'b00;
    localparam WORK = 2'b01;
    localparam DONE = 2'b10;

    reg [1:0] state, next_state;

    // 第一段：状态转移（时序逻辑）
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            state <= IDLE;
        else
            state <= next_state;
    end

    // 第二段：次态逻辑（组合逻辑）
    always @(*) begin
        case (state)
            IDLE:   next_state = start ? WORK  : IDLE;
            WORK:   next_state = DONE;
            DONE:   next_state = IDLE;
            default: next_state = IDLE;
        endcase
    end

    // 第三段：输出逻辑（时序逻辑，消除毛刺）
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            done <= 1'b0;
        else begin
            case (next_state)
                DONE: done <= 1'b1;
                default: done <= 1'b0;
            endcase
        end
    end

endmodule
```

### 5.2 状态机设计要点

1. **三段式结构**：状态转移 + 次态逻辑 + 输出逻辑
2. **状态编码**：二进制 / 格雷码 / 独热码 One-hot（FPGA 推荐）
3. **避免 latch**：组合逻辑中 case 要写全，或加 default

---

## 六、仿真与测试

### 6.1 Testbench 结构

```verilog
`timescale 1ns / 1ps

module tb_counter;

    reg        clk;
    reg        rst_n;
    wire [3:0] cnt;

    // 实例化待测模块
    counter_10 uut (
        .clk  (clk),
        .rst_n(rst_n),
        .cnt  (cnt)
    );

    // 时钟生成：周期 20ns（50MHz）
    always #10 clk = ~clk;

    // 测试激励
    initial begin
        clk   = 0;
        rst_n = 0;
        #20;
        rst_n = 1;
        #200;
        $finish;
    end

    // 波形输出
    initial begin
        $dumpfile("wave.vcd");
        $dumpvars(0, tb_counter);
    end

endmodule
```

### 6.2 常用系统函数

```verilog
$display("a = %d, b = %h", a, b);  // 打印
$monitor("time=%0t a=%d", $time, a); // 持续监控
$stop;                              // 暂停仿真
$finish;                            // 结束仿真
$readmemh("data.hex", mem);         // 读内存初始化文件
```

---

## 七、综合与实现要点

### 7.1 可综合 vs 不可综合

| 可综合 | 不可综合 |
|--------|----------|
| assign | initial（除测试用） |
| always @(posedge clk) | #10 延时 |
| always @(*) | $display, $monitor |
| case, if-else | wait, fork-join |
| 有限循环 for | while 循环 |

### 7.2 时序约束

```tcl
# XDC 约束示例（Vivado）
create_clock -period 20.000 [get_ports clk]
set_input_delay -clock clk -max 5 [get_ports din]
set_output_delay -clock clk -max 5 [get_ports dout]
```

---

## 八、常见陷阱与最佳实践

### 常见错误

1. **组合逻辑中产生 latch** — if 缺少 else，case 缺少 default
2. **时序逻辑用阻塞赋值 =** — 应该用 <=
3. **敏感列表不全** — 用 always @(*) 替代手动列表
4. **一个信号在多个 always 块赋值** — 综合报错 "multiple drivers"

### 最佳实践

- 使用 always @(*) 自动包含所有敏感信号
- 参数化设计，用 parameter 提高复用性
- 三段式状态机，逻辑清晰无毛刺
- case 语句加 default 避免 latch
- 充分仿真：先行为仿真，再门级仿真，最后上板

---

## 九、学习路线

```
第一阶段：基础语法
  模块结构、wire/reg、运算符
  组合逻辑：assign、always @(*)
  时序逻辑：always @(posedge clk)、<= 赋值
  练习：加法器、计数器、分频器

第二阶段：常用模块
  状态机（三段式）
  移位寄存器、串并转换
  按键消抖
  仿真验证
  练习：UART 发送、流水灯、数码管驱动

第三阶段：接口与通信
  UART、SPI、I2C
  跨时钟域处理
  时序约束入门

第四阶段：进阶
  流水线设计
  SoC 设计入门
  练习：RISC-V 简单处理器
```

---

## 十、推荐资源

### 书籍
- 《Verilog 数字系统设计教程》—— 夏宇闻
- 《Digital Design and Computer Architecture》—— Harris

### 开发工具
- **Vivado**（Xilinx FPGA，大学最常用）
- **Quartus Prime**（Intel/Altera FPGA）
- **ModelSim / QuestaSim**（仿真）
- **Icarus Verilog + GTKWave**（免费开源方案）

### 在线资源
- [HDLBits](https://hdlbits.01xz.net/) —— 刷题网站
- [EDA Playground](https://www.edaplayground.com/) —— 在线仿真
- [ChipVerify](https://www.chipverify.com/verilog) —— Verilog 教程

---

> **记住**：Verilog 不是编程语言，是"画电路图"的语言。始终问自己——我写的这段代码会综合成什么电路？
