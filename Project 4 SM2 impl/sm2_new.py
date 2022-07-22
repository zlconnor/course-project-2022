import hashlib
import math
import random
from Point import Point
import binascii


class SM2:
    # 椭圆曲线参数设置
    q = 0x8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3
    a = 0x787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498
    b = 0x63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A
    h = 1
    Gx = 0x421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D
    Gy = 0x0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2
    n = 0x8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7
    v = 256  # 哈希函数输出比特长度

    size = 2048  # 明文分组大小

    def encrypt(self, plain, pk):
        """
        :param plain:明文[字符串形式]
        :param pk: 公钥[(x,y)]
        :return: 密文[十六进制字符串]
        """
        plain = str(binascii.b2a_hex(plain.encode()), 'utf-8')
        cnt = self.size // 4
        plain_block_list = []
        i = -1
        for i in range(len(plain) // cnt):
            plain_block_list.append(int(plain[cnt * i:cnt * (i + 1)], 16))
        if math.ceil(len(plain) / cnt) != len(plain) // cnt:
            plain_block_list.append(int(plain[cnt * (i + 1):], 16))
        cipher = ''
        for block in plain_block_list:
            cipher += self.encrypt_block(block, pk)

    def encrypt_block(self, block, pk):
        """
        明文块加密
        :param block: 明文块[整数]
        :param pk: 公钥
        :return: 密文块[十六进制字符串]
        """
        # 转换为二进制字符串
        plain_block_bin = bin(block)[2:]
        plain_block_bin = '0' * (-len(plain_block_bin) % 8) + plain_block_bin
        plain_block_bin_len = len(plain_block_bin)
        # 获取公钥 点
        x,y=pk
        while True:
            



def all_zero(s):
    for ch in s:
        if ch != '0':
            return False
    return True


def padding(s, length):
    tmp = s
    s = ''
    if tmp[0:2] == '0b':
        s = s + '0b'
        tmp = tmp[2:len(tmp)]
    for i in range(0, length - len(tmp)):
        s = s + '0'
    for i in range(0, len(tmp)):
        s = s + tmp[i]
    return s


def hash_function(m):
    sha256 = hashlib.sha256()
    sha256.update(m.encode("utf8"))
    sha256 = bin(int(sha256.hexdigest(), 16))
    sha256 = padding(sha256, 32 * 8)
    return sha256


def KDF(Z, klen):
    v = 256
    if klen < (2 ** 32 - 1) * v:
        ct = 0x00000001
        H = []
        H_ = []
        for i in range(0, math.ceil(klen / v)):
            H.append((hash_function(Z + str(ct)))[2:])
            ct = ct + 1
        if klen / v == math.ceil(klen / v):
            H_ = (H[math.ceil(klen / v) - 1])[2:]
        else:
            H_ = H[math.ceil(klen / v) - 1][0:(klen - (v * math.floor(klen / v)))][2:]
        K = ''
        for i in range(0, math.ceil(klen / v)):
            if i != math.ceil(klen / v) - 1:
                K = K + H[i]
            else:
                K = K + H_
    else:
        print("error")
    return K


def encrypt(data, pb):
    t = '0'
    klen = len(data)
    while all_zero(t):
        # A1 用随机数发生器生成随机数k [1,n-1]
        k = random.randint(1, parameters['n'] - 1)
        # A2 计算椭圆曲线点C1=kG
        C1 = kP(k, Point(parameters['Gx'], parameters['Gy']))
        C1 = point2bytes(C1)
        C1 = bytes2bits(C1)
        # A3计算S=[h]PB
        S = kP(parameters['h'], pb)
        # 若S是无穷远点则报错退出
        # A4 计算[k]PB=(x2,y2)
        x2 = kP(k, pb).x
        y2 = kP(k, pb).y
        x2 = (bytes2bits(elem2bytes(x2)))[2:]
        y2 = (bytes2bits(elem2bytes(y2)))[2:]
        # A5 计算t=KDF
        t = KDF(x2 + y2, klen)
    # A6 计算C2=data \oplus t
    data = data[2:]
    C2 = bin(int(data, 2) ^ int(t, 2))
    C2 = padding(C2, klen)
    # A7 计算C3
    C3 = hash_function(x2 + data + y2)
    # A8 输出密文C=C1||C2||C3
    C1 = C1[2:]
    C2 = C2[2:]
    C3 = C3[2:]
    C = C1 + C2 + C3
    return C


def decrypt():
    pass
