---
created: 2026-06-30
tags:
  - verilog
  - FPGA
  - 学习日志
  - 实验
---

# Verilog Learning Log

> 从零开始的 Verilog 学习记录，每完成一个实验就打个勾

---

## 0x00 学习前自检

在开始之前，问问自己：

- [ ] 学过数字电路基础（与或非门、触发器、真值表）？
- [ ] 有 FPGA 开发板（或准备用仿真代替）？
- [ ] 装了 Vivado / Quartus 或至少 Icarus Verilog？
- [ ] 知道怎么看波形图？

如果全部打勾 -> 直接开始。

---

## 0x01 HDLBits 刷题日程

HDLBits 是最好的 Verilog 在线刷题站，浏览器里就能写、能仿真。

### 第一周：Getting Started + Verilog Language

- [ ] Step one - 热身
- [ ] Zero - 零基础入门
- [ ] Wire - wire 声明
- [ ] Notgate - 非门
- [ ] Andgate - 与门
- [ ] Norgate - 或非门
- [ ] Xorgate - 异或门
- [ ] Declaring wires
- [ ] 7458 chip

### 第二周：Vector + Module

- [ ] Vector0 - 向量基础
- [ ] Vector1 - 向量操作
- [ ] Module add - 模块例化
- [ ] Module shift - 移位模块
- [ ] Module csel - 选择器
- [ ] Module addsub - 加减法模块

### 第三周：Procedures + Always

- [ ] Always block
- [ ] Always if
- [ ] Always case
- [ ] Always if2 - 潜在 latch
- [ ] Blocking vs Non-blocking
- [ ] Latches - 锁存器

### 第四周：More Circuits

- [ ] Conditional - 条件运算符
- [ ] Reduction - 归约运算符
- [ ] Gates - 门电路综合
- [ ] Counters - 计数器
- [ ] FSM - 状态机


## 0x02 实验：流水灯

第一个能上板跑的程序。

### 原理

clk (50MHz) -> 分频器 -> 计数器 -> 移位寄存器 -> LED

### 代码



### 上板步骤

1. 新建 Vivado 项目，选对开发板型号
2. 创建设计文件，粘贴代码
3. 添加约束文件（管脚映射 XDC）
4. 综合 -> 实现 -> 生成比特流
5. 连接开发板 -> 下载程序

---

## 0x03 实验：数码管驱动

### 核心概念：分时复用

4 位数码管，每秒轮流点亮每一位（视觉暂留看起来全亮）。




## 0x02 实验：流水灯

第一个能上板跑的程序。

### 原理

clk (50MHz) -> 分频器 -> 计数器 -> 移位寄存器 -> LED

### 代码

```verilog
module led_flash (
    input        clk,
    input        rst_n,
    output reg [7:0] led
);

    reg [23:0] cnt;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            cnt <= 24'd0;
        else
            cnt <= cnt + 1'b1;
    end

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            led <= 8'b0000_0001;
        else if (cnt == 24'hffffff)
            led <= {led[6:0], led[7]};
    end

endmodule
```

### 上板步骤

1. 新建 Vivado 项目，选对开发板型号
2. 创建设计文件，粘贴代码
3. 添加约束文件 (XDC)
4. 综合 -> 实现 -> 生成比特流
5. 连接开发板 -> 下载程序

---

## 0x03 实验：数码管驱动

### 核心概念：分时复用

4 位数码管，每秒轮流点亮每一位（视觉暂留看起来全亮）。

```verilog
reg [16:0] scan_cnt;
reg [1:0]  digit_sel;

always @(posedge clk or negedge rst_n) begin
    if (!rst_n) begin
        scan_cnt  <= 17'd0;
        digit_sel <= 2'd0;
    end else if (scan_cnt == 17'd124999) begin
        scan_cnt  <= 17'd0;
        digit_sel <= digit_sel + 1'b1;
    end else begin
        scan_cnt <= scan_cnt + 1'b1;
    end
end

// 7 段译码表（共阴极）
always @(*) begin
    case (number)
        4'h0: seg = 7'b1000000;
        4'h1: seg = 7'b1111001;
        4'h2: seg = 7'b0100100;
        4'h3: seg = 7'b0110000;
        4'h4: seg = 7'b0011001;
        4'h5: seg = 7'b0010010;
        4'h6: seg = 7'b0000010;
        4'h7: seg = 7'b1111000;
        4'h8: seg = 7'b0000000;
        4'h9: seg = 7'b0010000;
        default: seg = 7'b1111111;
    endcase
end
```

---

## 0x04 实验：按键消抖

机械按键按下时产生 10-20ms 抖动，需要数字滤波。

```verilog
module debounce (
    input        clk,
    input        rst_n,
    input        key_in,
    output reg   key_out
);

    reg [19:0] cnt;
    reg key_reg1, key_reg2;

    // 两级同步器
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            key_reg1 <= 1'b1;
            key_reg2 <= 1'b1;
        end else begin
            key_reg1 <= key_in;
            key_reg2 <= key_reg1;
        end
    end

    // 20ms 计数器 (50MHz -> 1_000_000 周期)
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            cnt     <= 20'd0;
            key_out <= 1'b1;
        end else begin
            if (key_reg2 != key_out) begin
                if (cnt == 20'd999_999) begin
                    cnt     <= 20'd0;
                    key_out <= key_reg2;
                end else begin
                    cnt <= cnt + 1'b1;
                end
            end else begin
                cnt <= 20'd0;
            end
        end
    end

endmodule
```

---

## 0x05 踩坑记录

| # | 问题 | 原因 | 解决 |
|---|------|------|------|
| 1 | 仿真波形没变化 | 忘了加时钟激励 | 加 always #10 clk = ~clk |
| 2 | 综合报错 multiple drivers | 同一 reg 在两个 always 赋值 | 一个信号只能在一个 always 块驱动 |
| 3 | LED 不亮 | 没加约束文件 | 添加 XDC 管脚映射 |
| 4 | 按键不灵敏 | 没消抖 | 加 20ms 延时采样 |
| 5 | Latch inferred | if 缺 else / case 没写全 | 补全所有分支 |
| 6 | 计数器值不对 | 用了 = 而不是 <= | 时序逻辑改 <= |
| 7 | 模块例化 port 不匹配 | 端口名写错 | 检查对应关系 |
| 8 | 上板跑太快看不清 | 分频数不够 | 用 24-26 位计数器 |

---

## 0x06 常用命令速记

### Icarus Verilog + GTKWave

```bash
iverilog -o tb.vvp tb.v design.v
vvp tb.vvp
gtkwave wave.vcd
```

### Vivado TCL

```tcl
launch_runs synth_1
wait_on_run synth_1
launch_runs impl_1
wait_on_run impl_1
write_bitstream -force project.bit
```

---

## 0x07 学习检查清单

### 基础关

- [ ] 能写出完整模块 (module .. endmodule)
- [ ] 理解 wire 和 reg 的区别
- [ ] 会用 assign 描述组合逻辑
- [ ] 会用 always @(*) 描述组合逻辑
- [ ] 会用 always @(posedge clk) 描述时序逻辑
- [ ] 能解释 = 和 <= 的区别

### 中级关

- [ ] 能写出三段式状态机
- [ ] 会写 testbench 并看波形
- [ ] 能例化子模块
- [ ] 会用 parameter 参数化设计
- [ ] 知道如何避免 latch
- [ ] 能实现 UART 收发

---

## 0x08 项目创意

从易到难：

1. 流水灯
2. 数字钟 - 计数器 + 数码管
3. 简单电子琴 - 按键 + 分频 + 蜂鸣器
4. 矩阵键盘扫描
5. VGA 彩条输出
6. UART 环路测试
7. SPI Flash 读写
8. 简单 RISC-V CPU（终极挑战）

---

## 0x09 资源快链

- [[2026/大二小学期/verilog/verilog]] - 语法速查手册
- HDLBits - 刷题网站
- EDA Playground - 在线仿真
- OpenCores - 开源 IP 核
- Nandland - FPGA 入门教程

---

> 每写一行代码，都问自己：综合出来是什么电路？
