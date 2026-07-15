轮询
	cpu主动反复询问外设
# 中断
外设发生事件时，主动通知CPU
```伪代码
void trap_task( ){
保存相关寄存器
处理中断
清除中断
恢复相关寄存器
}

```
## 异常与中断
 CPU 执行中遇到的特殊事件：
• 同步异常：这类异常在指令执行期间产生，如无效的存
储器地址/无效操作码；
eg:除0，
• 中断：它是与指令流异步的外部事件，包含来源包括软
件、定时器和外部触发
异步的外部事件
▪ 当异常发生时，处理器PC指针跳转到特定的地址上；当处
理完成后，使用返回指令返回原地址继续执行。
## 硬件中断
irq,
电平模式->保持中断信号一直为高，中断结束后变为0,信号为高时，触发中断

边缘模式->上升沿
SOC2只有一个中断脚
多个外设合并到一个脚，通过**或**逻辑连接至interrupt
	但需要在中断中进行轮询
	- （中断控制器）超出当前范围
## 软件实现
- main函数中
```C
	#define MIE_MACHINE_EXTERNAL      (1u << 11)
	#define MSTATUS_GLOBAL_INTERRUPT  (1u << 3)
  write_csr(mie, MIE_MACHINE_EXTERNAL);//允许机器外部中断
  write_csr(mstatus, MSTATUS_GLOBAL_INTERRUPT);//打开全局中断开关
```
中断使能
trap_handler


执行特定内存区代码（参考汇编trap_entry.s)
trap_entry:
- 
- trap_handler函数
- 
