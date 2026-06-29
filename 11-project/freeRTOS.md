RTOS real time operating systems
Free RTOS

移植freeRTOS
cubeMX
- Middleware and software packs
- interface CMSIS_V2 通用接口
	- os开口的函数都是通用接口函数
- 生成代码中
	- osKernerInitialize()系统内核初始化
	- defaultTaskHandle = osThreadNew(StartDefaultTask, NULL,&defaultTask_attributes)  ==Thread==线程概念
	- osKernelStart();
		- 注意此时cpu调度权移到Free RTOS 手中后边代码将不会被执行
- 编写代码
- StartDefaultTask 函数定义
	- 使用osdelay 延时
	- 编写Task1
- 回到CubeMx的界面
	- freeRtos
		- Tasks and Queues 标签页
	- 在cubeMx中编辑
		- 修改任务函数和任务名称
		- 可视化修改与添加
- FreeRTOS 任务调度原理
- PC寄存器 指向当前指向的指令，可以修改PC寄存器的值（汇编）
	- 时间片 重新计算时间片
	- 记录状态参数 分别指向任务A和任务B 多线程（状态流转）
		- 就绪态
		- 阻塞态(使用osDelay)
		- 运行态
		- 挂起态
		- ![[04-images/Pasted image 20260522122042.png]]