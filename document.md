# 网络空间安全创新创业实践课程项目说明
# （各项目报告详见各项目文件夹中Report \*.pdf文件）
# (本文档中大部分图片取自各项目报告)

## 成员信息

姓名：张麟康

学号：201900301107

Git账户名称：zlconnor

## 项目信息

### 项目一 SM3生日攻击（完成人：张麟康）

对于杂凑函数$f$，其值域为$H$，那么寻找到一对碰撞就是找到不同的$x$和$x'$使得$f(x)=f(x')$。根据生日悖论，要想以超过百分之五十的概率找到一碰撞需要尝试的次数是$\sqrt{\frac{\pi}{2}H}$次。本项目基于上述原理，利用Python编程语言通过生成一定量的随机字符串对于缩减输出长度的SM3算法找到碰撞。

### 项目二 SM3 Rho Method（完成人：张麟康）

本项目根据Rho Method对利用Python编程语言实现对缩减输出长度的SM3算法进行碰撞攻击。

### 项目三 Merkle Tree实现（完成人：张麟康）

Merkle树叶子结点上存储数据块的哈希值，随后将两个相邻的数据块合并成一个字符串并计算哈希，逐级向上生成一个根，通常应用于数字签名、P2P网络、可信计算以及区块链验证等，本项目利用Python编程语言通过列表数据结构简单模拟Merkle Tree的实现以及结点存在性与不存在性的证明。

### 项目四 SM2实现（完成人：张麟康）

SM2椭圆曲线公钥密码算法是我国自主设计的公钥密码算法，包括数字签名算法、密钥交换协议以及公钥加密算法，分别用于实现数字签名、密钥协商以及数据加密功能，基于椭圆曲线上点群离散对数问题结合有限域相关理论实现，本项目基于Python编程语言实现了SM2中的数字签名和公钥加密算法。

### 项目五 SM3长度扩展攻击（完成人：张麟康）

对于满足加密前将待加密明文按照一定规则填充到固定长度倍数并且按照固定长度将明文分块散列并用前一块的散列结果作为下一个块初始向量的杂凑函数即MD结构的杂凑函数，存在一种长度扩展攻击的攻击手段。由于SM3算法满足MD结构，将SM3消息分组并存储其初始向量的中间值即可实现长度扩展攻击，本项目即通过获取消息的填充以及后缀的方式实现SM3算法的长度扩展攻击。

### 项目六 PGP方案实现（完成人：张麟康）

PGP加密由一系列散列函数、数据压缩、对称密钥加密以及公钥密码算法组合而成，每个步骤均支持几种算法，根据需求选择使用。PGP用于发送机密消息，结合对称和公钥密码体制，体用对称密码算法对消息进行加密，对称加密密钥通过公钥密码加密传输，此外还支持身份认证和完整性检查。本项目综合利用MD5摘要算法、SM2数字签名算法、SM2公钥密码算法以及IDEA分组密码算法和zlib压缩等技术实现PGP方案的模拟。

## 项目清单

### 完成的项目

1. implement the naïve birthday attack of reduced SM3
2. implement the Rho method of reduced SM3
3. implement length extension attack for SM3, SHA256, etc.
4. Impl Merkle Tree following RFC6962
5. impl sm2 with RFC6979
6. Implement a PGP scheme with SM2

### 未完成的项目

1. Try to Implement this scheme
2. report on the application of this deduce technique in Ethereum with ECDSA
3. verify the above pitfalls with proof-of-concept code
4. Implement the above ECMH scheme
5. implement sm2 2P sign with real network communication
6. PoC impl of the scheme, or do implement analysis by Google
7. implement sm2 2P decrypt with real network communication
8. send a tx on Bitcoin testnet, and parse the tx data down to every bit, better write script yourself
9. forge a signature to pretend that you are Satoshi
10. research report on MPT
11. Find a key with hash value “*sdu_cst_20220610*” under a message composed of *your name* followed by *your student ID*. For example, “*San Zhan 202000460001*”.
12. Find a 64-byte message under some k fulfilling that their hash value is symmetrical
13. Write a circuit to prove that your CET6 grade is larger than 425.
    * Your grade info is like (cn_id, grade, year, sig_by_moe). These grades are published as commitments onchain by MoE.
    * When you got an interview from an employer, you can prove to them that you have passed the exam without letting them know the exact grade.
14. The commitment scheme used by MoE is SHA256-based.
    * commit = SHA256(cn_id, grade, year, sig_by_moe, r)

### 有问题的项目及问题

项目四：SM2实现 中尚未实现密钥交换协议。

项目六：为了简便未加入Socket封装。

## 项目报告

### 项目一 SM3生日攻击

#### 项目代码说明

![image-20220725125308761](https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725125308761.png)

![image-20220725125316810](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725125316810.png)

![image-20220725125322331](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725125322331.png)

![image-20220725125333921](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725125333921.png)

![image-20220725125342236](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725125342236.png)

![image-20220725125350386](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725125350386.png)

![image-20220725125357437](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725125357437.png)

![image-20220725125405554](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725125405554.png)

#### 运行指导

直接运行文件夹[Project 1 birthday attack of reduced SM3](https://github.com/zlconnor/course-project-2022/tree/master/Project 1 birthday attack of reduced SM3)下的文件sm3_btd_atk.py即可，可以根据上述项目代码说明修改相关参数并直接运行。

#### 代码运行截图

![image-20220725125423467](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725125423467.png)

![image-20220725125433563](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725125433563.png)

![image-20220725125442396](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725125442396.png)

#### 贡献情况

本项目全部由[张麟康](https://github.com/zlconnor)完成。

### 项目二 SM3 Rho Method

#### 项目代码说明

![image-20220725124430305](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725124430305.png)

![image-20220725124439652](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725124439652.png)

![image-20220725124457208](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725124457208.png)

#### 运行指导

直接运行文件夹[Project 2 the Rho method of reduced SM3](https://github.com/zlconnor/course-project-2022/tree/master/Project 2 the Rho method of reduced SM3)下的文件sm3_rho_method.py即可，可以根据上述项目代码说明修改相关参数并直接运行。[Project 3 Merkle Tree](https://github.com/zlconnor/course-project-2022/tree/master/Project 3 Merkle Tree)

#### 代码运行截图

![image-20220725124513981](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725124513981.png)

#### 贡献情况

本项目全部由[张麟康](https://github.com/zlconnor)完成。

### 项目三 Merkle Tree实现

#### 项目代码说明

![image-20220725124544468](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725124544468.png)

![image-20220725124554129](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725124554129.png)

![image-20220725124601469](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725124601469.png)

![image-20220725124611776](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725124611776.png)

![image-20220725124629949](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725124629949.png)

![image-20220725124645268](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725124645268.png)

![image-20220725124653561](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725124653561.png)

![image-20220725124702999](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725124702999.png)

![image-20220725124722562](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725124722562.png)

![image-20220725124735578](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725124735578.png)

![image-20220725124743081](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725124743081.png)

![image-20220725124753952](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725124753952.png)

![image-20220725124804855](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725124804855.png)

#### 运行指导

直接运行文件夹[Project 3 Merkle Tree](https://github.com/zlconnor/course-project-2022/tree/master/Project 3 Merkle Tree)下的文件merkle_tree.py即可，可以根据上述项目代码说明修改相关参数并直接运行。[Project 4 SM2 impl](https://github.com/zlconnor/course-project-2022/tree/master/Project 4 SM2 impl)

#### 代码运行截图

![image-20220725124633532](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725124633532.png)

![image-20220725124653561](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725124653561.png)

![image-20220725124810444](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725124810444.png)

#### 贡献情况

本项目全部由[张麟康](https://github.com/zlconnor)完成。

### 项目四 SM2实现

#### 项目代码说明

![image-20220725124858527](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725124858527.png)

![image-20220725124911852](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725124911852.png)

![image-20220725124923591](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725124923591.png)

![image-20220725124937560](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725124937560.png)

![image-20220725124945855](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725124945855.png)

![image-20220725124954824](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725124954824.png)

![image-20220725125002589](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725125002589.png)

![image-20220725125008669](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725125008669.png)

![image-20220725125015231](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725125015231.png)

![image-20220725125021356](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725125021356.png)

![image-20220725125029472](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725125029472.png)

![image-20220725125037320](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725125037320.png)

![image-20220725125048906](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725125048906.png)

![image-20220725125058142](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725125058142.png)

![image-20220725125108681](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725125108681.png)

![image-20220725125119702](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725125119702.png)

![image-20220725125126796](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725125126796.png)

![image-20220725125133251](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725125133251.png)

#### 运行指导

直接运行文件夹[Project 4 SM2 impl](https://github.com/zlconnor/course-project-2022/tree/master/Project 4 SM2 impl)下的文件sm2_new.py即可，可以根据上述项目代码说明修改相关参数并直接运行。[Project 5 SM3 length extension](https://github.com/zlconnor/course-project-2022/tree/master/Project 5 SM3 length extension)

#### 代码运行截图

![image-20220725125140655](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725125140655.png)

![image-20220725125148669](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725125148669.png)

![image-20220725125200274](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725125200274.png)

![image-20220725125208844](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725125208844.png)

![image-20220725125219233](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725125219233.png)

![image-20220725125226473](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725125226473.png)

#### 贡献情况

本项目全部由[张麟康](https://github.com/zlconnor)完成。

### 项目五 SM3长度扩展攻击

#### 项目代码说明

![image-20220725124307352](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725124307352.png)

![image-20220725124315560](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725124315560.png)

![image-20220725124323957](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725124323957.png)

![image-20220725124334705](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725124334705.png)

#### 运行指导

直接运行文件夹[Project 5 SM3 length extension](https://github.com/zlconnor/course-project-2022/tree/master/Project 5 SM3 length extension)下的文件length_extension_attack.py即可，可以根据上述项目代码说明修改相关参数并直接运行。

#### 代码运行截图

![image-20220725124354511](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725124354511.png)

#### 贡献情况

本项目全部由[张麟康](https://github.com/zlconnor)完成。

### 项目六 PGP方案实现

#### 项目代码说明

![image-20220725123739667](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725123739667.png)

![image-20220725123802868](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725123802868.png)

![image-20220725123828302](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725123828302.png)

![image-20220725124013498](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725124013498.png)

![image-20220725124027431](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725124027431.png)

![image-20220725124034479](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725124034479.png)

![image-20220725124043977](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725124043977.png)

![image-20220725124051509](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725124051509.png)

![image-20220725124058696](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725124058696.png)

![image-20220725124105121](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725124105121.png)

![image-20220725124112206](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725124112206.png)

#### 运行指导

直接运行文件夹[Project 6 PGP impl](https://github.com/zlconnor/course-project-2022/tree/master/Project 6 PGP impl)下的文件pgp_scheme.py即可，可以根据上述项目代码说明修改相关参数并直接运行。

#### 代码运行截图

![image-20220725124123681](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725124123681.png)

![image-20220725124139178](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725124139178.png)

![image-20220725124152519](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725124152519.png)

![image-20220725124204087](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725124204087.png)

![image-20220725124221054](Https://github.com/zlconnor/course-project-2022/blob/master/document.assets/image-20220725124221054.png)

#### 贡献情况

本项目全部由[张麟康](https://github.com/zlconnor)完成。
