使用到的函数：HAL_CGPIO_==W==ritePin(GPIO C,GPIO_PIN_13,GPIO_PIN_SET)
使用到的引脚PD2(默认低电平），PC8－15(默认高电平)根据原理图可知拉高电平熄灭
点亮led
前置知识：GPIO——P
```C
void led_show(int led_locate)
{
	HAL_GPIO_WritePin(GPIO_C,GPIO_PIN_8)
}
```