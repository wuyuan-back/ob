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
	- 
	- Tasks and Queues 标签页
	- 