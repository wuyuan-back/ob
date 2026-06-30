---
created: 2026-06-30
tags:
  - 数字逻辑
  - 实验
  - verilog
  - PWM
  - 呼吸灯
---

# 实验 11：PWM 脉冲宽度调制

> 对应课程章节：50% 占空比设计

## 实验目标

- 掌握 PWM 信号生成原理
- 实现可调占空比 PWM
- 实现 LED 呼吸灯效果

## 原理

PWM 通过调节占空比控制输出功率：
- 占空比 = Ton / Tperiod
- 50% 占空比 = 方波

## 代码实现

### 可调占空比 PWM

```verilog
module pwm #(
    parameter W = 8
) (
    input             clk, rst_n,
    input  [W-1:0]   duty,      // 占空比设定值
    output reg        pwm_out
);
    reg [W-1:0] cnt;

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            cnt <= 0;
        else
            cnt <= cnt + 1'b1;
    end

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n)
            pwm_out <= 1'b0;
        else
            pwm_out <= (cnt < duty);
    end
endmodule
```

### LED 呼吸灯

```verilog
module breath_led (
    input clk, rst_n,
    output reg led
);
    reg [15:0] pwm_cnt;    // PWM 周期
    reg [15:0] duty;       // 当前占空比
    reg [7:0]  step;       // 渐变步进
    reg up;                // 方向：增/减

    always @(posedge clk or negedge rst_n) begin
        if (!rst_n) begin
            pwm_cnt <= 0;
            duty    <= 0;
            step    <= 0;
            up      <= 1;
        end else begin
            pwm_cnt <= pwm_cnt + 1'b1;

            // 每完成一个 PWM 周期更新一次 duty
            if (pwm_cnt == 16'd65535) begin
                step <= step + 1'b1;
                if (step == 8'd255) begin
                    step <= 0;
                    if (up) begin
                        if (duty == 16'd65535) up <= 0;
                        else duty <= duty + 256;
                    end else begin
                        if (duty == 0) up <= 1;
                        else duty <= duty - 256;
                    end
                end
            end

            led <= (pwm_cnt < duty);
        end
    end
endmodule
```

## 检查清单

- [ ] PWM 输出波形正确（示波器/仿真观察）
- [ ] 占空比可调（通过参数或按键）
- [ ] 呼吸灯渐亮渐暗平滑
- [ ] 50% 占空比方波生成

## 参考链接

- [[2026/大二小学期/verilog/数字逻辑]] — 实验总表
- [[2026/大二小学期/verilog/实验06_分频器]] — 基础时钟
