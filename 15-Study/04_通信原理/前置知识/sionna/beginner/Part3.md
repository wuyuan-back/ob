### Sionna Tutorial Part 3：Advanced Link-level Simulations（高级链路级仿真）

Part 3 是 Sionna 入门教程中非常关键的一章。它开始从前两章的基础通信系统和可微分通信系统，进入更加接近实际 5G 无线通信系统的仿真。

如果说：

* Part 1：学习如何使用 Sionna 搭建通信系统。

* Part 2：学习如何将通信系统中的参数变成可训练参数，使用梯度下降进行优化。

* Part 3：学习如何搭建一个更加真实的 5G OFDM 通信链路。

* Part 4：进一步使用神经网络构建接收机，实现 Learned Receiver。

那么 Part 3 的核心就是：

使用 Sionna 搭建一个包含 5G LDPC 编码、OFDM 调制、3GPP 信道模型、信道估计、均衡、解调和译码的完整通信系统。

这也是你后续研究 AI 信道估计、AI 信号检测的重要基础。

### 一、Part 3 的整体架构

首先看一下本章搭建的通信系统。

![Publications - Taekyun Lee](https://images.openai.com/static-rsc-4/TLnGKwgOrNovKhRuWR-VzJ0sEu4nvHbNtF9yhkG7r0bPwvyXzRkBh-J_oc9teUhlyEqw5wNfd_gmMgaHDzoEEG1Q_RR4lWTP81ZFHxDR0zx-Oseu79i_EySEB_03KHDc6Qv4gCyXMVraJrXUsHiSTqArHKH0Bxo6M13YrWKx2s090yowzj4axfm4kDXZETNN?purpose=fullsize)

它实际上是一条完整的数字通信链路：

### 发射端 Transmitter

Binary Source

随机生成信息比特

5G LDPC Encoder

信道编码

Mapper + ResourceGridMapper

QAM 调制 + OFDM 资源映射

### 无线信道 Channel

3GPP CDL Channel + AWGN

多径衰落、多天线传播、噪声

### 接收端 Receiver

LS Channel Estimator

信道估计

LMMSE Equalizer

信号均衡

Demapper + LDPC Decoder

解调 + 信道译码

Recovered Bits

恢复原始信息比特

你需要特别注意：

本章的重点已经不再是单独理解某个通信模块，而是理解这些模块如何组合成一个完整的端到端通信系统。

### 二、OFDM Resource Grid and Stream Management

这一部分主要解决两个问题：

* 多个收发天线之间如何管理数据流？

* OFDM 系统中如何分配数据符号和导频符号？

### 2.1 Stream Management：数据流管理

首先看参数：

```python
NUM_UT = 1
NUM_BS = 1

NUM_UT_ANT = 1
NUM_BS_ANT = 4

NUM_STREAMS_PER_TX = NUM_UT_ANT
```

这里定义了：

| 参数                 | 含义          | 数值  |
| ------------------ | ----------- | --- |
| NUM_UT             | 用户终端数量      | 1   |
| NUM_BS             | 基站数量        | 1   |
| NUM_UT_ANT         | 用户终端天线数     | 1   |
| NUM_BS_ANT         | 基站天线数       | 4   |
| NUM_STREAMS_PER_TX | 每个发射端的数据流数量 | 1   |

这意味着：

* 用户终端只有一根发射天线。

* 基站有四根接收天线。

* 用户终端发送一个数据流。

* 基站通过四根天线接收这个数据流。

这就是 SIMO（Single Input Multiple Output）。

![5G手机到底牛逼在哪里？](https://images.openai.com/static-rsc-4/n-96IfbIlU3UQUZ28BCRrsV2WryGTWNlbWoR-qekE6GkILAVGfW1aFC_TlXOvcrvSV84K3WNGsIJ6Y8ti1tz8dA6N5UVJg42YvvzP1PpNbmuMJi857_Ar1KY-3pSmEUuIn_gwjTFF_NYht-W8zrrrN0dRQic2YJINVpNPH54PxIsdVR0jfMx39RqjDfQwEci?purpose=fullsize)

这里需要区分三个概念：

* 天线数量：物理射频天线的数量。

* 数据流数量：独立传输的数据流数量。

* 接收端数量：通信系统中逻辑接收节点的数量。

四根接收天线并不意味着接收四个独立数据流。

### RX_TX_ASSOCIATION

```python
RX_TX_ASSOCIATION = np.array([[1]])
```

这是接收端与发射端的关联矩阵。

矩阵：

A=
\\begin{bmatrix}
1
\\end{bmatrix}

其中：

* 1：接收端与发射端存在通信关系。

* 0：不存在通信关系。

注意，这个矩阵描述的是逻辑收发节点之间的关系，而不是物理天线之间的连接关系。

最后：

```python
STREAM_MANAGEMENT = sn.phy.mimo.StreamManagement(
    RX_TX_ASSOCIATION,
    NUM_STREAMS_PER_TX
)
```

创建数据流管理对象。

在简单的 SIMO 系统中，它比较容易理解；到了多用户 MIMO 系统，就需要考虑不同用户的数据流如何分配给不同接收端。

### 2.2 Resource Grid：OFDM 资源栅格

接下来是：

```python
RESOURCE_GRID = sn.phy.ofdm.ResourceGrid(
    num_ofdm_symbols=14,
    fft_size=76,
    subcarrier_spacing=30e3,
    num_tx=NUM_UT,
    num_streams_per_tx=NUM_STREAMS_PER_TX,
    cyclic_prefix_length=6,
    pilot_pattern="kronecker",
    pilot_ofdm_symbol_indices=[2, 11]
)
```

这段代码非常重要。

Resource Grid 是 OFDM 系统中管理时频资源的核心对象。

![OFDM Resource Grid and Channel Estimation - MATLAB & Simulink](https://images.openai.com/static-rsc-4/N3oH602V1umD3ZZV6FddUomdASLA0IMsmI-YsIFt_OBE5RINrZmcemrKWSVq1-GZzaiBtZpkSmRSTYGnRzokefx0nbPVXX4jpgBU04GQze4sFFXvZ3O63s8OIMfSKtbGWIJbvQaICol0ptRS8VY9g0-wqXxadOlaR8UUMbYTNesHrfmizAGLummwPbJ9YAuu?purpose=fullsize)

理解参数：

| 参数                        | 含义           | 数值        |
| ------------------------- | ------------ | --------- |
| num_ofdm_symbols          | OFDM 符号数量    | 14        |
| fft_size                  | FFT 点数       | 76        |
| subcarrier_spacing        | 子载波间隔        | 30 kHz    |
| cyclic_prefix_length      | 循环前缀长度       | 6         |
| pilot_pattern             | 导频分配模式       | Kronecker |
| pilot_ofdm_symbol_indices | 导频所在 OFDM 符号 | 2、11      |

其中最重要的是：

一个 OFDM Resource Grid 可以看成一个二维时频资源矩阵。

* 横向：OFDM 符号，即时间维度。

* 纵向：子载波，即频率维度。

这里有：

14\\times76=1064

个时频资源单元（Resource Elements，RE）。

但不是所有资源单元都用于传输数据。

其中一部分用于导频，剩下的才用于数据传输。

### 为什么需要导频？

接收端不知道无线信道具体发生了什么变化。

因此，发射端需要发送已知的导频信号，让接收端通过这些已知信号估计信道。

这就是后面 LS Channel Estimator 的基础。

### 三、Antenna Arrays：天线阵列

这一部分开始引入更加真实的无线传播环境。

首先：

```python
CARRIER_FREQUENCY = 2.6e9
```

载波频率：

f_c=2.6\\text{ GHz}

接下来定义用户终端天线：

```python
UT_ARRAY = sn.phy.channel.tr38901.Antenna(
    polarization="single",
    polarization_type="V",
    antenna_pattern="38.901",
    carrier_frequency=CARRIER_FREQUENCY
)
```

这里使用了 3GPP TR 38.901 标准中的天线模型。

然后定义基站天线阵列：

```python
BS_ARRAY = sn.phy.channel.tr38901.AntennaArray(
    num_rows=1,
    num_cols=int(NUM_BS_ANT/2),
    polarization="dual",
    polarization_type="cross",
    antenna_pattern="38.901",
    carrier_frequency=CARRIER_FREQUENCY
)
```

这里有几个值得注意的地方：

第一，基站有四个物理天线单元。

但是：

```python
num_cols=int(NUM_BS_ANT/2)
```

得到的是 2。

这是因为这里采用双极化天线配置。每个阵列位置包含两个极化分量，因此两个位置对应四个天线端口。

第二，天线不仅仅是一个数量参数。

真实天线还具有：

* 辐射方向图（Radiation Pattern）

* 极化方式（Polarization）

* 天线间距（Antenna Spacing）

* 空间方向性

这些因素会影响无线信道的空间特性。

这也是 Sionna 相较于简单 AWGN 仿真的重要优势之一。

### 四、Channel Model：3GPP 无线信道模型

这是 Part 3 最值得认真学习的部分之一。

### 4.1 CDL 信道模型

```python
CDL_MODEL = "C"
DELAY_SPREAD = 100e-9

SPEED = 10.0

CDL = sn.phy.channel.tr38901.CDL(
    CDL_MODEL,
    DELAY_SPREAD,
    CARRIER_FREQUENCY,
    UT_ARRAY,
    BS_ARRAY,
    DIRECTION,
    min_speed=SPEED
)
```

这里使用了 3GPP TR 38.901 中的 CDL（Clustered Delay Line）模型。

CDL 用于模拟无线信道中的多径传播。

![How Wi-Fi Motion Sensing Works: The Physics Behind the Technology - Surety Home](https://images.openai.com/static-rsc-4/uHyow1-SgT0NJHBZnxopIdI2ivT3Q8A91tqGTmRNrDqVYDQLJEowFjrpf_g5WoMtNacHpk0zqIVkFAC2kNAGJ8qe9nIu82zfRuSP6EC12GYmrgH9vcwBVuuR8rvH1fXttUBN4hHacRH3IODW4kaXlshAVfQr4YyUGmmKdn9VWUr_ZWdQH2_-UorCWzTxjigr?purpose=fullsize)

现实中，无线电波从发射端传播到接收端时，会经历：

* 直射传播

* 建筑物反射

* 地面反射

* 散射

* 绕射

因此，接收端收到的并不是单一的一条信号，而是多条不同传播路径的叠加。

可以用下面的公式描述：

h(t,\\tau)=\\sum_{l=1}^{L}
a_l(t)\\delta(\\tau-\\tau_l)

其中：

* ：多径数量。

* ：第 条路径的复数增益。

* ：第 条路径的传播时延。

* ：冲激函数。

这正是 CDL 模型的基本思想。

### 4.2 CDL-A 到 CDL-E

Sionna 提供五种典型的 CDL 信道：

| 模型    | 信道类型 |
| ----- | ---- |
| CDL-A | NLoS |
| CDL-B | NLoS |
| CDL-C | NLoS |
| CDL-D | LoS  |
| CDL-E | LoS  |

其中：

* NLoS：Non-Line-of-Sight，非视距传播。

* LoS：Line-of-Sight，视距传播。

本章选择：

```python
CDL_MODEL = "C"
```

即 CDL-C 非视距信道。

这意味着我们主要研究存在多径传播、没有直射主路径的无线通信环境。

### 4.3 生成信道冲激响应

```python
BATCH_SIZE = 128

a, tau = CDL(
    batch_size=BATCH_SIZE,
    num_time_steps=RESOURCE_GRID.num_ofdm_symbols,
    sampling_frequency=1/RESOURCE_GRID.ofdm_symbol_duration
)
```

这段代码非常重要。

它不是生成一条信道，而是同时生成 128 组随机信道实现。

其中：

* `a`：多径复增益。

* `tau`：多径传播时延。

输出维度：

```python
a.shape
# [128, 1, 4, 1, 1, 24, 14]

tau.shape
# [128, 1, 1, 24]
```

我们逐个理解 `a` 的维度：

| 维度  | 含义         | 大小  |
| --- | ---------- | --- |
| 1   | Batch Size | 128 |
| 2   | 接收端数量      | 1   |
| 3   | 接收天线数量     | 4   |
| 4   | 发射端数量      | 1   |
| 5   | 发射天线数量     | 1   |
| 6   | 多径数量       | 24  |
| 7   | 时间采样数量     | 14  |

为什么是 14？

因为 Resource Grid 中配置了：

```python
num_ofdm_symbols=14
```

所以这里生成了对应于 14 个 OFDM 符号时刻的信道增益。

为什么有 24 条路径？

这是 CDL-C 模型对应的多径结构。

### a 和 tau 有什么区别？

这是一个非常容易混淆的知识点。

| 参数  | 物理含义  | 是否随时间变化 |
| --- | ----- | ------- |
| a   | 路径复增益 | 是       |
| tau | 路径时延  | 本例中假设不变 |

复数增益：

a_l(t)=a_{l,I}(t)+ja_{l,Q}(t)

它包含：

* 幅度变化。

* 相位变化。

而路径时延：

\\tau_l

描述的是信号经过不同路径到达接收端所需要的时间。

因此，`a` 描述信道的动态变化，`tau` 描述多径传播的时延结构。

### 五、Uplink Transmission：完整上行通信链路

这是本章最核心的部分。

前面配置了：

* OFDM 资源栅格。

* 天线阵列。

* 3GPP CDL 信道。

现在正式搭建完整通信链路。

### 5.1 发射端：编码与调制

首先：

```python
NUM_BITS_PER_SYMBOL = 2
CODERATE = 0.5
```

这里采用 QPSK 调制。

因为：

\\log_2 4=2

每个 QPSK 符号携带两个编码比特。

编码率为：

R=\\frac{k}{n}=0.5

也就是说，每两个编码比特中，平均只有一个信息比特。

接下来：

```python
n = int(
    RESOURCE_GRID.num_data_symbols
    * NUM_BITS_PER_SYMBOL
)

k = int(n * CODERATE)
```

这里：

* ：编码后的比特数量。

* ：原始信息比特数量。

在本例中：

n=1824k=912

因此，每个数据块：

* 输入 912 个信息比特。

* 输出 1824 个编码比特。

### 5G LDPC 编码

```python
encoder = sn.phy.fec.ldpc.LDPC5GEncoder(k, n)
```

这里使用的是 5G NR 标准中的 LDPC 编码器。

这与前面 Part 1、Part 2 中较简单的通信链路不同。

它开始引入真正的 5G 信道编码技术。

### QPSK 映射

```python
mapper = sn.phy.mapping.Mapper(
    "qam",
    NUM_BITS_PER_SYMBOL
)
```

将二进制比特转换为复数调制符号。

例如：

00\\rightarrow s_001\\rightarrow s_110\\rightarrow s_211\\rightarrow s_3

这些符号会映射到 QPSK 星座图上。

### Resource Grid Mapping

```python
rg_mapper = sn.phy.ofdm.ResourceGridMapper(
    RESOURCE_GRID
)
```

这里把调制符号放到 OFDM 资源栅格中。

也就是：

将 QAM 符号分配到指定的时频资源单元，同时保留导频位置。

### 5.2 无线信道：OFDMChannel

```python
channel = sn.phy.channel.OFDMChannel(
    CDL,
    RESOURCE_GRID,
    add_awgn=True,
    normalize_channel=True,
    return_channel=True
)
```

这是整个通信系统的信道模块。

它主要完成三件事：

* 根据 CDL 模型生成无线信道。

* 将时域信道转换为频域信道响应。

* 对发射信号施加信道影响，并加入 AWGN 噪声。

接收信号可以简化表示为：

Y=HX+N

其中：

* ：发射信号。

* ：无线信道频率响应。

* ：加性高斯白噪声。

* ：接收信号。

这里有一个重要区别：

本章使用的是：

```python
OFDMChannel
```

而不是：

```python
TimeChannel
```

两者的区别：

| 模块          | 仿真方式 | 特点                |
| ----------- | ---- | ----------------- |
| OFDMChannel | 频域   | 假设每个 OFDM 符号内信道不变 |
| TimeChannel | 时域   | 可以模拟符号内信道变化及 ICI  |

ICI 是载波间干扰（Inter-Carrier Interference）。

当信道在一个 OFDM 符号持续时间内发生变化时，原本相互正交的子载波可能产生干扰。

因此，后续如果研究高速移动场景下的 OFDM 系统，可以进一步关注 TimeChannel。

### 5.3 接收端：LS 信道估计

```python
ls_est = sn.phy.ofdm.LSChannelEstimator(
    RESOURCE_GRID,
    interpolation_type="nn"
)
```

这是你尤其需要掌握的部分。

LS（Least Squares）即最小二乘信道估计。

接收端已知发射端导频符号 ，接收到对应信号 。

根据：

Y_p=H_pX_p+N_p

可以得到 LS 信道估计：

\\boxed{
\\hat H_p^{LS}=\\frac{Y_p}{X_p}
}

这里的除法是逐元素复数除法。

由于导频只分布在部分时频资源单元上，所以还需要对其他位置进行插值。

本例使用：

```python
interpolation_type="nn"
```

即最近邻插值（Nearest Neighbor）。

这意味着接收端利用附近已知的导频信道估计值，填补其他位置的信道估计。

![Channel estimation in OFDM systems operating under high mobility using Wiener filter combined basis expansion model | Journal on Wireless Communications and Networking | Springer Nature Link](https://images.openai.com/static-rsc-4/aCDrdA76mOAerGzpWuBLpSXPkPrOdfNyjG-OQaaAWOt7mGiMswg-xqGQx-UHUFsjIpR_xwjKKHcMtXeyHW5X66H33IGzBOzxPUivaZPcGpd75SUBKAS27-upu2cI2e2Fw8o_WNGdRggQzU0kVIgmu0oRCEgtYlYweWaesIA3_fhKxh7euRPRvmQ7XjNlh12n?purpose=fullsize)

这一步与后续 AI 信道估计研究直接相关。

你未来可以把：

\\hat H^{LS}

作为神经网络的输入，让神经网络学习更准确的信道响应：

\\hat H^{AI}=f_\\theta(\\hat H^{LS})

然后比较 LS 和 AI 信道估计的性能。

### 5.4 接收端：LMMSE 均衡

```python
lmmse_equ = sn.phy.ofdm.LMMSEEqualizer(
    RESOURCE_GRID,
    STREAM_MANAGEMENT
)
```

为什么需要均衡？

因为无线信道会对发送信号造成幅度和相位变化。

接收信号：

Y=HX+N

我们希望根据 和估计的信道 ，恢复原始信号 。

最简单的思路是 Zero Forcing（ZF）：

\\hat X_{ZF}=\\frac{Y}{\\hat H}

但是当信道增益很小时，ZF 可能严重放大噪声。

因此这里使用 LMMSE（Linear Minimum Mean Square Error）。

在单输入单输出情况下，其典型形式为：

\\hat X_{LMMSE}
=
\\frac{\\hat H^\*}
{|\\hat H|^2+\\sigma_n^2/E_s}Y

其中：

* ：信道估计的复共轭。

* ：噪声功率。

* ：发送符号能量。

LMMSE 在恢复信号时兼顾信道失真和噪声影响。

本例是 SIMO 系统，实际实现还需要综合四根接收天线的信息。

这里需要建立一个认识：信道估计解决的是 H 是多少，均衡解决的是如何利用 H 恢复 X。

### 5.5 解调与译码

接下来：

```python
demapper = sn.phy.mapping.Demapper(
    "app",
    "qam",
    NUM_BITS_PER_SYMBOL
)
```

将均衡后的软符号转换为比特的对数似然比（LLR）。

LLR 可以理解为：

接收端认为某个比特为 0 或 1 的相对可信程度。

然后：

```python
decoder = sn.phy.fec.ldpc.LDPC5GDecoder(
    encoder,
    hard_out=True
)
```

使用 5G LDPC 译码器恢复原始信息比特。

完整过程：

Y
\\rightarrow \\hat H
\\rightarrow \\hat X
\\rightarrow LLR
\\rightarrow \\hat b

至此，整个通信链路就搭建完成了。

### 六、Creating an End-to-End System：封装完整系统

前面我们分别定义了各个模块。

现在将它们组合到一个类中：

```python
class OFDMSystem(sn.phy.Block):
```

这段代码值得重点学习。

为什么不直接把前面的代码全部放在一起？

因为 Sionna 希望我们把整个通信链路封装成一个可以重复调用的系统模块。

这里的 `Block` 继承自：

```python
torch.nn.Module
```

因此它能够融入 PyTorch 的模块体系。

主要有两个函数：

### 1\. `__init__()`

负责初始化通信系统中的模块。

例如：

```python
self.encoder = ...
self.mapper = ...
self.channel = ...
self.ls_est = ...
self.lmmse_equ = ...
self.demapper = ...
self.decoder = ...
```

### 2\. `call()`

负责定义一次完整的前向传播。

```python
def call(self, batch_size, ebno_db):
```

这里输入：

* `batch_size`：一次仿真的样本数量。

* `ebno_db`：信噪比参数。

最终返回：

```python
return bits, bits_hat
```

即：

* `bits`：原始信息比特。

* `bits_hat`：接收端恢复的信息比特。

这样就能够直接计算 BER 和 BLER。

### 七、Running the Simulation：BER 性能仿真

这是本章的最后一部分，也是通信系统性能分析的重要环节。

### 7.1 两种信道估计方式

本章比较两种情况：

第一种：LS Channel Estimation

```python
model_ls = OFDMSystem(False)
```

接收端通过导频进行信道估计。

第二种：Perfect CSI

```python
model_pcsi = OFDMSystem(True)
```

接收端直接获得真实信道信息。

这里的 Perfect CSI 是一种理想化参考条件。

现实中，接收机不可能直接获得完全准确的信道状态信息。

因此，Perfect CSI 可以看成性能参考上限。

两种系统的区别主要体现在：

```python
if self.perfect_csi:
    h_hat, err_var = h_freq, 0.
else:
    h_hat, err_var = self.ls_est(y, no)
```

其他模块基本保持不变。

这就使得我们可以比较：

信道估计误差究竟会对整个通信系统的性能造成多大影响？

### 7.2 BER 和 BLER

首先区分两个指标。

| 指标   | 全称               | 含义     |
| ---- | ---------------- | ------ |
| BER  | Bit Error Rate   | 比特错误率  |
| BLER | Block Error Rate | 数据块错误率 |

BER：

BER=
\\frac{\\text{错误比特数}}
{\\text{总传输比特数}}

BLER：

BLER=
\\frac{\\text{错误数据块数}}
{\\text{总数据块数}}

例如，传输 100 个数据块，其中 10 个数据块存在至少一个错误：

BLER=10\\%

即使每个错误数据块只错了一个比特，它仍然算作一个错误数据块。

### 7.3 BER 仿真结果分析

![Part 3: Advanced Link-level Simulations — Sionna 2.1.0](https://images.openai.com/static-rsc-4/6jZ0_ZX_2LpUzYKHKMsG--0pm6UykSu7gGRMdXyVvQlUp37khjNH3cZ1uCwMfrerUVpSZ5YQtaEDIyf78O0GB1H1A40ZXJZd4Qcu2sA_TtuAnLYrSnr1FKgrmzilazfLhtFcX2HH08iJeKNGlPSSPvTTK6jYuX50xL6cRgDABOnY79zDNMs5xGUq0qEvBZPh?purpose=fullsize)

从你提供的结果中可以看到：

| Eb/N0     | LS BER    | Perfect CSI BER |
| --------- | --------- | --------------- |
| -8 dB     | 0.43139   | 0.28008         |
| -5.105 dB | 0.37682   | 0.17203         |
| -3.368 dB | 0.32840   | 0.0001663       |
| -2.789 dB | 0.30935   | 0               |
| 0.105 dB  | 0.14742   | 未提供             |
| 1.263 dB  | 0.0004947 | 未提供             |

可以观察到：

Perfect CSI 的性能明显优于 LS 信道估计。

原因是：

Perfect CSI 直接知道真实信道，不需要承担信道估计误差。

而 LS 估计会受到以下因素影响：

* 导频数量有限。

* 接收噪声。

* 信道时变。

* 插值误差。

这些误差会传递到均衡器，最终影响比特恢复。

### 一个值得注意的细节

仿真结果中的：

```text
BER = 0
BLER = 0
```

不代表系统在这个信噪比下绝对不会发生错误。

它只表示：在当前 Monte Carlo 仿真的样本范围内，没有观察到错误。

例如：

```python
max_mc_iter=100
```

限制了最大 Monte Carlo 仿真次数。

因此，不能把有限次仿真的零错误直接理解为理论 BER 等于零。

### 八、Part 3 对你研究 AI 通信有什么意义？

这一部分需要结合你的研究方向理解。

你目前关注的是：

* AI 信道估计。

* AI 信号检测。

* OFDM 通信系统。

* SDR 实际收发链路。

Part 3 恰好给出了一个可以开展这些研究的基础平台。

我把它拆成三个研究入口。

### 8.1 AI Channel Estimation：AI 信道估计

传统方法：

Y_p\\rightarrow LS\\rightarrow \\hat H_{LS}

AI 方法：

Y_p\\rightarrow Neural\\ Network
\\rightarrow \\hat H_{AI}

也可以先使用 LS 估计，再利用神经网络进行优化：

\\hat H_{LS}\\rightarrow NN
\\rightarrow \\hat H_{AI}

比较：

* LS。

* LMMSE 信道估计。

* CNN 信道估计。

* Transformer 信道估计。

评价指标：

NMSE=
\\frac{\\mathbb E\[\\|\\hat H-H\\|^2\]}
{\\mathbb E\[\\|H\\|^2\]}

这里的 NMSE 是归一化均方误差。

还可以比较不同方法下的 BER 和 BLER。

### 8.2 AI Signal Detection：AI 信号检测

传统接收端：

Y\\rightarrow LMMSE\\rightarrow \\hat X

AI 接收端：

Y,H\\rightarrow Neural\\ Detector
\\rightarrow \\hat X

可以研究神经网络如何替代传统的均衡与检测模块。

例如：

* CNN Detector。

* MLP Detector。

* Model-driven Neural Detector。

* Deep Unfolding Detector。

这里需要注意：信道估计与信号检测是两个相关但不同的研究问题，不要一开始就把它们全部放进一个神经网络。

### 8.3 Learned Receiver：学习型接收机

这也是 Part 4 将要涉及的内容。

传统通信系统是：

\\text{Channel Estimation}
\\rightarrow
\\text{Equalization}
\\rightarrow
\\text{Demapping}

Learned Receiver 则可以直接利用神经网络从接收信号中恢复发送比特：

Y\\rightarrow Neural\\ Network
\\rightarrow \\hat b

![Effect of DNN Approximation for Channel Estimation and Signal Detection on OFDM Applications | IIETA](https://images.openai.com/static-rsc-4/J6vAlpjbx6QwophjrQcg2kqiU_tJ-TS3_dYSm3LgLxwKfr8qQr0WwEjS-853H5ovQfcUkk5havuf1NU7EDZw99GIIuk7wP3L9SCmdkdudoDe1V6RAF1G6-so6b8Nf5gzmQm33w-JlajKLYObMSkHp89CII4x8Im6F4JGiSjWXmYVSIpGH_-b23izJ39iOzaV?purpose=fullsize)

这实际上是在探索：

能否通过数据驱动的方法，让接收机自动学习如何处理信道失真、噪声和干扰？

### 九、建议你完成的 Part 3 实践任务

不要只看懂代码就进入 Part 4。Part 3 最重要的是能够独立修改通信系统的参数，并理解它们对 BER 的影响。

我建议按照下面的顺序实践。

Part 3 实践清单

建议顺序

完成进度

0/6

任务 1：理解完整通信链路

画出发射端、信道和接收端的模块结构。

任务 2：修改天线数量

将 BS 天线从 4 根改为 2 根、8 根，观察 SIMO 性能变化。

任务 3：修改 CDL 信道

比较 CDL-A、CDL-C、CDL-D 的信道特征。

任务 4：修改导频配置

改变导频 OFDM 符号位置，观察 LS 估计效果。

任务 5：比较 LS 与 Perfect CSI

重新运行 BER 仿真，分析两者的性能差距。

任务 6：导出信道数据

保存真实信道 H、LS 信道估计 H_hat 和对应标签，作为后续 AI 实验的数据基础。

### 十、Part 1–3 的学习脉络总结

最后，把前三章放在一起理解：

| 阶段     | 学习内容              | 核心能力            |
| ------ | ----------------- | --------------- |
| Part 1 | 基础通信系统            | 搭建 OFDM 仿真      |
| Part 2 | 可微分通信系统           | 使用 SGD 优化通信参数   |
| Part 3 | 高级链路级仿真           | 搭建 5G NR 风格通信链路 |
| Part 4 | Learned Receivers | 使用神经网络实现接收机     |

我认为，你在 Part 3 最应该掌握的不是每个 API 的调用方式，而是以下四个知识点：

* Resource Grid：理解 OFDM 时频资源如何组织，以及导频如何分配。

* CDL Channel：理解 3GPP 多径信道的生成机制，特别是复数路径增益和传播时延。

* LS + LMMSE：理解传统接收机如何进行信道估计和信号均衡。

* BER Simulation：理解如何通过链路级仿真评估通信系统性能。

这四个部分构成了你后续开展 AI 通信研究的基础。

我的建议：先不要急着进入 Part 4。 最好先独立跑通 Part 3，并完成 LS 与 Perfect CSI 的 BER 对比。随后进入 Part 4 时，你就能清楚地知道神经网络究竟在替代传统接收机中的哪一个环节，以及为什么需要它。
