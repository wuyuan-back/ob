![[LCD设置.png]]
![[lcd—show.png]]
# lcd与led共用pc8-pc15的管脚，导致点亮LCD时LED全部点亮
## 问题本质：调用LCD函数时会更改pc端的电平
## 解决方法：通过修改调用的LCD函数添加代码
``` C
uint16_t temp = GPIOC->OCR;//函数开头



GOIO->OCR = temp;//函数结尾
```
