---
created: 2026-06-30
tags:
  - 数字逻辑
  - 实验
  - verilog
  - BCD
  - BinBCD
---

# 实验 10：Binary to BCD 转换

> 对应课程章节：BinBCD（34位 / 38位二进制转 BCD）

## 实验目标

- 掌握 Double Dabble 算法
- 实现参数化位宽的二进制转 BCD
- 结合数码管显示转换结果

## 原理

### Double Dabble 算法

核心思想：逐位左移，每移完一位检查 BCD 位是否 ≥5，如果是则加 3 调整。

```
输入 8'b11111111（255）
移位过程（共 8 次移位，每次移位后检查调整）：
  初始: z = 0000_0000_0000_0000_0000_0000_11111111
        └──100位──┘──10位──┘──个位──┘
  最终: z = 0000_0000_0010_0101_0101 (BCD: 2 5 5)
```

## 代码实现

```verilog
module binbcd #(
    parameter BITS = 8,
    parameter DIGITS = 3
) (
    input  [BITS-1:0] b,
    output reg [DIGITS*4-1:0] p
);
    reg [BITS+DIGITS*4-1:0] z;
    integer i;

    always @(*) begin
        z = 0;
        z[BITS-1:0] = b;

        repeat (BITS) begin
            // 每 4 位为一组 BCD 码，≥5 则加 3
            if (z[11:8] > 4) z[11:8] = z[11:8] + 3;
            if (z[15:12] > 4) z[15:12] = z[15:12] + 3;
            z = {z[z_WIDTH-2:0], 1'b0};
        end

        p = z[DIGITS*4+1:2];
    end
endmodule
```

## 检查清单

- [ ] 8 位二进制 → 3 位 BCD 正确（0~255）
- [ ] 测试边界值（0, 9, 10, 99, 100, 255）
- [ ] 参数化位宽可配置
- [ ] 结合数码管显示转换结果

## 参考链接

- [[2026/大二小学期/verilog/数字逻辑]] — 实验总表
- [[2026/大二小学期/verilog/实验08_数码管驱动]] — 显示配合
