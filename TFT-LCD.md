![[LCD设置.png]]
![[lcd—show.png]]
# lcd与led共用pc8-pc15的管脚，导致点亮LCD时LED全部点亮
## 问题本质：调用LCD函数时会更改pc端的电平
## 解决方法：1.通过修改调用的LCD函数添加代码 --> 使得lcd的更改不会引起LED变化
``` C
uint16_t temp = GPIOC->ODR;//函数开头



GPIOC->ODR = temp;//函数结尾
```
## 2.在LCD初始化之前将PD2设置为reset 就是关闭锁存器
``` C
HAL_GPIO_WritePin();
```