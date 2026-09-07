使用到的函数：HAL_CGPIO_==W==ritePin(GPIO C,GPIO_PIN_13,GPIO_PIN_SET)
使用到的引脚PD2(默认低电平），PC8－15(默认高电平)根据原理图可知拉高电平熄灭
点亮led
前置知识：GPIO_PIN_X是uint16_t,LD1->PC8
```C
void led_show(int led_locate，int led_state)
{
	if(led_state == 1)
	{
	HAL_GPIO_WritePin(GPIOC,GPIO_PIN_8<<(led_locate-1),GPIO_PIN_RESET);
	}
	else
	{HAL_GPIO_WritePin(GPIOC,GPIO_PIN_8<<(led_locate-1),GPIO_PIN_SET);
	}
	HAL_GPIO_WritePin(GPIOD,GPIO_PIN_2,GPIO_PIN_SET);
	HAL_GPIO_WritePin(GPIOD,GPIO_PIN_2,GPIO_PIN_RESET);
	
}
```
可能存在问题，灯光打架
建议：
- [ ] 使用全局变量