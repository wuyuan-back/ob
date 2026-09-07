定时器的三个寄存器
- PSC 预分频器
- ARR 自动重载值 是一个16bite的数<=2的16次方-1
- CNT 计数器
- ![[三个寄存器的原理图.png]]
基本原理：定时器中断，![[Pasted image 20260113155549.png]]
系统频率80MHz
设置周期为1s的定时器
ARR=8000-1 是一个16bite的数
PSC=10000-1


# 注意事项
## 常见错误：
### 要使用定时器必须先添加TIM2使能端。
- HAL_StatusTypeDef HAL_TIM_Base_Start_IT(TIM_HandleTypeDef * htim);
- 在HAL_tim库的2365行
2.不可以将led_show()的代码放在中断函数之内，因为中断函数的执行与主循坏无关，无法具体确定是处于lcd的临时存储状态，所以==不要将显示的代码放在中断函数以内==
3.