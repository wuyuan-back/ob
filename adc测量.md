引脚PB15,PB12
配置为ADC输入模式
R37，R38

adc2_in15
adc1_in11

依旧先编译
ADC
在库函数
找到ADC获取函数
HAL_ADC_GetValue(&hadc1)
ADC使能函数
HAL_ADC_Start(&hadc1)
>[!warning]
>这个函数要在fun.c中使用，因为adc默认单次转换需要重复开启
>


```C
double get_vol(ADC_HandleTypedef *hadc)
{
 HAL_ADC_Start(&hadc1);
 uint32_t adc_value = HAL_ADC_GetValue(hadc);
 return 3.3*adc_value/4096;
}
```
adc为12bit
$2^{12}$

