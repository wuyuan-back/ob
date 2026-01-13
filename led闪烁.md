主要参数PSC,ARR
基本原理：定时器中断，![[Pasted image 20260113155549.png]]
系统频率80MHz
设置周期为1s的定时器
ARR=8000-1 是一个16bite的数
PSC=10000-1


# 注意事项
1.常见错误：要使用定时器必须先添加TIM2使能端。
HAL_StatusTypeDef HAL_TIM_Base_Start_IT(TIM_HandleTypeDef * htim);
在
