Demapper 的核心原理是：根据接收到的复数信号，计算它属于不同星座点的可能性，再把这些可能性转换成每个比特的 LLR。

这里需要先纠正一个容易混淆的概念：

Demapper 严格来说不是信道译码器（Decoder），而是软解调器（Soft Demodulator）。它不负责纠正编码错误，而是估计发送端可能发送了哪些比特。

我们以 16-QAM 和 AWGN 信道为例，推导它的实现过程。

### 一、Demapper 接收到了什么？

假设发射端使用 16-QAM。

![Intro to Digital Signal Processing (DSP) | John-Gentile.com](https://images.openai.com/static-rsc-4/L7AwhGhqameQA79vPKP-IeCEqu22sjbnxHAKQAwhlhtSPACGks1BAB7eWc6PNO7sNFirzlOrj_Q2mIGWDeJs5HrWEnXKgzE8AEXV_eA8KNLyMZ9cHDlDDvkVlf4TBNY-VYbWnbaVhr9G0EBSf-uUUjZ7VbvqOPzq_4KcfjnICC3UucspPunhh-kCN8BJ4lBm?purpose=fullsize)

16-QAM 一共有 16 个星座点：

M=16=2^4

每个星座点对应 4 个比特。

假设发送端发送：

b=\[1011\]

经过 Mapper，得到一个复数星座点：

x=x_{1011}

然后经过 AWGN 信道：

y=x+n

接收端得到的 通常不会恰好落在原来的星座点上。

例如：

y=0.9+1.2j

Demapper 的任务就是根据这个 ，推断原来的 4 个比特。

### 二、第一步：计算接收信号与所有星座点的距离

首先，Demapper 知道发射端使用的是 16-QAM，因此它知道全部 16 个候选星座点。

假设星座点集合为：

\\mathcal C=\\{x_0,x_1,\\ldots,x_{15}\\}

对于接收到的信号 ，计算它与每个星座点之间的欧氏距离：

\\boxed{d_i^2=|y-x_i|^2}

例如：

![FA201A15 シンボル誤り率とビット誤り率の関係 | さて、雨の日は勉強でもするか。](https://images.openai.com/static-rsc-4/cWuqoWN5ELC6acbiq53_IYV8OhXqmc03WSQnu0vWNc_AGxW2XVU26_o6zBfckQI1Kkz4Tc5GmsAj86D9oAhkAAmqooVd-sIyAMw1QDt3dlOHj47sn2MkvSZUQlcfbwlRKky3aJHv8eQRDSFvr05BeUPFBt0p5JNWaJ-xbNdW6vVL2DL0CZXrRgTKCsmn4mdG?purpose=fullsize)

距离越小，说明接收信号越接近对应的理想星座点。

但是，Demapper 并不一定直接选择最近的星座点。因为它还可以保留概率信息。

### 三、第二步：计算每个星座点的似然概率

这里就涉及概率论。

AWGN 信道模型为：

y=x+n

假设复噪声满足：

n\\sim\\mathcal{CN}(0,N_0)

那么接收信号在给定发送符号 时的条件概率密度为：

\\boxed{
P(y|x_i)=
\\frac{1}{\\pi N_0}
\\exp\\left(-\\frac{|y-x_i|^2}{N_0}\\right)
}

这个公式非常重要。

它说明：

* 如果 离 很近，概率较大。

* 如果 离 很远，概率较小。

* 噪声越大，接收信号的不确定性越高。

因此，Demapper 可以根据接收信号和噪声方差，计算 16 个候选星座点的似然概率。

### 四、第三步：从星座点概率转换成比特概率

这是 Demapper 最关键的步骤。

前面我们得到的是：

P(y|x_i)

但我们真正需要的是每个比特为 0 或 1 的概率。

假设 16-QAM 中，每个星座点对应 4 个比特：

b=\[b_1,b_2,b_3,b_4\]

现在只考虑第一个比特。

我们将 16 个星座点分成两组：

* 第一组：第一个比特为 0。

* 第二组：第一个比特为 1。

![Understanding Constellation Diagrams: QPSK, QAM, EVM, and Noise Effects](https://images.openai.com/static-rsc-4/khaQWqmOGB3ESWv60hf1V5LdH0xBW89is7WBGh6_OEVF-znm5vwoTmX9AMOJR8BkHmZ3_RBBHD6hhvHCA6EEFmHnwCOkbT5SGcJjls9vLa8PBDkRNDnBfk1Y442KokBDKhvO9oEdiKHeSPQpt3_cx5eY0YOgxtdjoaaSOw8DVd3J4r2FWdWGX1JAOB9ygFiP?purpose=fullsize)

如果采用等概率比特先验，那么：

P(b_1=0|y)
\\propto
\\sum_{x_i\\in\\mathcal C_0}P(y|x_i)P(b_1=1|y)
\\propto
\\sum_{x_i\\in\\mathcal C_1}P(y|x_i)

其中：

* ：第一个比特为 0 的星座点集合。

* ：第一个比特为 1 的星座点集合。

为什么这里要使用求和？

因为接收信号可能来自这一组中的任何一个星座点。

我们并不需要先确定它究竟是哪一个星座点，而是把所有符合比特条件的候选情况综合起来。

对于 16-QAM，每一组包含 8 个星座点。

### 五、第四步：计算 LLR

有了两组概率，就可以计算 LLR：

\\boxed{
LLR(b_k)=
\\ln\\frac{P(b_k=0|y)}
{P(b_k=1|y)}
}

将前面的概率表达式代入：

LLR(b_k)=
\\ln
\\frac{
\\sum\\limits_{x_i\\in\\mathcal C_{k,0}}
\\exp(-|y-x_i|^2/N_0)
}{
\\sum\\limits_{x_i\\in\\mathcal C_{k,1}}
\\exp(-|y-x_i|^2/N_0)
}

这里忽略了分子分母相同的归一化常数。

对于 16-QAM，一个接收符号需要分别计算：

LLR(b_1),LLR(b_2),LLR(b_3),LLR(b_4)

因此：

一个复数接收符号，最终会输出 4 个 LLR。

### 六、Sionna 的 Demapper 实际做了什么？

回到你之前的代码：

```python
self.demapper = sionna.phy.mapping.Demapper(
    "app",
    constellation=self.constellation
)
```

这里的 `"app"` 表示 APP（A Posteriori Probability）解映射。

它主要完成以下操作：

输入接收信号 y

复数信号

计算候选星座点距离

计算似然概率

按照比特标签分组

分别计算比特为 0 和 1 的概率

计算 LLR

输出每个比特的软信息

这里还有一个区别：

| 解映射方式   | 原理                  |
| ------- | ------------------- |
| APP     | 对每组星座点的概率求和，再计算 LLR |
| Max-Log | 用每组中概率最大的星座点近似概率求和  |

Max-Log 的 LLR 可以近似为：

LLR(b_k)\\approx
\\frac{
\\min\\limits_{x_i\\in\\mathcal C_{k,1}}|y-x_i|^2
-
\\min\\limits_{x_i\\in\\mathcal C_{k,0}}|y-x_i|^2
}{N_0}

它计算量更小，但属于近似算法。

### 七、动手验证：观察 Demapper 的输出

你可以直接在当前 Sionna Notebook 中运行下面的代码。

```python
# 创建 16-QAM 系统
model = UncodedSystemAWGN(
    num_bits_per_symbol=4,
    block_length=1024
)

# 运行一次仿真
bits, llr = model(
    batch_size=1,
    ebno_db=10.0
)

# 根据 LLR 进行硬判决
bits_hat = (llr < 0).int()

print("原始比特：", bits[0, :20])
print("接收LLR：", llr[0, :20])
print("判决比特：", bits_hat[0, :20])

# 计算 BER
ber = (bits != bits_hat).float().mean()
print("BER:", ber.item())
```

你会看到三个结果：

* `bits`：发射端实际发送的比特。

* `llr`：接收端对每个比特的可靠性判断。

* `bits_hat`：根据 LLR 正负号得到的硬判决结果。

### 八、进一步理解：为什么这对 AI 通信很重要？

你现在学到的 Demapper 实际上是一个基于数学模型的传统接收机模块。

它依赖三个已知条件：

* 星座图已知。

* 信道模型已知。

* 噪声方差已知。

但在真实无线环境中，信道可能存在多径衰落、频率选择性衰落、相位偏移等问题。

这时，传统解映射器的性能可能受到影响。

AI 通信研究中，一个重要方向就是：

\\text{接收信号}
\\longrightarrow
\\boxed{\\text{Neural Demapper}}
\\longrightarrow
\\text{LLR}

让神经网络学习从接收信号到软信息的映射关系。

建议你下一步研究一个问题：传统 Demapper 已经有明确的概率公式，为什么还需要神经网络来实现 Demapper？

这个问题会自然引出 Neural Receiver、信道估计和端到端通信系统。


## 添加前向纠错
Polar码
LDPC码
![[Pasted image 20261119145441.png]]
