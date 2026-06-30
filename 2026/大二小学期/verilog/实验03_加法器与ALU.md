---
created: 2026-06-30
tags:
  - 数字逻辑
  - 实验
  - verilog
  - 组合逻辑
  - ALU
---

# 实验 03：加法器与算术逻辑单元

## 实验目标

- 掌握全加器原理与实现
- 对比行波进位与超前进位
- 设计简单 ALU

## 代码实现

### 全加器

```verilog
module full_adder (
    input  a, b, cin,
    output sum, cout
);
    assign sum  = a ^ b ^ cin;
    assign cout = (a & b) | (a & cin) | (b & cin);
endmodule
```

### 4 位行波进位加法器

```verilog
module adder_4bit (
    input  [3:0] a, b,
    input        cin,
    output [3:0] sum,
    output       cout
);
    wire c1, c2, c3;
    full_adder u0 (.a(a[0]), .b(b[0]), .cin(cin),  .sum(sum[0]), .cout(c1));
    full_adder u1 (.a(a[1]), .b(b[1]), .cin(c1),   .sum(sum[1]), .cout(c2));
    full_adder u2 (.a(a[2]), .b(b[2]), .cin(c2),   .sum(sum[2]), .cout(c3));
    full_adder u3 (.a(a[3]), .b(b[3]), .cin(c3),   .sum(sum[3]), .cout(cout));
endmodule
```

## 检查清单

- [ ] 全加器真值表正确
- [ ] 4 位加法器功能正确
- [ ] ALU 支持加、减、与、或
- [ ] 仿真覆盖边界（进位溢出）

## 参考链接

- [[2026/大二小学期/verilog/数字逻辑]] — 实验总表
- [[2026/大二小学期/verilog/实验02_多路选择器与译码器]]
