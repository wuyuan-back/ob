### Sionna Tutorial Part 2：Differentiable Communication Systems（可微分通信系统）

这一章是 Sionna 入门教程中非常重要的一部分。

如果说 Part 1 主要解决的是如何使用 Sionna 搭建和仿真通信系统，那么 Part 2 就开始进入 AI 通信的核心问题：

如何将传统通信系统与神经网络结合，并通过梯度下降优化通信系统中的参数？

本章主要围绕三个主题展开：

* Gradient Computation Through End-to-end Systems：端到端通信系统中的梯度计算。

* Creating Custom Layers：创建自定义神经网络层。

* Setting up Training Loops：构建模型训练循环。

### 一、本章整体框架

### 1.1 传统通信系统与可微分通信系统

先回顾一个传统数字通信系统：

Bits（比特源）

Mapper（调制映射）

Channel（信道）

Demapper（解调）

Recovered Bits（恢复比特）

传统通信系统中，Mapper、信道模型和 Demapper 通常采用人工设计的算法。

而可微分通信系统的思路是：

* 保留传统通信模块。

* 将部分模块替换为神经网络。

* 允许系统参数参与梯度计算。

* 通过训练优化通信系统的整体性能。

例如：

* 优化星座图的位置。

* 使用神经网络实现接收端解调。

* 联合优化发射端和接收端。

这就是 End-to-End Learning（端到端学习）的基本思想。

### 二、Gradient Computation Through End-to-end Systems

这一部分的核心是：如何让梯度从接收端一直反向传播到发射端？

### 2.1 搭建基础通信系统

教程首先构建一个简单的通信系统：

* 调制方式：64-QAM

* 信道模型：AWGN

* 编码：无编码

* 调制比特数：6 bit/symbol

为什么是 6？

因为：

$$ \\log_2 64=6 $$

一个 64-QAM 符号对应 6 个比特。

首先定义比特源：

```python
binary_source = sn.phy.mapping.BinarySource()
```

定义 64-QAM 星座：

```python
NUM_BITS_PER_SYMBOL = 6

qam_constellation = sn.phy.mapping.Constellation(
    "qam",
    NUM_BITS_PER_SYMBOL
)
```

这里最重要的是接下来这部分。

### 将星座点设置为可训练参数

```python
trainable_points = torch.stack([
    qam_constellation.points.real.clone(),
    qam_constellation.points.imag.clone()
], dim=0)

trainable_points.requires_grad_(True)
```

理解这段代码，需要先理解星座图。

![Scaling Factor in QAM system – Zack's Ad hoc Page](https://images.openai.com/static-rsc-4/BER3GcQ6FV9mFmS-NXrRKZc4h5mU88qzlIP-y7kwz-ZOhHeuunRV-CousT2xw_WlOhZoqBWdEFK7adIcGQzfIVogsgwLivVtc9I5_v_n8_Lk1vBk78vdLp5vRDhWrYMdmXQzWG0unqDpgtlO-hUgihkkc10vyk4PAB8TTk72Ho1RSnQNjfZr9KPe3hme8CMc?purpose=fullsize)

64-QAM 包含 64 个星座点，每个点对应一个复数：

$$ s_i=I_i+jQ_i $$

其中：

* ：同相分量。

* ：正交分量。

原本的星座点由固定的 QAM 规则决定。

现在，教程把它们拆成实部和虚部两个张量：

$$ P= \\begin I_1&I_2&\\cdots&I_64\\ Q_1&Q_2&\\cdots&Q_64 \\end $$

其维度为：

```python
torch.Size([2, 64])
```

关键代码：

```python
trainable_points.requires_grad_(True)
```

它告诉 PyTorch：

这个张量是需要参与梯度计算的变量。

于是，64 个星座点的位置就不再完全固定，而是可以通过训练进行调整。

接下来使用自定义星座：

```python
constellation = sn.phy.mapping.Constellation(
    "custom",
    num_bits_per_symbol=NUM_BITS_PER_SYMBOL,
    points=torch.complex(
        trainable_points[0],
        trainable_points[1]
    ),
    normalize=True,
    center=True
)
```

这里有两个参数：

| 参数             | 含义         |
| -------------- | ---------- |
| normalize=True | 对星座进行功率归一化 |
| center=True    | 对星座进行中心化   |

注意：归一化和中心化也会影响最终的星座点，因此实际优化受到这些约束的影响。

### 2.2 完成信号传输

接下来构建 Mapper、Demapper 和 AWGN 信道：

```python
mapper = sn.phy.mapping.Mapper(
    constellation=constellation
)

demapper = sn.phy.mapping.Demapper(
    "app",
    constellation=constellation
)

awgn_channel = sn.phy.channel.AWGN()
```

整个信号处理过程：

```python
bits = binary_source([BATCH_SIZE, 1200])

x = mapper(bits)

y = awgn_channel(x, no)

llr = demapper(y, no)
```

各变量含义：

| 变量   | 含义              |
| ---- | --------------- |
| bits | 原始发送比特          |
| x    | 调制后的复数符号        |
| y    | 经过 AWGN 信道的接收符号 |
| llr  | 接收端计算出的软信息      |

其中：

* `BATCH_SIZE = 128`：每次并行处理 128 个数据块。

* `1200`：每个数据块包含 1200 个比特。

### AWGN 信道模型

接收信号可以表示为：

$$ y=x+n $$

其中：

$$ n\\sim\\mathcal(0,N_0) $$

这里的 表示复高斯白噪声。

教程设置：

```python
EBN0_DB = 17.0
```

并通过：

```python
no = sn.phy.utils.ebnodb2no(
    ebno_db=EBN0_DB,
    num_bits_per_symbol=NUM_BITS_PER_SYMBOL,
    coderate=1.0
)
```

将 转换为噪声功率谱密度对应的参数。

这里编码率为 1，因为没有使用信道编码。

### 2.3 定义损失函数：Binary Cross Entropy

接收端的任务是根据接收信号恢复发送比特。

教程使用二元交叉熵：

### $$ \\mathcal_

-\\frac1 \\sum_^ \\left\[ b_i\\log \\sigma(l_i) + (1-b_i)\\log(1-\\sigma(l_i)) \\right\] $$

其中：

* ：实际发送的比特，取值为 0 或 1。

* ：Demapper 输出的 LLR。

* ：Sigmoid 函数。

* ：参与计算的比特总数。

LLR 是 Log-Likelihood Ratio（对数似然比），表示接收端对比特取值的置信程度。

本教程中将 LLR 直接作为 BCE 的 logits 输入：

```python
loss = F.binary_cross_entropy_with_logits(
    llr,
    bits.float()
)
```

为什么不需要先进行 Sigmoid？

因为 `binary_cross_entropy_with_logits` 已经将 Sigmoid 和交叉熵计算整合在一起，可以获得更稳定的数值计算。

理解重点：

损失函数衡量的是接收端恢复比特的效果。

损失越小，说明模型输出的软信息越符合真实发送比特。

### 2.4 梯度计算：反向传播

这是本节最核心的知识。

传统通信系统中，我们通常只关心：

$$ bits\\rightarrow x\\rightarrow y\\rightarrow llr $$

现在，我们还需要计算：

$$ \\frac}

$$

也就是损失函数对星座点位置的梯度。

代码：

```python
loss.backward()

gradient = trainable_points.grad
```

这里发生了什么？

PyTorch 的 Autograd 会自动追踪计算过程中涉及可训练参数的运算，并通过链式法则计算梯度。

例如：

$$ P\\rightarrow Mapper\\rightarrow x $$

$$ x\\rightarrow AWGN\\rightarrow y $$

$$ y\\rightarrow Demapper\\rightarrow LLR $$

$$ LLR\\rightarrow BCE\\rightarrow Loss $$

最终：

### $$ \\frac

\\frac \\frac \\frac \\frac $$

这意味着：

即使 AWGN 和 Demapper 本身不是神经网络，只要它们的运算可以微分，梯度就能够穿过这些模块。

这是 Sionna 最重要的能力之一。

### 2.5 使用 Adam 更新星座点

获得梯度之后，就可以更新参数。

```python
optimizer = torch.optim.Adam(
    [trainable_points],
    lr=1e-2
)
```

执行：

```python
optimizer.step()
```

从数学角度看，最基本的梯度下降更新规则是：

$$ P_=P_t-\\eta\\nabla_P\\mathcal $$

其中：

* ：当前星座点。

* ：学习率。

* ：损失函数对星座点的梯度。

Adam 则进一步利用梯度的一阶矩和二阶矩估计调整更新步长。

本节最终观察到：

经过一次 SGD 更新，星座点的位置发生了轻微变化。

![Next-gen wireless chip boosts battery life and reduces signal errors - The Brighter Side of News](https://images.openai.com/static-rsc-4/Ih4WSUKgyqIc4E1GQapj47oa4pp7v1NotFhTLZtbgMyVREuKVc3s9cY3TWLoc9zlcF3oJa7YKQKdyxOUbtn1dnsd7pbCFbJg02W82eYUAIVZJ371Lvn-qjn2s4Y8osgSNWNhwhhJttblSznIhfpX03xfMkN5kQVAGEZg4ilMsaVlMlDNEHVphrzMBgsQ5c_s?purpose=fullsize)

这里并不是说星座点变化越大越好，而是通过训练寻找能够降低通信误差的星座布局。

### 三、Creating Custom Layers

上一部分实现了对传统通信系统参数的优化。

这一部分开始进入更加重要的内容：

如何自己编写神经网络，并将其作为通信系统中的一个模块？

### 3.1 PyTorch 的 nn.Module

教程采用 PyTorch 实现神经网络：

```python
class NeuralDemapper(nn.Module):
```

`nn.Module` 是 PyTorch 中定义神经网络模型的基础类。

一个神经网络通常包含：

* 网络层定义。

* 参数初始化。

* 前向传播函数。

教程设计了一个由三个全连接层组成的神经网络解调器。

### 3.2 Neural Demapper 网络结构

### Neural Demapper 架构

输入接收符号

y=I+jQ

复数输入，拆分为 I、Q 两个实数特征

Dense Layer 1

### 2 → 64

ReLU

Dense Layer 2

### 64 → 64

ReLU

Dense Layer 3

### 64 → 6

Linear / Logits

输出 LLR

\[b_1,b_2,b_3,b_4,b_5,b_6\]

为什么输入是 2，输出是 6？

因为：

* 输入：一个复数符号包含 I、Q 两个实数特征。

* 输出：64-QAM 每个符号对应 6 个比特。

### 代码解析

第一步：定义网络层。

```python
self.dense_1 = nn.Linear(2, 64)
self.dense_2 = nn.Linear(64, 64)
self.dense_3 = nn.Linear(64, NUM_BITS_PER_SYMBOL)
```

第二步：处理复数输入。

```python
nn_input = torch.stack(
    [y.real, y.imag],
    dim=-1
)
```

原始接收符号：

$$ y=I+jQ $$

转换为：

$$ y'=\[I,Q\] $$

第三步：进行前向传播。

```python
z = F.relu(self.dense_1(nn_input))

z = F.relu(self.dense_2(z))

z = self.dense_3(z)
```

最后一层没有使用 ReLU。

原因是输出需要作为 logits，即 LLR 使用，输出必须允许正值和负值。

第四步：调整输出维度。

```python
llr = z.reshape(y.shape[0], -1)
```

输出形状：

$$ \[BATCH_SIZE,1200\\times6\] $$

即：

$$ \[128,7200\] $$

这样就可以与原始比特张量进行损失计算。

### 四、构建端到端通信系统 End2EndSystem

前面只是单独定义了 Neural Demapper。

现在要将它整合到完整通信系统中。

### 4.1 系统结构

Binary Source

Trainable Constellation + Mapper

可训练星座图

AWGN Channel

传统信道模型

Neural Demapper

神经网络解调器

BCE Loss

梯度从 Loss 反向传播，更新可训练参数。

### 4.2 为什么要使用 nn.Parameter？

在模型中：

```python
self.points = nn.Parameter(
    torch.stack([
        qam_constellation.points.real.clone(),
        qam_constellation.points.imag.clone()
    ], dim=0)
)
```

与之前的：

```python
trainable_points.requires_grad_(True)
```

有什么区别？

| 方法                 | 作用             |
| ------------------ | -------------- |
| requires_grad=True | 让张量参与梯度计算      |
| nn.Parameter       | 将张量注册为模型的可训练参数 |

使用 `nn.Parameter` 后，PyTorch 可以自动将星座点纳入：

```python
model.parameters()
```

因此可以直接使用：

```python
optimizer = torch.optim.Adam(
    model_train.parameters()
)
```

统一优化整个模型的参数。

### 4.3 训练模式与评估模式

教程在 `End2EndSystem` 中设置了一个参数：

```python
self._training_mode = training
```

根据这个参数，模型会有不同的输出。

| 模式             | 输出         |
| -------------- | ---------- |
| training=True  | Loss       |
| training=False | bits 和 llr |

训练阶段需要损失函数来更新模型。

评估阶段则需要输出恢复比特的软信息，以计算 BER 和 BLER。

注意，这里使用的是教程自行设置的 `_training_mode`，并不是 PyTorch 的 `model.train()` 和 `model.eval()` 自动切换逻辑。

### 五、Benchmarking：模型性能评估

在训练之前，教程先比较两个系统：

* Baseline：传统 64-QAM Mapper + APP Demapper。

* Untrained Model：尚未训练的神经网络解调器。

### 5.1 什么是 BER 和 BLER？

通信系统性能评价最常用的两个指标。

BER（Bit Error Rate，比特误码率）

$$ BER=\\frac}} $$

BLER（Block Error Rate，块误码率）

$$ BLER=\\frac}} $$

二者区别：

* BER 衡量单个比特的传输准确性。

* BLER 衡量整个数据块是否出现错误。

例如，一个数据块包含 1200 个比特，只要其中一个比特错误，该数据块就被计为错误块。

### 5.2 未训练神经网络的表现

教程给出的结果：

Untrained Model

| Eb/N0    | Baseline BER | Untrained BER |
| -------- | ------------ | ------------- |
| 10 dB    | 0.0270       | 0.524         |
| 15 dB 左右 | 约 0.0006     | 约 0.524       |
| 20 dB    | 0            | 0.525         |

可以发现：

传统解调器随着信噪比增加，误码率不断下降。

而未经训练的神经网络解调器，BER 始终在 0.5 左右。

为什么？

因为神经网络的权重是随机初始化的，还没有学习到接收信号与比特之间的映射关系。

它的输出基本接近随机判断。

这说明：仅仅用神经网络替换传统解调器，并不能自动获得更好的通信性能。

### 六、Setting up Training Loops

现在正式训练神经网络。

### 6.1 训练过程

教程设置：

```python
NUM_TRAINING_ITERATIONS = 10000
```

训练次数为 10000 次，训练信噪比为：

$$ E_b/N_0=15\\text $$

优化器使用 Adam：

```python
optimizer = torch.optim.Adam(
    model_train.parameters()
)
```

完整训练流程：

```python
for i in range(NUM_TRAINING_ITERATIONS):

    optimizer.zero_grad()

    loss = model_train(BATCH_SIZE, 15.0)

    loss.backward()

    optimizer.step()

    if i % 100 == 0:
        print(loss.item())
```

逐行解释：

| 代码               | 功能         |
| ---------------- | ---------- |
| zero_grad()      | 清除上一次迭代的梯度 |
| model_train()    | 前向传播，计算损失  |
| loss.backward()  | 反向传播，计算梯度  |
| optimizer.step() | 更新模型参数     |

这里尤其需要理解：

为什么每次训练都要执行 `zero_grad()`？

因为 PyTorch 默认会累积梯度。如果不清零，本轮梯度就会与之前的梯度相加。

### 6.2 保存训练好的模型

```python
torch.save(
    model_train.state_dict(),
    'weights-neural-demapper.pt'
)
```

`state_dict()` 保存模型中的参数。

这样就不需要每次评估都重新训练。

之后重新创建模型：

```python
model = End2EndSystem(
    training=False
).to(sn.phy.config.device)
```

加载权重：

```python
model.load_state_dict(
    torch.load(
        'weights-neural-demapper.pt',
        weights_only=True
    )
)
```

最终就可以进行独立测试。

### 6.3 训练后的模型表现

Trained Model

| Eb/N0    | Baseline BER | Trained BER |
| -------- | ------------ | ----------- |
| 10 dB    | 0.0270       | 0.0258      |
| 15 dB 左右 | 约 0.0006     | 约 0.0007    |
| 20 dB    | 0            | 6.51×10⁻⁸   |

从结果可以看出：

* 训练后的神经网络已经能够完成解调。

* 其 BER 与传统解调器非常接近。

* 部分信噪比下表现略有差异。

需要注意，不能仅凭表格中某些点的数值就断言神经网络全面优于传统解调器。实际比较还需要考虑统计误差、训练条件和测试条件。

### 七、本章知识总结

### 7.1 核心知识点

| 知识点                     | 本章学到了什么        | 重要程度 |
| ----------------------- | -------------- | ---- |
| Differentiable System   | 通信系统模块可以参与梯度计算 |      |
| Trainable Constellation | 使用梯度下降优化星座点    |      |
| Autograd                | PyTorch 自动计算梯度 |      |
| BCE Loss                | 使用二元交叉熵评价解调结果  |      |
| Neural Demapper         | 用神经网络代替传统解调器   |      |
| nn.Module               | 创建自定义神经网络层     |      |
| nn.Parameter            | 注册可训练参数        |      |
| Adam                    | 优化网络参数         |      |
| BER / BLER              | 评价通信系统性能       |      |

### 7.2 这一章真正要理解的三个问题

问题一：为什么 Sionna 可以实现端到端训练？

因为 Sionna 的通信模块不仅可以执行信号处理，还支持在可微分运算路径上进行梯度传播。

问题二：神经网络在通信系统中承担什么任务？

它可以替代或者辅助传统通信算法，例如：

* 信道估计。

* 信号检测。

* 符号解调。

* 信道译码。

问题三：传统通信模块是否需要全部替换为神经网络？

不需要。

事实上，本章就展示了混合架构：

* Mapper：传统模块，但星座点可训练。

* AWGN：传统信道模型。

* Demapper：神经网络模块。

这正是 AI + 通信研究中非常重要的思路：结合传统通信理论与数据驱动方法。

### 八、结合你的 AI 通信研究方向：这一章有什么价值？

你之前确定的研究兴趣是 AI 信道估计与信号检测，并且计划使用 Sionna、TorchSig 和 SDR 硬件逐步建立实验平台。

这一章是你从传统通信仿真过渡到 AI 通信研究的基础。

我建议将后续学习分成三个阶段：

### 阶段一：理解本章基础

当前阶段

* 掌握 Mapper、Channel、Demapper。

* 理解 BCE、LLR 和 BER。

* 理解 Autograd 和反向传播。

* 能够独立实现 Neural Demapper。

    ### 阶段二：进入 OFDM 神经接收机

    下一阶段

* 学习 OFDM 调制解调。

* 理解导频与信道估计。

* 学习 LS、LMMSE 信道估计。

* 使用神经网络实现信道估计或信号检测。

    ### 阶段三：结合 SDR 实验

    研究实践

* 在 Sionna 中训练和测试神经接收机。

* 使用 GNU Radio 和 SDR 采集真实 IQ 数据。

* 对比理想仿真信道与真实无线信道。

* 分析模型在实际信道中的泛化能力。

### 8.1 一个值得你注意的区别

本章虽然介绍的是端到端通信系统，但当前实验实际上非常简单：

| 项目     | 本章实验        |
| ------ | ----------- |
| 调制方式   | 64-QAM      |
| 信道     | AWGN        |
| 信道编码   | 无           |
| 信道估计   | 不涉及         |
| OFDM   | 不涉及         |
| 神经网络任务 | 星座优化、神经网络解调 |

因此，不能把本章的实验直接等同于实际 OFDM 神经接收机。

真实 OFDM 系统还需要处理：

* 多径衰落。

* 子载波间干扰。

* 信道估计误差。

* 导频设计。

* 同步误差。

* 多普勒频移。

这些才是你后续研究 AI 信道估计和信号检测时需要重点关注的问题。

### 九、本章学习检查清单

学习完成度

### 0/9

能够解释可微分通信系统的概念

能够解释 trainable_points 和 requires_grad=True

能够理解 BCE 与 LLR 的关系

能够解释 loss.backward() 的梯度传播过程

能够独立写出三层 Neural Demapper

能够解释 nn.Parameter 与 nn.Module

能够独立搭建 Adam 训练循环

能够解释 BER 和 BLER 的区别

能够解释本章实验为什么还不属于 OFDM 神经接收机

我的建议： 不要急着直接跳到 Part 3。最好先自己复现本章的 Neural Demapper，尤其是理解 `forward → loss → backward → optimizer.step()` 这一完整过程。

当你能够独立搭建这个模型时，你就真正掌握了使用 Sionna + PyTorch 构建可训练通信系统的基本方法。接下来再进入 OFDM 神经接收机，会容易理解得多。
