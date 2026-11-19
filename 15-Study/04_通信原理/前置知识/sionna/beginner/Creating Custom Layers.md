这三个问题分别对应 AI 通信中的三个重要基础：信号表示、软信息检测、神经网络架构设计。我们结合传统通信原理和这段 Sionna 代码来理解。

### 1\. 为什么复数信号要拆成 I/Q 两个实数？

### （1）从通信信号本身理解

数字通信中，调制后的基带信号通常用复数表示：

y=I+jQ

其中：

* ：同相分量（In-phase）。

* ：正交分量（Quadrature）。

* ：虚数单位。

例如，QPSK 的四个星座点可以表示为：

\\begin{aligned}
s_1&=1+j\\\\
s_2&=1-j\\\\
s_3&=-1+j\\\\
s_4&=-1-j
\\end{aligned}

实际上，每个复数星座点都对应二维平面上的一个点。

![Understanding Constellation Diagrams: QPSK, QAM, EVM, and Noise Effects](https://images.openai.com/static-rsc-4/LWTaHa4nTLceEP1_i1y4iAy_Uito_-M-k1oiOlS2za1bsZDghc-G73qtqPgubwKpbHBXw8iJKmj-y32o-PTmInYr5gZUUD1-ToO2wwhDKaOD88tT_dyF7HoqJfFk0ES-UMcLkHcKR_VP1nrmihJrcx6AbXZvfFhaXT5ZYVc9uocwuR83GWcnNHekMZm_w_oT?purpose=fullsize)

所以，复数信号并不是包含了某种无法处理的特殊信息，而是用一种紧凑的方式表示两个实数维度。

### （2）为什么 PyTorch 要拆开？

PyTorch 的普通 `nn.Linear` 主要针对实数特征进行计算。

因此，代码：

```python
nn_input = torch.stack([y.real, y.imag], dim=-1)
```

实际上完成了：

y\\in\\mathbb C
\\quad\\longrightarrow\\quad
\[I,Q\]\\in\\mathbb R^2

这样神经网络就可以利用普通的全连接层处理通信信号。

例如：

```python
y = 0.7 + 0.3j
```

经过转换：

```python
nn_input = [0.7, 0.3]
```

### （3）为什么不直接使用复数神经网络？

当然可以。

复数神经网络（Complex-valued Neural Network）可以直接处理复数权重和复数特征。

但它需要专门设计复数运算、激活函数和训练机制。

对于这个入门案例，将 I/Q 拆成两个实数更简单，也更容易使用成熟的 PyTorch 工具。

核心结论：拆分 I/Q 不会丢失信号信息，而是将复数信号转换成神经网络能够直接处理的二维实数特征。

### 2\. 为什么输出 LLR，而不是直接输出 0 或 1？

这是三个问题中最重要的一个，因为它直接关系到数字通信中的软判决（Soft Decision）。

### （1）先理解硬判决

假设接收端需要判断发送的比特究竟是 0 还是 1。

传统硬判决直接给出结果：

\\hat b=
\\begin{cases}
0,& P(b=0|y)>P(b=1|y)\\\\
1,& P(b=1|y)>P(b=0|y)
\\end{cases}

例如：

接收到某个信号后，系统认为：

P(b=0|y)=0.51P(b=1|y)=0.49

那么硬判决输出：

\\hat b=0

但这个判断其实并不可靠。

再看另一种情况：

P(b=0|y)=0.99P(b=1|y)=0.01

硬判决仍然输出 0。

问题来了：

这两种情况虽然判决结果相同，但它们的置信程度明显不同。

硬判决丢失了这种信息。

### （2）LLR 保留置信程度

LLR（Log-Likelihood Ratio，对数似然比）的定义：

LLR=\\ln\\frac{P(b=0|y)}{P(b=1|y)}

我们计算刚才两个例子：

情况 A：判断不确定

LLR=\\ln\\frac{0.51}{0.49}
\\approx 0.040接近 0，置信度较低

情况 B：判断非常确定

LLR=\\ln\\frac{0.99}{0.01}
\\approx 4.595较大的正值，倾向于 0

如果更倾向于比特 1

LLR=\\ln\\frac{0.01}{0.99}
\\approx -4.595较大的负值，倾向于 1

所以：

| LLR   | 含义       |
| ----- | -------- |
| 大于 0  | 更倾向于 0   |
| 小于 0  | 更倾向于 1   |
| 接近 0  | 不确定性较高   |
| 绝对值较大 | 判断置信程度较高 |

### （3）为什么通信系统需要软信息？

因为数字通信接收机通常不止有解映射，还会有信道译码。

例如，采用 LDPC 编码的通信系统：

接收信号

Demapper

输出 LLR 软信息

LDPC Decoder

利用校验约束进行迭代译码

恢复发送比特

LDPC 译码器可以利用每个比特的置信程度，结合校验矩阵中的约束进行迭代更新。

如果只给它 0 或 1，就丢失了接收端原本掌握的可靠性信息。

因此，软判决通常比硬判决更有利于获得较好的译码性能。

### （4）为什么最后一层不使用 ReLU？

回到代码：

```python
self.dense_3 = nn.Linear(64, NUM_BITS_PER_SYMBOL)
```

这里没有使用 ReLU。

因为 LLR 既可能为正，也可能为负。

如果使用 ReLU：

ReLU(x)=\\max(0,x)

那么所有负数都会变成 0，网络就无法表达倾向于比特 1 的负 LLR。

核心结论：Neural Demapper 输出 LLR，是为了保留比特判决的置信程度，为后续信道译码提供更充分的信息。

### 3\. 为什么每个符号独立处理，而不是整个 OFDM 数据块联合处理？

这个问题涉及神经网络架构设计。

### （1）当前代码实际上做了什么？

看这行代码：

```python
nn_input = torch.stack([y.real, y.imag], dim=-1)
```

输入形状：

\[B,N,2\]

其中：

* ：数据块数量。

* ：每个数据块的符号数量。

* 2：I/Q 两个特征。

接下来：

```python
z = F.relu(self.dense_1(nn_input))
```

PyTorch 的 `nn.Linear` 默认只对最后一个维度进行线性变换。

因此：

\[B,N,2\]\\rightarrow\[B,N,64\]

它并不会把整个数据块的 100 个符号合并起来计算，而是对每个符号分别执行相同的网络。

### （2）用具体例子理解

假设一个 OFDM 数据块包含 4 个接收符号：

Y=\[y_1,y_2,y_3,y_4\]

当前网络的处理方式：

Symbol-wise Demapper

y1

I/Q

y2

I/Q

y3

I/Q

y4

I/Q

同一个网络

共享参数

同一个网络

共享参数

同一个网络

共享参数

同一个网络

共享参数

LLR1

LLR2

LLR3

LLR4

数学表达：

LLR_i=f_\\theta(y_i)

其中：

* ：神经网络。

* ：网络参数。

* ：符号索引。

所有符号共享同一个网络参数 ，但计算过程相互独立。

### （3）如果对整个数据块联合处理呢？

另一种方式是：

\[ y_1,y_2,\\ldots,y_N\]
\\longrightarrow f_\\theta
\\longrightarrow \[LLR_1,\\ldots,LLR_N\]

这意味着网络在处理某个符号时，可以参考其他符号的信息。

例如，可以使用：

* CNN：学习局部符号之间的关联。

* RNN / LSTM：学习序列中的时间关联。

* Transformer：利用注意力机制学习不同符号之间的关联。

![Exploration of How Transformers Work in AI<!-- -->](https://images.openai.com/static-rsc-4/sysSLHwbgNUWJtBncuXUl0mKjGXrwa6LkJHpFgiNuySEBLxLQkSb2vDdZ6H_UR2cFkIpMGhOyJXcCwF3SDZeM7neBHUKUzs-Xp-bH-hsGEqYWAzWSwuvvmgDO7c6Oq7KB1FKM3JavbRNT8ARIE6gQJhcjGU_lwH6eUCDsUqupFJSqTVNPKDMpy7gZ4Enjgz2?purpose=fullsize)

但是，联合处理并不一定总是更好。

它需要考虑更多因素：

| 比较维度  | 逐符号网络     | 联合网络         |
| ----- | --------- | ------------ |
| 输入    | 单个符号的 I/Q | 整个符号序列       |
| 参数共享  | 是         | 视架构而定        |
| 符号关联  | 不直接建模     | 可以建模         |
| 计算复杂度 | 通常较低      | 通常较高         |
| 适用场景  | 独立符号检测    | 存在时序或结构关联的场景 |

### （4）为什么这个案例选择逐符号处理？

主要有三个原因：

* 结构简单：可以先研究神经网络能否学习传统解映射器的功能。

* 参数共享：不同符号使用同一套网络参数，降低模型规模。

* 容易训练：每个符号都可以作为独立训练样本，不必先学习复杂的序列关系。

但这里有一个重要的通信原理问题：

在理想的平坦信道、正确均衡且噪声独立的情况下，逐符号解映射通常已经足够。

而在存在信道记忆、符号间干扰（ISI）、残余频偏、相关噪声等情况下，利用符号之间的关联可能带来额外收益。

### 4\. 把三个问题联系起来

你可以把它们理解成一个完整的 AI 接收机设计逻辑：

* 信号表示：输入如何表示？

    复数通信信号转换为 I/Q 两个实数特征。

    y\\rightarrow\[I,Q\]

* 判决方式：输出应该是什么？

    不仅预测比特，还要预测比特的置信程度。

    y\\rightarrow LLR

* 网络架构：如何利用信号信息？

    可以逐符号处理，也可以联合建模符号间的关联。

    LLR_i=f_\\theta(y_i)

### 5\. 对你后续研究 AI 通信的启发

结合你目前关注的 AI 信道估计和信号检测，我建议你进一步区分三个研究层次：

| 研究方向                  | 核心问题              | 典型方法                   |
| --------------------- | ----------------- | ---------------------- |
| AI Channel Estimation | 信道是什么？            | CNN、深度展开网络             |
| AI Signal Detection   | 发送了什么符号？          | Neural Detector、深度展开检测 |
| AI Demapping          | 每个比特有多大概率是 0 或 1？ | Neural Demapper        |

其中，当前案例属于第三种。

一个值得你思考的研究问题：

如果把当前 Neural Demapper 的输入从均衡后的单个复数符号，扩展为接收符号、信道估计值和噪声方差三个部分：

f_\\theta(y,\\hat h,\\sigma^2)

网络是否能更好地适应不同信道条件？

这就涉及一个重要方向：信道状态信息感知的神经网络接收机（CSI-aware Neural Receiver）。

它比单纯学习星座点分类更接近实际无线通信系统中的研究问题。
