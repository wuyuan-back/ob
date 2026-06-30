---
created: 2026-06-30
tags:
  - 数字逻辑
  - 实验
  - verilog
  - FIFO
  - Block RAM
  - IP核
---

# 实验 17：FIFO 设计（Block RAM）

> 对应课程章节：FIFO（First Input First Output）+ IP Block RAM Generator

## 实验目标

- 理解 FIFO 的工作原理
- 实现同步 FIFO
- 学会调用 Xilinx Block RAM Generator IP 核

## 原理

FIFO（First In First Out）是一种先进先出的数据缓冲器。

### 同步 FIFO 结构

```
写使能 ──→┌───────┐
数据入 ──→│ FIFO  │──→ 数据出
时钟   ──→│       │──→ 空标志
复位   ──→│       │──→ 满标志
          └───────┘
```

## 代码实现

### 同步 FIFO

```verilog
module sync_fifo #(
    parameter DATA_WIDTH = 8,
    parameter ADDR_WIDTH = 4,
    parameter DEPTH = 16
) (
    input                     clk, rst_n,
    input                     wr_en,
    input  [DATA_WIDTH-1:0]   wr_data,
    input                     rd_en,
    output reg [DATA_WIDTH-1:0] rd_data,
    output                    empty,
    output                    full
);
    reg [DATA_WIDTH-1:0] mem [0:DEPTH-1];
    reg [ADDR_WIDTH-1:0] wr_ptr, rd_ptr;
    reg [ADDR_WIDTH:0]   fifo_cnt;  // 多一位判断空/满

    // 写操作
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            wr_ptr <= 0;
        else if (wr_en && !full) begin
            mem[wr_ptr] <= wr_data;
            wr_ptr <= wr_ptr + 1;
        end
    end

    // 读操作
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            rd_ptr  <= 0;
            rd_data <= 0;
        end else if (rd_en && !empty) begin
            rd_data <= mem[rd_ptr];
            rd_ptr <= rd_ptr + 1;
        end
    end

    // 计数
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            fifo_cnt <= 0;
        else begin
            case ({wr_en && !full, rd_en && !empty})
                2'b10: fifo_cnt <= fifo_cnt + 1;
                2'b01: fifo_cnt <= fifo_cnt - 1;
                default: fifo_cnt <= fifo_cnt;
            endcase
        end
    end

    assign empty = (fifo_cnt == 0);
    assign full  = (fifo_cnt == DEPTH);
endmodule
```

### 异步 FIFO（跨时钟域）

异步 FIFO 需要：
1. 双端口 RAM
2. 格雷码指针（跨时钟域同步）
3. 空/满标志生成

> 完整异步 FIFO 实现较复杂，建议先掌握同步 FIFO，再参考 Xilinx 官方代码。

## IP 核方式

Vivado 中可通过 **IP Catalog → FIFO Generator** 直接生成 FIFO IP 核，配置图形化界面：

1. 选择 FIFO 类型（同步/异步）
2. 配置数据宽度和深度
3. 选择标志类型（空/满/almost 空/满）
4. 选择实现方式（Block RAM / Distributed RAM）

## 检查清单

- [ ] 同步 FIFO 写入/读取功能正确
- [ ] 空标志在 FIFO 空时拉高
- [ ] 满标志在 FIFO 满时拉高
- [ ] 仿真验证写入后读出数据一致
- [ ] 异步 FIFO 跨时钟域测试
- [ ] 用 Block RAM Generator 生成 IP 核

## 参考链接

- [[2026/大二小学期/verilog/数字逻辑]] — 实验总表
- [[2026/大二小学期/verilog/实验04_DFF与寄存器]] — 寄存器基础
