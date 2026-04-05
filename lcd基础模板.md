不需要在cubeMX中设置，但需要手动导入lcd.c和lcd.h文件

初始化函数
```C
void lcdInit(void)
{
	//HAL库初始化
	LCD_Init();
	//设置LCD的背景色
	LCD_clear(Blue);
	//设置字体颜色
	LCD_SetTextColor(White);
	//设置LCD字体的背景色
	LCD_SetBackcolor(Blue);
}
```

解决LCD和LED引脚冲突的问题
原因：LCD刷新时修改GPIOC->ODR寄存器
解决方法：在LCD现实前保存GPIO->ODR寄存器

修改**最底层**的LCD代码
即
```C
void LCD_WriteReg(u8 LCD_Reg, u16 LCD_RegValue);
void LCD_WriteRAM_Prepare(void); 
void LCD_WriteRAM(u16 RGB_Code);
```

修改样例
```C
void LCD_WriteReg(LCD_Reg,LCD_RegValue)
{
uint16_t temp = GPIOC->ODR；

其余源代码保持不动

GPIOC->ODR = temp;
}
```

