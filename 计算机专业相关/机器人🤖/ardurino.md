Arduino在数字电路中常用的函数主要包括以下几个：

引脚模式设置函数：`pinMode()`
- 功能：用于设置数字引脚的工作模式。
- 参数：
  - `pin`：要设置的引脚编号。
  - `mode`：引脚模式，可以是以下几种之一：
      - `INPUT`：将引脚设置为输入模式。
      - `OUTPUT`：将引脚设置为输出模式。
      - `INPUT_PULLUP`：将引脚设置为输入模式，并启用内部上拉电阻。
- 示例：
  
  ```cpp
    pinMode(13, OUTPUT); // 将13号引脚设置为输出模式
    pinMode(2, INPUT_PULLUP); // 将2号引脚设置为输入模式，并启用内部上拉电阻
    ```

数字信号写入函数：`digitalWrite()`
- 功能：用于向指定的数字引脚写入高电平或低电平。
- 参数：
  - `pin`：要操作的数字引脚编号。
  - `value`：要写入的电平状态，可以是`HIGH`（高电平，通常为5V）或`LOW`（低电平，0V）。
- 示例：
  
  ```cpp
    digitalWrite(13, HIGH); // 将13号引脚设置为高电平
    digitalWrite(13, LOW); // 将13号引脚设置为低电平
    ```

数字信号读取函数：`digitalRead()`
- 功能：用于读取指定数字引脚的电平状态。
- 参数：`pin`，要读取的数字引脚编号。
- 返回值：返回引脚的电平状态，`HIGH`或`LOW`。
- 示例：
  
  ```cpp
    int buttonState = digitalRead(2); // 读取2号引脚的电平状态
    if (buttonState == LOW) {
      // 如果2号引脚为低电平，执行相应操作
    }
    ```

脉冲宽度调制函数：`analogWrite()`
- 功能：用于向支持PWM的引脚输出模拟值，通过PWM信号来近似模拟输出。
- 参数：
  - `pin`：要控制的PWM引脚编号。
  - `value`：PWM输出值，范围为0到255，其中0表示0%占空比（低电平），255表示100%占空比（高电平）。
- 示例：
  
  ```cpp
    analogWrite(9, 128); // 向9号引脚输出50%占空比的PWM信号
    ```

这些函数是Arduino数字电路操作的基础，通过合理使用它们，可以实现对各种数字输入输出设备的控制和信号处理。
电池；突出正，平负
电压低于10.5v需充电

## 中断
Arduino在模拟电路中常用的函数主要有`analogRead()`和`analogWrite()`。以下是这两个函数的详细介绍：

1. `analogRead(pin)`
- 功能：从指定的模拟输入引脚读取模拟值。
- 参数：
  - `pin`：要读取的模拟输入引脚编号，通常为`A0`到`A5`（具体取决于Arduino板的型号）。
- 返回值：返回一个整数值，范围为0到1023。这个值表示输入电压相对于参考电压（通常是5V或3.3V）的比例。
- 示例：
  
  ```cpp
    int sensorValue = analogRead(A0); // 从A0引脚读取模拟值
    Serial.println(sensorValue); // 将读取的值打印到串口监视器
    ```

2. `analogWrite(pin, value)`
- 功能：通过PWM（脉宽调制）的方式向指定的引脚输出模拟值。
- 参数：
  - `pin`：要输出PWM信号的引脚编号，必须是支持PWM的引脚。
  - `value`：PWM占空比，范围为0到255，对应占空比为0%到100%。
- 返回值：无。
- 注意事项：
  - 不同的Arduino板支持的PWM引脚不同。例如，Arduino Uno支持的PWM引脚为3、5、6、9、10和11。
  - 使用`analogWrite()`时，不需要先用`pinMode()`设置引脚模式。
  - PWM信号并不是真正的模拟信号，而是一种通过快速切换高电平和低电平来模拟的信号。
- 示例：
  
  ```cpp
    analogWrite(9, 128); // 向9号引脚输出50%占空比的PWM信号
    ```

应用场景
- `analogRead()`：常用于读取传感器（如光敏电阻、温度传感器）的模拟信号。
- `analogWrite()`：常用于控制LED的亮度或直流电机的转速。

通过这两个函数，Arduino可以方便地与各种模拟传感器和执行器进行交互，实现复杂的控制功能。
Arduino 提供了中断功能，允许程序在特定事件发生时暂停当前任务，转而执行一段预定义的代码（称为中断服务例程，ISR）。以下是与中断相关的函数和概念：

1. `attachInterrupt()`
- 功能：将一个中断服务例程（ISR）附加到指定的中断引脚。
- 参数：
  - `interrupt`：中断编号，通常为 `0` 或 `1`（某些 Arduino 板可能支持更多）。
  - `callback`：中断服务例程的名称，即当中断发生时要执行的函数。
  - `mode`：触发模式，可以是以下几种之一：
      - `LOW`：当引脚电平为低时触发中断。
      - `CHANGE`：当引脚电平从高变低或从低变高时触发中断。
      - `RISING`：当引脚电平从低变高时触发中断。
      - `FALLING`：当引脚电平从高变低时触发中断。
- 示例：
  
  ```cpp
    void myISR() {
      // 中断服务例程代码
      digitalWrite(13, HIGH); // 点亮LED
    }

    void setup() {
      pinMode(2, INPUT_PULLUP); // 将2号引脚设置为输入模式，并启用内部上拉电阻
      attachInterrupt(0, myISR, FALLING); // 将中断服务例程附加到中断0（数字2引脚），当电平从高变低时触发
    }

    void loop() {
      // 主循环代码
    }
    ```

2. `detachInterrupt()`
- 功能：从指定的中断引脚分离中断服务例程。
- 参数：
  - `interrupt`：中断编号，通常为 `0` 或 `1`。
- 示例：
  
  ```cpp
    detachInterrupt(0); // 分离中断0的中断服务例程
    ```

3. 中断引脚
- Arduino Uno：数字引脚2和3通常用于中断0和中断1。
- 其他 Arduino 板：支持的中断引脚可能不同，具体可以参考相应板的文档。

注意事项
1. 中断服务例程（ISR）的编写：
   - ISR 应该尽可能短小精悍，避免复杂的计算和调用耗时的函数，因为 ISR 需要快速执行以避免阻塞其他中断。
   - ISR 中不能使用 `delay()` 函数，因为这会导致中断响应延迟。
   - ISR 中不能使用 `Serial.print()` 等串口通信函数，因为串口通信可能会被中断。
2. 中断优先级：
   - Arduino 的中断系统是简单的，通常只有一个全局中断优先级。如果有多个中断同时触发，Arduino 会按照中断编号的顺序依次处理。
3. 中断的稳定性：
   - 中断触发的稳定性取决于外部信号的质量。如果信号抖动较大，可能会导致中断频繁触发。

示例代码：使用中断检测按钮按下

```cpp
volatile bool buttonPressed = false; // 使用volatile关键字，因为ISR会修改这个变量

void buttonISR() {
  buttonPressed = true; // 在ISR中设置标志位
}

void setup() {
  pinMode(2, INPUT_PULLUP); // 将2号引脚设置为输入模式，并启用内部上拉电阻
  attachInterrupt(0, buttonISR, FALLING); // 将中断服务例程附加到中断0（数字2引脚），当电平从高变低时触发
}

void loop() {
  if (buttonPressed) { // 检查标志位
    buttonPressed = false; // 重置标志位
    digitalWrite(13, HIGH); // 点亮LED
    delay(500); // 延时500毫秒
    digitalWrite(13, LOW); // 熄灭LED
  }
}
```

在这个示例中，当按钮按下时，中断服务例程 `buttonISR` 会被触发，设置一个全局变量 `buttonPressed` 为 `true`。在主循环中，程序会检查这个变量，执行相应的操作。

通过使用中断，可以实现更高效和响应更快的事件处理，特别是在需要及时响应外部信号的情况下。

以下是一些常见的Arduino第三方中断库及相关信息：

1. MsTimer2
- 功能：提供定时中断功能，允许用户设置定时器中断的时间间隔和调用的中断服务程序。
- 主要函数：
  - `void set(unsigned long ms, void (*f)())`：设置定时中断的时间间隔（单位为毫秒）和调用的中断服务程序。
  - `void start()`：开启定时中断。
  - `void stop()`：关闭定时中断。
- 使用示例：
  
  ```cpp
    void myISR() {
      // 中断服务例程代码
    }

    void setup() {
      MsTimer2::set(1000, myISR); // 每1000毫秒调用一次myISR
      MsTimer2::start(); // 开始定时中断
    }

    void loop() {
      // 主循环代码
    }
    ```

2. TimerOne
- 功能：针对Timer1的库，提供定时中断功能，适用于需要使用Timer1的项目。
- 主要函数：
  - `void initialize(long microseconds)`：初始化定时器，设置定时器的周期（单位为微秒）。
  - `void start()`：开始定时器。
  - `void stop()`：停止定时器。
  - `void attachInterrupt(void (*isr)(), long microseconds)`：附加中断服务例程，并设置定时器周期。
- 使用示例：
  
  ```cpp
    void myISR() {
      // 中断服务例程代码
    }

    void setup() {
      Timer1.initialize(1000000); // 设置定时器周期为1000000微秒（1秒）
      Timer1.attachInterrupt(myISR); // 附加中断服务例程
      Timer1.start(); // 开始定时器
    }

    void loop() {
      // 主循环代码
    }
    ```

3. Arduino-timer
- 功能：一个简单易用的定时器库，支持多种定时器操作。
- 主要函数：
  - `timer_create_default()`：创建一个默认设置的定时器。
  - `timer.every(unsigned long interval, void (*function)())`：设置定时器在指定的时间间隔（单位为毫秒）后调用指定的函数。
  - `timer.tick()`：更新定时器状态，需要在`loop()`中调用。
- 使用示例：
  
  ```cpp
    #include <arduino-timer.h>

    auto timer = timer_create_default(); // 创建定时器

    void myFunction() {
      // 定时器触发时执行的函数
    }

    void setup() {
      timer.every(1000, myFunction); // 每1000毫秒调用一次myFunction
    }

    void loop() {
      timer.tick(); // 更新定时器状态
    }
    ```

4. Tilen Majerle的EXTI库（STM32）
- 功能：用于STM32系列的外部中断（EXTI）库，简化了外部中断的配置和使用。
- 特点：
  - 自动开启GPIO口时钟频率。
  - 自动配置输入模式引脚。
  - 自动开启中断。
- 适用场景：适用于STM32系列开发板，需要使用外部中断的项目。

5. HLW8012库
- 功能：专为HLW8012电能监测芯片设计的库，支持中断驱动和非中断驱动两种模式。
- 特点：
  - 中断驱动模式下，测量值在后台持续更新。
  - 提供默认校准参数，支持自定义电阻值和手动校准。
- 适用场景：适用于需要进行电能监测的项目，如智能插座、电能监测设备等。

这些第三方中断库为Arduino项目提供了更丰富的中断功能，可以根据具体需求选择合适的库来实现定时中断或外部中断等功能。