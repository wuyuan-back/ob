---
created: 2026-06-30
tags:
  - 数字逻辑
  - 实验
  - verilog
  - BCD
  - 计数器
---

# 实验 15：0~99999 BCD 计数器

> 对应课程章节：BCD 计数器 0~99999（12bit / 17bit 编码）

## 实验目标

- 设计 5 位 BCD 计数器
- 理解 12bit 与 17bit 两种编码方式
- 数码管显示全部 5 位

## 原理

### 编码对比

| 位数 | 编码方式 | 示例 99999 |
|------|---------|-----------|
| 12bit | 3×4bit BCD | `1010 0000 0111` → 实际是 BCD 编码的 3 位 |
| 17bit | 5×4bit BCD - 3bit 压缩 | `11000 011010 011111` |
| 20bit | 5×4bit BCD（标准） | `1001 1001 1001 1001 1001` |

## 代码实现

### 5 位 BCD 计数器

```verilog
module bcd_counter_5digit (
    input  clk, rst_n, en,
    output reg [19:0] bcd,     // 5 × 4bit BCD
    output carry
);
    // 每 4bit 为一位 BCD
    wire [3:0] digit0 = bcd[3:0];
    wire [3:0] digit1 = bcd[7:4];
    wire [3:0] digit2 = bcd[11:8];
    wire [3:0] digit3 = bcd[15:12];
    wire [3:0] digit4 = bcd[19:16];

    assign carry = (bcd == 20'h99999) & en;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            bcd <= 0;
        else if (en) begin
            if (bcd == 20'h99999)
                bcd <= 0;
            else begin
                if (digit0 != 9)
                    bcd[3:0] <= digit0 + 1;
                else begin
                    bcd[3:0] <= 0;
                    if (digit1 != 9)
                        bcd[7:4] <= digit1 + 1;
                    else begin
                        bcd[7:4] <= 0;
                        // 依次进位...
                    end
                end
            end
        end
    end
endmodule
```

## 检查清单

- [ ] 0 → 99999 正确计数
- [ ] 进位信号在 99999 时拉高
- [ ] 5 位数码管稳定显示
- [ ] 理解 12bit/17bit/20bit 编码差异

## 参考链接

- [[2026/大二小学期/verilog/数字逻辑]] — 实验总表
- [[2026/大二小学期/verilog/实验08_数码管驱动]] — 显示
- [[2026/大二小学期/verilog/实验10_BinBCD]] — BCD 转换
