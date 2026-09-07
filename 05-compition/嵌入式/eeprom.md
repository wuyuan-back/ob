IIC通信协议
主机STM32，从机AT24C02
知道从机的地址：
![[Pasted image 20260410151257.png|354]]
底层驱动代码参考IIC_HAL
位于资源数据包
复制到软件中
工程中添加文件，软件IIC
软件读写IIC
在IIC.hal.c下写两个函数
```C
void eeprom_write(uint8_t addr,uint8_t dat)
{
I2CStart();
I2CSendByte(0xa0);//锁定从机地址，执行写入
I2CWaitAck();
I2CSendByte(addr);//为片内地址，告诉从机内部写入地址
I2CWaitAck();
I2CSendByte(dat);//写入内容
I2CStop();

//连续调用时，会出错
HAL_Delay(20);
}
//addr 0-255
uint8_t eeprom_read(uint8_t addr)
{
I2CStart();
I2CSendByte(0xa0);//锁定从机地址，
I2CWaitAck();
I2CSendByte(addr);//为片内地址，告诉从机内部读取地址
I2CWaitAck();
I2CStop();

I2CStart();
I2CSendByte(0xa1);
I2CWaitAck();
uint8_t dat = I2CReceiveByte();
I2CSendNotAck();//不给回应，只发送一次
I2CStop();
return dat;
}



//主函数中
//I2C初始化
I2CInit();
```
