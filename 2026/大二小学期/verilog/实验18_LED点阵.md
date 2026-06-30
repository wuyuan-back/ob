---
created: 2026-06-30
tags:
  - 数字逻辑
  - 实验
  - verilog
  - LED点阵
  - 显示
---

# 实验 18：8×8 LED 点阵显示

> 对应课程章节：LED 显示控制

## 实验目标

- 掌握 LED 点阵的行列扫描原理
- 实现静态图案显示
- 实现动态滚动显示

## 原理

8×8 LED 点阵共有 64 个 LED，通过行/列扫描控制：

- **行扫描**：每次选中一行
- **列数据**：每行对应的 8 列数据（亮/灭）
- **分时复用**：快速扫描所有行（>60Hz 无闪烁）

```
行选 0 ──→  0  列数据: 01100110
行选 1 ──→  1  列数据: 10011001
  ...      ...
行选 7 ──→  7  列数据: 00111100
```

## 代码骨架

```verilog
module led_matrix (
    input  clk, rst_n,
    output reg [7:0] row,       // 行选（低电平有效）
    output reg [7:0] col_data   // 列数据
);
    reg [2:0] row_idx;
    reg [15:0] scan_cnt;

    // 行扫描（约 1kHz 扫描频率）
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            scan_cnt <= 0;
            row_idx  <= 0;
        end else if (scan_cnt == 16'd49999) begin
            scan_cnt <= 0;
            row_idx  <= row_idx + 1;
        end else begin
            scan_cnt <= scan_cnt + 1;
        end
    end

    // 行选
    always @(*) begin
        case (row_idx)
            3'd0: row = 8'b1111_1110;
            3'd1: row = 8'b1111_1101;
            3'd2: row = 8'b1111_1011;
            3'd3: row = 8'b1111_0111;
            3'd4: row = 8'b1110_1111;
            3'd5: row = 8'b1101_1111;
            3'd6: row = 8'b1011_1111;
            3'd7: row = 8'b0111_1111;
        endcase
    end

    // 列数据（ROM 存储图案）
    always @(*) begin
        case (row_idx)
            // 显示一个心形 ❤
            3'd0: col_data = 8'b01100110;
            3'd1: col_data = 8'b10011001;
            3'd2: col_data = 8'b10000001;
            3'd3: col_data = 8'b01000010;
            3'd4: col_data = 8'b00100100;
            3'd5: col_data = 8'b00011000;
            3'd6: col_data = 8'b00000000;
            3'd7: col_data = 8'b00000000;
        endcase
    end
endmodule
```

## 扩展：滚动显示

将多帧图案存入 ROM，通过计数器控制帧切换频率，实现文字滚动效果。

## 检查清单

- [ ] 点阵显示无闪烁（扫描频率 > 60Hz）
- [ ] 静态图案显示正确（字母、数字、符号）
- [ ] 多行扫描时亮度均匀
- [ ] 动态滚动流畅

## 参考链接

- [[2026/大二小学期/verilog/数字逻辑]] — 实验总表
- [[2026/大二小学期/verilog/实验08_数码管驱动]] — 分时复用原理类似
