---
tags:
  - OpenHarmony
  - RTOS
  - Hi3861
  - 启动框架
created: 2026-06-30
---

# OpenHarmony 轻量系统启动框架

> 本文系统梳理 OpenHarmony 轻量系统（Hi3861/Hispark Pegasus）的启动流程与注册宏体系，与 [[点灯实验]] 互为补充。

---

## 一、启动流程概览

```
系统上电/复位
      │
      ▼
  ┌──────────────┐
  │  内核初始化   │  ← LosInit()、LOS_Start()
  └──────┬───────┘
         │
         ▼
  ┌──────────────────┐
  │  SYS_SERVICE_INIT │  系统核心服务初始化（中断、调度器底层）
  └──────┬───────────┘
         │
         ▼
  ┌──────────────────┐
  │ SYSEX_SERVICE_INIT│  扩展系统服务（文件系统、网络协议栈底座）
  └──────┬───────────┘
         │
         ▼
  ┌──────────────┐
  │   SYS_RUN    │  系统运行前收尾 —— 轻量初始化，**不可 while(1)**
  └──────┬───────┘
         │
         ▼
  ┌──────────────┐
  │  SYSEX_RUN   │  扩展运行前
  └──────┬───────┘
         │
         ▼
  ┌─────────────────┐
  │ APP_FEATURE_INIT │  ✅ **应用入口** —— 多线程已就绪，可创建任务
  └─────────────────┘
         │
         ▼
  ┌──────────┐
  │  用户任务  │  ← osThreadNew(LedTask, ...)
  └──────────┘
```

---

## 二、启动注册宏完整清单

所有宏定义位于 `ohos_init.h`，通过 **GCC 段属性 `__attribute__((section()))`** 将函数指针放入特定链接段，系统启动时按段顺序遍历调用。

| 宏 | 对应链接段 | 优先级（数字越小越先） | 说明 |
|---|---|---|---|
| `SYS_SERVICE_INIT(func)` | `.zinitcall.sys.service.init` | **0** | 系统核心服务（内存管理、定时器、中断） |
| `SYSEX_SERVICE_INIT(func)` | `.zinitcall.sys2.service.init` | **1** | 扩展系统服务（IPC、文件系统底座） |
| `SYS_RUN(func)` | `.zinitcall.sys.run` | **2** | 系统运行前初始化（IO、外设早期配置） |
| `SYSEX_RUN(func)` | `.zinitcall.sys2.run` | **3** | 扩展运行前初始化 |
| `APP_FEATURE_INIT(func)` | `.zinitcall.app.feature.init` | **4** | **应用功能入口**（业务层） |

### 关键规则

1. **顺序严格**：数字越小的段越早执行，不允许跨段依赖
2. **不可阻塞**：`SYS_SERVICE_INIT` ~ `SYSEX_RUN` 阶段调度器可能未完全就绪，**不能使用 `while(1)` 或 `osDelay`**
3. **`APP_FEATURE_INIT` 是唯一适合多任务的地方**：此时 CMSIS-RTOS V2 调度器已运行，可以安全调用 `osThreadNew`、`osDelay`、信号量等

---

## 三、实现原理：GCC 段属性机制

`ohos_init.h` 中的核心宏展开大致如下：

```c
typedef void (*InitCall)(void);

#define SYS_RUN(func) \
    __attribute__((section(".zinitcall.sys.run"))) InitCall __zinitcall_##func = func

#define APP_FEATURE_INIT(func) \
    __attribute__((section(".zinitcall.app.feature.init"))) InitCall __zinitcall_##func = func
```

**工作流程**：

1. 每个 `SYS_RUN(func)` 在编译时生成一个**函数指针**，放入对应的 `.zinitcall.xxx` 段
2. 链接脚本将同名的段**合并**为一个连续数组
3. 内核启动时调用 `LOS_DoInitCall()` 遍历该数组，逐一执行所有注册函数

```c
// 简化实现
void LOS_DoInitCall(void)
{
    extern InitCall __zinitcall_sys_run_start[];
    extern InitCall __zinitcall_sys_run_end[];
    for (InitCall *call = __zinitcall_sys_run_start;
         call < __zinitcall_sys_run_end;
         call++) {
        (*call)();  // 逐个调用
    }
}
```

---

## 四、实战中的关键差异

对比 [[点灯实验#三、延伸收获：OpenHarmony-的启动时序认知]] 中的实际教训：

| 宏 | 多线程就绪 | 能否 `while(1)` | 能否 `osThreadNew` | 典型场景 |
|---|---|---|---|---|
| `SYS_RUN` | ❌ 未就绪 | ❌ 卡死系统 | ❌ | GPIO 快速初始化、打印标识 |
| `APP_FEATURE_INIT` | ✅ 已就绪 | ✅ | ✅ | 创建点灯/传感器/网络任务 |

> **踩坑记忆**：点灯实验中忘记加 `APP_FEATURE_INIT(led_demo)`，代码烧录后毫无反应。加上后同时注意不要误用 `usleep`（忙等待）导致看门狗复位，应使用 `osDelay`（主动让权）。

---

## 五、代码模板：标准启动结构

```c
#include "ohos_init.h"
#include "cmsis_os2.h"

/* ─── 早期初始化（SYS_RUN 阶段）─── */
static void EarlyHardwareInit(void)
{
    // 只做快速初始化，不要 while(1)！
    IoTGpioInit(LED_TEST_GPIO);
}
SYS_RUN(EarlyHardwareInit);

/* ─── 应用入口（APP_FEATURE_INIT 阶段）─── */
static void LedTask(void *arg)
{
    (void)arg;
    while (1) {
        IoTGpioSetOutputVal(LED_TEST_GPIO, 1);
        osDelay(30);          // ✅ 主动让权，别用 usleep
        IoTGpioSetOutputVal(LED_TEST_GPIO, 0);
        osDelay(30);
    }
}

static void LedDemoEntry(void)
{
    osThreadAttr_t attr = {
        .name       = "LedTask",
        .priority   = osPriorityNormal,
        .stack_size = 1024,      // ✅ 足够栈空间
    };
    osThreadNew(LedTask, NULL, &attr);
}
APP_FEATURE_INIT(LedDemoEntry);
```

---

## 六、参考链接

- [[点灯实验]] — 本文的实战背景，记录了 5 个典型踩坑
- [[下半年规划]] — 鸿蒙实验在本学期规划中的位置
- OpenHarmony 源码：`utils/native/lite/include/ohos_init.h`
- CMSIS-RTOS V2 API 参考：`osThreadNew`、`osDelay`、`osPriority`

---

## Change Log

| 日期 | 变更 |
|---|---|
| 2026-06-30 | 初版创建，梳理启动宏体系与点灯实验的关联 |
