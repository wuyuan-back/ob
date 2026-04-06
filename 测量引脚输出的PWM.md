测量原理
$f =1/t$
PWM的上升沿，产生中断
解决方法：
上升沿产生时，cnt = 0;
下一个上升沿产生时，保存在一个变量中

![[20260406_155842.png]]
以上为原理图

![[20260406_155926.png]]
555定时器，自动通过OUT输出一个频率可调的PWM波，通过**PA15**进行输入捕获，通过**R40**调节PWM波；
对应为两个问题
- 通过PA15，PB4测量PWM波
- 通过杜邦线将PA1连接到PA7引脚测量PWM波

# 通过PA7完成脉冲输入捕获
# 环境配置
cubeMx
- PA17，设置为TIM17_ch1
- 左侧找到TIM17,修改channel 1 为input capture mode即输入捕获
- PSC设置为80－1
- NVICseetings 使能中断
## 代码实现
- 在tim.h找到中断使能函数，HAL_TIM_Start_IT(   )
- 再找到输入捕获的回调函数,TIM_IT_CaptureCallback()
- 
```C
uint32_t fre ,capture_value;


void C
{
	if(htim->Instance == TIM17)
	{
		capture_value = HAL_TIM_ReadCaptureValue(htim,TIM_CHANNEL_1);//在tim.h中找到ctrl f找到readcapture 函数
		TIM17->CNT = 0;
		fre = (80000000/(80*capture_value));
	}

}


//写完之后再到lcd_show()lcd显示函数中添加
```
>[!TIPs]
>这个函数实际上读取的是CCR值，本质是，触发中断时CNT赋值给CCR
>所以也可以通过cature_value = TIM17->CCR1;的等效写法
