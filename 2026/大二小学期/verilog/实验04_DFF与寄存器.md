---
created: 2026-06-30
tags:
  - 数字逻辑
  - 实验
  - verilog
  - 时序逻辑
---

# 实验 04：D 触发器与寄存器

## 实验目标

- 掌握 D 触发器的 Verilog 描述
- 理解阻塞与非阻塞赋值的区别
- 实现移位寄存器

## 代码实现

### 带异步复位的 D 触发器

```verilog
module dff (
    input  clk, rst_n, d,
    output reg q
);
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            q <= 1'b0;
        else
            q <= d;
    end
endmodule
```

### 8 位移位寄存器

```verilog
module shift_reg (
    input            clk, rst_n,
    input            din,
    output reg [7:0] q
);
    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            q <= 8'd0;
        else
            q <= {q[6:0], din};   // 左移，新数据进入 LSB
    end
endmodule
```

## ⚠️ 阻塞 vs 非阻塞赋值对比

```verilog
// 非阻塞 <= （正确，并行赋值）
always @(posedge clk) begin
    a <= b;
    c <= a;  // 取的是赋值前 a 的旧值
end
// 等价于两个寄存器级联

// 阻塞 = （错误用法！）
always @(posedge clk) begin
    a = b;
    c = a;   // 取的是 a 的新值（= b）
end
// 综合出的是两个并行寄存器，和仿真行为不一致
```

## 检查清单

- [ ] D 触发器复位功能正确
- [ ] 移位寄存器功能正确
- [ ] 用仿真对比 `=` 与 `<=` 的波形差异
- [ ] 理解为什么时序逻辑必须用 `<=`

## 参考链接

- [[2026/大二小学期/verilog/数字逻辑]] — 实验总表
- [[2026/大二小学期/verilog/实验05_计数器]] — 下一实验
