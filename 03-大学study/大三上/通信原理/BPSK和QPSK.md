![[Pasted image 20260922164719.png]]
以IQ调制为基础，本质是相位移动PSK（phase shift keying)相位键控
![[Pasted image 20260922165041.png]]
BPSK
传输0时的s ( t ) = c o s ( ω 0 t )
传输1时的s ( t ) = − c o s ( ω 0 t )
![[Pasted image 20260922165217.png]]
![[Pasted image 20260922165256.png]]
**那么，取出那个不旋转的向量就可以解调出+1 和 -1 ，从而得到输入信号是0还是1**
如何取出那个不旋转的向量+1和-1呢？

1. 使用低通滤波器，滤去高频分量，得到直流量。
2. 通过积分。
3. ![[Pasted image 20260922165413.png]]