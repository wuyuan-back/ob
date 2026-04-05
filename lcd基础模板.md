不需要在cubeMX中设置，但需要手动导入lcd.c和lcd.h文件

初始化函数
```C
void lcdInit(void)
{
	//HAL库初始化
	LCD_Init();
	LCD_clear(Blue);
	LCD_SetTextColor(White);
	LCD_SetBackcolor(Blue);
}
```


