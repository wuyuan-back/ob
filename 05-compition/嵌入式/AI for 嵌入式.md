提示词篇
好的，我来为你设计一个更丰富的蓝桥杯嵌入式赛题提示词模板，并说明如何将其封装为Claude Code的Skill。

---

## 一、蓝桥杯嵌入式赛题特点分析

蓝桥杯嵌入式设计与开发科目有以下特点：

- **硬件平台**：四梯嵌入式竞赛实训平台，MCU型号为**STM32G431RBT6**
- **竞赛时长**：省赛/决赛均为**5小时**
- **试题构成**：客观题（约30%）+ 基于硬件平台的程序设计与调试（约70%）
- **核心考点**：GPIO、定时器、ADC、USART、EXTI中断、I2C（如24C02）、PWM、输入捕获等

---

## 二、针对蓝桥杯赛题的增强提示词模板

### 模板1：基础功能实现（适用于单模块任务）

```markdown
# 角色
你是一位资深的STM32嵌入式工程师，曾多次指导选手参加蓝桥杯嵌入式设计与开发竞赛并获奖。

# 项目上下文
- 芯片型号：STM32G431RBT6
- 开发环境：STM32CubeIDE
- 使用的库：STM32 HAL库
- 工程由STM32CubeMX生成，所有外设已通过CubeMX完成初始化配置
- 用户代码必须写在由 `USER CODE BEGIN` 和 `USER CODE END` 注释标记的区域内
- 竞赛平台：四梯嵌入式竞赛实训平台

# 任务目标
【在此处描述具体功能，例如：】
使用TIM2产生周期为1秒、占空比为50%的PWM波形，通过PA0引脚输出，并用按键（PC13）控制PWM的启动与停止。

# 输出要求与约束
1. 必须使用HAL库API（如 `HAL_TIM_PWM_Start`, `HAL_TIM_PWM_Stop`, `HAL_GPIO_ReadPin` 等）
2. 代码必须放置在正确的 `USER CODE` 区域内
3. 必须包含中断处理（如按键采用EXTI中断方式）
4. 提供实现思路说明 + 完整代码 + 关键参数计算过程
5. 添加清晰的中文注释

# 蓝桥杯评分注意事项
- 注意代码的健壮性，防止按键抖动
- 注意时钟配置的准确性
- 代码风格需整洁规范
```

### 模板2：综合题模板（适用于多模块联调，对标正式赛题）

```markdown
# 角色
你是一位蓝桥杯嵌入式竞赛资深指导老师，熟悉竞赛评分标准和常见失分点。

# 项目上下文
- 芯片型号：STM32G431RBT6
- 开发环境：STM32CubeIDE
- 使用的库：STM32 HAL库
- 工程由STM32CubeMX生成
- 用户代码必须写在 `USER CODE BEGIN/END` 区域内

# 硬件资源映射（请根据实际赛题调整）
| 功能 | 引脚 | 外设 |
|------|------|------|
| LED1 | PA0 | GPIO Output |
| LED2 | PA1 | GPIO Output |
| 按键1 | PC13 | EXTI |
| 按键2 | PB0 | EXTI |
| PWM输出 | PA6 | TIM3_CH1 |
| ADC采集 | PA4 | ADC1_IN4 |
| 串口通信 | PA9/PA10 | USART1 |
| EEPROM | PB6/PB7 | I2C1 (24C02) |

# 任务目标
【综合题描述，例如：】
设计一个智能控制器，实现以下功能：
1. 通过ADC采集电位器电压（0-3.3V），转换为0-100%的占空比
2. 通过PWM输出控制LED亮度
3. 按键1切换模式（自动/手动），按键2在手动模式下调节亮度步进
4. 通过串口每秒上报当前模式、占空比和ADC值
5. 掉电后通过24C02保存当前模式

# 输出要求与约束
1. 全部使用HAL库API
2. 代码按模块组织：主循环逻辑、中断服务、外设驱动
3. 必须标注每个代码段对应的 `USER CODE` 区域
4. 提供：系统架构说明 → 外设配置参数 → 完整代码 → 测试要点
5. 特别标注蓝桥杯常见失分点（如：未处理按键抖动、未考虑边界条件等）

# 蓝桥杯评分对标
- 功能完整性（60%）：所有功能正确实现
- 代码规范性（20%）：注释完整、命名规范、结构清晰
- 健壮性（20%）：异常处理、边界条件、防抖处理
```

### 模板3：快速解题模板（适用于比赛时间紧张时）

```markdown
# 紧急任务：蓝桥杯赛题快速实现

## 约束（必须遵守）
- 芯片：STM32G431RBT6
- 库：HAL库
- IDE：STM32CubeIDE
- 代码放在 `USER CODE` 区域内
- 不能修改CubeMX生成的初始化代码

## 功能需求
【简要描述，2-3句话】

## 输出格式
请按以下格式输出：
1. 实现思路（3-5行）
2. 需要修改的 `USER CODE` 区域及代码
3. 关键参数配置（定时器周期、分频系数等）
4. 编译和测试注意事项

## 特别注意
- 代码必须可直接复制使用
- 不要添加额外的库或复杂抽象
- 保持代码简洁，便于快速调试
```

---

## 三、封装为Claude Code Skill

### 3.1 Skill 是什么

Skill是Claude Code的一种扩展机制，本质是一个包含`SKILL.md`文件的目录，用于为Claude提供特定领域的**指令、工作流程和参考材料**。Skill的核心优势是**按需加载**——Claude只在需要时才会读取完整的Skill内容，不会占用日常对话的上下文。

Skill与`CLAUDE.md`的区别在于：
- `CLAUDE.md`：每次对话都自动加载的项目守则
- **Skill**：需要时才调用的操作卡，适合特定场景

### 3.2 创建蓝桥杯嵌入式Skill

**步骤1：创建Skill目录**

在项目根目录或用户目录下创建：

```bash
# 项目级Skill（推荐，与比赛项目绑定）
mkdir -p .claude/skills/lanqiao-embedded/

# 或用户级Skill（全局可用）
mkdir -p ~/.claude/skills/lanqiao-embedded/
```

**步骤2：编写SKILL.md文件**

在`.claude/skills/lanqiao-embedded/SKILL.md`中写入：

```markdown
---
name: lanqiao-embedded
description: 蓝桥杯嵌入式设计与开发竞赛辅助技能。当用户提到蓝桥杯、嵌入式竞赛、STM32G431、四梯平台、省赛/国赛题目时自动激活。提供HAL库代码生成、外设配置、综合题解答和评分标准对照。
---

# 蓝桥杯嵌入式设计与开发 Skill

## 触发条件
当用户请求涉及以下任一关键词时，此Skill应被激活：
- "蓝桥杯"、"嵌入式竞赛"、"省赛"、"国赛"
- "STM32G431"、"四梯平台"、"竞赛实训平台"
- "PWM"、"ADC"、"24C02"、"输入捕获"、"串口"

## 硬件平台规范
- MCU: STM32G431RBT6
- 开发环境: STM32CubeIDE
- 库: HAL库（禁止使用LL库或寄存器操作，除非用户明确要求）
- 代码必须放置在 `USER CODE BEGIN/END` 区域内

## 核心外设参考实现

### 1. GPIO + EXTI按键
```c
// 按键初始化（CubeMX已生成，只需编写回调）
void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin) {
    if(GPIO_Pin == KEY1_Pin) {
        // 防抖处理：建议使用定时器延时或状态机
        HAL_Delay(20);
        if(HAL_GPIO_ReadPin(KEY1_GPIO_Port, KEY1_Pin) == GPIO_PIN_RESET) {
            // 按键按下处理逻辑
        }
    }
}
```

### 2. PWM输出（TIM）
```c
// 启动PWM
HAL_TIM_PWM_Start(&htimX, TIM_CHANNEL_Y);
// 修改占空比
__HAL_TIM_SET_COMPARE(&htimX, TIM_CHANNEL_Y, pulse_value);
// pulse_value范围: 0 ~ TIM_X->ARR
```

### 3. ADC单通道采集
```c
HAL_ADC_Start(&hadcX);
if(HAL_ADC_PollForConversion(&hadcX, 100) == HAL_OK) {
    uint32_t adc_value = HAL_ADC_GetValue(&hadcX);
    // adc_value范围: 0 ~ 4095 (12位)
}
```

### 4. 串口发送
```c
char buffer[64];
sprintf(buffer, "Value: %d\r\n", value);
HAL_UART_Transmit(&huartX, (uint8_t*)buffer, strlen(buffer), 100);
```

### 5. I2C (24C02 EEPROM)
```c
// 写单字节
HAL_I2C_Mem_Write(&hi2cX, 0xA0, addr, I2C_MEMADD_SIZE_8BIT, &data, 1, 100);
// 读单字节
HAL_I2C_Mem_Read(&hi2cX, 0xA0, addr, I2C_MEMADD_SIZE_8BIT, &data, 1, 100);
```

## 输出规范

### 对于单功能题，输出格式：
1. **实现思路**（2-3句话说明核心逻辑）
2. **需要添加的代码**（标注USER CODE区域）
3. **关键参数计算**（如ARR、PSC的计算过程）
4. **测试验证方法**

### 对于综合题，输出格式：
1. **系统架构**（模块划分与数据流）
2. **各模块代码**（按USER CODE区域组织）
3. **主循环逻辑**
4. **中断服务配置**
5. **评分要点自查清单**

## 蓝桥杯常见失分点提醒
在生成代码时，主动检查并提醒以下问题：
- [ ] 按键未做防抖处理
- [ ] ADC未等待转换完成即读取
- [ ] 串口发送未检查缓冲区大小
- [ ] 定时器周期计算错误（注意时钟频率）
- [ ] 中断优先级配置不当导致嵌套问题
- [ ] 未考虑边界条件（如占空比0%和100%）
- [ ] 代码未放在USER CODE区域内（会被CubeMX覆盖）

## 代码风格要求
- 变量命名：驼峰式，如 `pwmDuty`, `adcValue`
- 宏定义：全大写，如 `PWM_PERIOD`, `MAX_DUTY`
- 注释：关键逻辑必须有中文注释
- 缩进：使用Tab或4空格（保持与CubeMX生成代码一致）
```

### 3.3 如何使用Skill

**方式一：自动触发**

在Skill的`description`中已定义触发关键词，当你的提问包含"蓝桥杯"、"STM32G431"等关键词时，Claude会自动加载此Skill。

**方式二：手动调用**

在Claude Code中输入斜杠命令：
```
/lanqiao-embedded
```

**方式三：在提示词中显式引用**

```
@lanqiao-embedded 请帮我实现一个PWM控制LED呼吸灯的功能
```

### 3.4 Skill进阶：添加参考文档

如果Skill内容较多，可以将部分内容拆分到外部文件：

```
.claude/skills/lanqiao-embedded/
├── SKILL.md          # 主文件（核心指令）
├── hal-reference.md  # HAL库常用函数速查
├── common-mistakes.md # 常见错误与解决方案
└── templates/        # 代码模板
    ├── pwm-template.c
    ├── adc-template.c
    └── uart-template.c
```

在`SKILL.md`中引用这些文件：
```markdown
## 参考文档
- HAL库函数速查：参见 [hal-reference.md](hal-reference.md)
- 常见错误排查：参见 [common-mistakes.md](common-mistakes.md)
- 代码模板：参见 [templates/](templates/) 目录
```

### 3.5 多个Skill的管理

如果你需要管理多个竞赛或项目的Skill，可以按以下结构组织：

```bash
~/.claude/skills/
├── lanqiao-embedded/      # 蓝桥杯嵌入式
├── lanqiao-mcu/           # 蓝桥杯单片机（51系列）
├── stm32-general/         # 通用STM32开发
└── code-review/           # 代码审查
```

项目级Skill（`.claude/skills/`）优先级高于用户级Skill（`~/.claude/skills/`）。

---

## 四、实战示例

假设你在比赛中遇到一道题："使用STM32G431的TIM3_CH1（PA6）输出频率1kHz、占空比可调的PWM，通过按键（PC13）调整占空比（步进10%），并通过串口打印当前占空比。"

**你的提问方式**：

```
@lanqiao-embedded
题目：使用TIM3_CH1（PA6）输出1kHz PWM，占空比可调（步进10%），
按键PC13调节，串口打印当前占空比。
请给出完整实现。
```

Skill会自动加载并提供：
1. TIM3的ARR和PSC计算（基于系统时钟84MHz）
2. 按键中断+防抖代码
3. PWM占空比更新代码
4. 串口打印代码
5. 所有代码标注USER CODE区域
6. 失分点自查提醒
根据现实情况的痛点补充
你这个要求非常专业，已经完全达到了**高级嵌入式架构师**的思维层级。这意味着你不再满足于让AI当一个“代码打字员”，而是希望它成为你的**“配置合规审查官”**。

要实现这个效果，我们需要在之前的Skill中引入**“配置契约（Configuration Contract）”**模式。核心理念是：**AI 宁可拒绝生成代码，也不能“无中生有”地创造外设句柄。**

以下是为 Claude Code Skill 定制的高级规则，包含**强制检查流程**和**标准反馈格式**。

---

### 🛡️ 核心策略：引入“三步走”审查机制

在 `SKILL.md` 中增加以下强制流程，要求AI在生成任何代码前，必须先完成**句柄清单核对**。

#### 1. 强制预检步骤（写入 Skill）
在蓝桥杯/STM32 开发 Skill 中添加以下逻辑：

```markdown
## ⛔ 代码生成前置约束（铁律）
在编写任何功能代码之前，必须执行以下“句柄审计”：

1. **识别需求**：分析用户需求，列出所有需要使用的硬件资源（如：PWM输出、ADC采集、I2C读写、外部中断）。
2. **匹配现有句柄**：对照用户提供的工程上下文（或通用的 STM32G431 工程），确认是否存在对应的 Handle（如 `&htim3`, `&hadc1`）。
3. **决策与反馈**：
   - **如果全部存在**：正常生成 HAL 代码。
   - **如果部分缺失**：**严禁**使用 `TIMx->CR1` 等寄存器直接替代，也**严禁**猜测一个 `htim5` 出来。
   - **必须立即停止代码生成**，并输出一份 **【CubeMX 配置缺失报告】**，指导用户去 CubeMX 添加配置。
```

---

#### 2. 标准化输出格式：“配置缺失报告”
当 AI 发现当前工程的句柄不够用时，它必须输出下面这个结构化的报告，而不是直接甩代码：

```markdown
### ⚠️ 代码生成受阻：检测到缺少必要的 CubeMX 句柄

当前工程中未检测到实现 `[具体功能名称]` 所需的硬件句柄。

#### 🔍 缺失资源清单
| 所需资源 | 推荐引脚 | 建议的外设名称 | 缺失原因 |
| :--- | :--- | :--- | :--- |
| 高级定时器（产生PWM） | PA8 | TIM1_CH1 | 当前工程未开启 TIM1 时钟，或未配置 Channel 1 为 PWM 模式 |
| I2C 总线（读写EEPROM） | PB6/PB7 | I2C1 | 当前工程未初始化 I2C1 |

#### 🛠️ CubeMX 解决步骤（请按顺序操作）
1. 打开 `STM32CubeMX` 并加载当前工程目录下的 `.ioc` 文件。
2. **添加 TIM1**：在 Pinout 视图中，点击 `PA8`，将其复用为 `TIM1_CH1`；在 Configuration 中，将 Channel1 设为 `PWM Generation CH1`，并根据需求调整预分频器（PSC）和自动重载值（ARR）。
3. **开启 I2C1**：在 Pinout 视图中，点击 `PB6` 选为 `I2C1_SCL`，`PB7` 选为 `I2C1_SDA`；在 Configuration 中，将 I2C 速度设为 `Fast Mode (400 KHz)`。
4. **重新生成代码**：点击 `GENERATE CODE` 覆盖工程（**请注意：** 只会更新 `Core` 文件夹，不会影响你设定的 `App` 文件夹）。

#### 📌 操作完成后
请在 VSCode 中重新附加（Attach）新生成的 `tim.c` 和 `i2c.c` 文件给我，我将立即为您生成对应的 PWM 或 EEPROM 读写函数。
```

---

### 🧠 进阶技巧：让 AI 学会“翻译” `.ioc` 文件（半自动审计）

既然你使用 VSCode，`.ioc` 文件其实是一个**纯文本配置文件**。你可以利用这一点，在提示词中加入：

> “我将把当前工程的 `.ioc` 文件内容粘贴给你，请解析其中 `#PCD` 和 `#PA` 开头的配置，列出当前启用的外设，并仅基于这些外设完成编码。”

**举个例子**：如果你把 `.ioc` 文件拖入上下文，AI 会看到：

```text
#PCD: TIM3.Channel1=PWM Generation CH1
#PCD: TIM3.Channel2=Input Capture direct mode
#PCD: USART1.Mode=Asynchronous
```

AI 读取后，会精准回答：“检测到您启用了 `TIM3_CH1` 用于 PWM，以及 `USART1`。但未检测到 `ADC1`。您要求的使用 ADC 读取电压的功能，请先在 CubeMX 中添加 ADC 句柄。”

---

### 🚀 最终 Skill 升级代码片段

将以下这段“紧箍咒”直接合并进你的 `SKILL.md` 中，确保 Claude Code 绝对不会乱写：

```markdown
## 编码伦理与“未知句柄”处理协议

当用户请求实现某个功能时，必须遵循以下决策树：

[用户需求] --> [分解为硬件资源]
    |
    V
[检查上下文 / .ioc 文件 / 用户提供的 main.c]
    |
    ├-- 发现对应 Handle (如 htim3) --> [✅ 允许生成 HAL 代码]
    |
    └-- 未发现对应 Handle (如 htim3) --> [🚫 触发“配置缺失报告”]
            |
            V
        [停止生成任何 C 代码] --> [输出 CubeMX 操作指南] --> [等待用户确认添加完成]
```

**特别强调**：
当你在回复中输出配置缺失报告时，**不要**为了“显得完整”而顺手用寄存器写一段代码给我。因为一旦你写了寄存器代码，用户可能会产生侥幸心理直接复制，从而导致后续 CubeMX 更新时引脚冲突。你的职责是**强制用户回到 CubeMX 走标准流程**。

---

通过这种方式，AI 就成了你 CubeMX 配置的“校验锁”。它不会越俎代庖，而是强迫你完善图形化配置。长久下来，你的工程永远保持 **“CubeMX 配置 = 实际代码使用的句柄”** 的一致性，混乱问题将从根源上被解决。

如果你需要在 Skill 中加入针对特定型号（比如 G431 的 HRTIM 或 DAC）的常见缺失检查清单，也可以告诉我，我可以帮你把那些具体的外设检查项也塞进去。 👍