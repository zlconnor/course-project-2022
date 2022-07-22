import hashlib
import math
import random
import time
import binascii
from data_type_transform import point2bit, hex2point, mod_inverse, bin_xor


class SM2:
    # 椭圆曲线参数设置
    p = 0x8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3
    a = 0x787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498
    b = 0x63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A
    Gx = 0x421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D
    Gy = 0x0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2
    n = 0x8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7
    v = 256  # 哈希函数输出比特长度
    h = 1
    size = 2048  # 明文分组大小

    def key_produce(self):
        """
        生成公钥 私钥函数
        :return: 公钥：PB {x,y} 私钥：dB
        """
        dB = random.randint(1,self.n-1)
        PB = self.ecc_multiply(dB, (self.Gx, self.Gy))
        return PB, dB

    def test_point(self, cipher):
        """
        检测密文 点坐标 是否正确
        :param cipher: 待检测的密文 点坐标
        :return: True 检测合格 False 检测不合格
        """
        x, y = cipher

        # y*y=x*x*x+a*x+b 检测方程
        tmp1 = y * y % self.p
        tmp2 = (x * x * x + self.a * x + self.b) % self.p

        if tmp1 == tmp2:
            return True
        else:
            return False

    def KDF(self, Z, klen):
        """
        密钥派生函数
        :param Z:密钥二进制串
        :param klen:明文二进制长度
        :return: 扩展后的密钥二进制串
        """
        ct = 1  # 计数器
        K = ''  # 十六进制串
        for i in range(klen // self.v):
            K += self.hash(Z + bin(ct)[2:].zfill(32))
            ct += 1
        # 取剩余部分
        f_length = klen / self.v
        if math.ceil(f_length) != int(f_length):
            K += self.hash(Z + bin(ct)[2:].zfill(32))[:(klen - self.v * int(f_length)) // 4]
        # 返回二进制串
        K_binary = bin(int(K, 16))[2:].zfill(klen)
        return K_binary

    def hash(self, s):
        """
        哈希函数  国密 SM2 原版 hash 函数 是 SM3 256 bit，这里只是测试方便
        :return: 16 进制串 256 bit
        """
        sha_obj = hashlib.sha256()
        sha_obj.update(s.encode())
        return sha_obj.hexdigest()

    def ecc_add_same(self, G):
        """
        椭圆曲线上的相同坐标的两个点相加
        :param G: 生成元，基点
        :return: 相加之后的点
        """
        x1, y1 = G

        # 计算 斜率 k ，k 已不具备明确的几何意义
        tmp1 = 3 * x1 * x1 + self.a
        tmp2 = mod_inverse(2 * y1, self.p)
        k = tmp1 * tmp2 % self.p

        # 求 x3
        x3 = (k * k - x1 - x1) % self.p

        # 求 y3
        y3 = (k * (x1 - x3) - y1) % self.p

        return x3, y3

    def ecc_add_diff(self, G1, G2):
        """
        椭圆曲线上两个不同点相加
        :param G1: 第一个点
        :param G2: 第二个点
        :return: 相加得到的点
        """
        x1, y1 = G1
        x2, y2 = G2

        # 计算 斜率 k
        tmp1 = y2 - y1
        tmp2 = mod_inverse((x2 - x1) % self.p, self.p)
        k = tmp1 * tmp2 % self.p

        # 求 x3
        x3 = (k * k - x1 - x2) % self.p

        # 求 y3
        y3 = (k * (x1 - x3) - y1) % self.p

        return x3, y3

    def ecc_add_neighbor(self, point, pointBase):
        """
        相邻的两个点相加 ，pointBase 为基点，如：23P 点 + 24P 点
        :return: 新的点
        """
        return self.ecc_add_diff(pointBase, self.ecc_add_same(point))

    def ecc_multiply(self, k, G):
        """
        椭圆曲线上的点乘以常数 k
        :param k: int
        :param G: 生成元 基点
        :return: 相乘之后的点
        """
        if k == 1:
            return G  # 只有 k 取 1 时，才有这种可能

        if k == 2:
            return self.ecc_add_same(G)

        if k == 3:
            return self.ecc_add_diff(G, self.ecc_add_same(G))

        if k % 2 == 0:
            return self.ecc_add_same(
                self.ecc_multiply(k // 2, G))  # return 里只能有一个 oval_multiply 函数，两个及以上很有可能出错，进入无限循环

        if k % 2 == 1:
            return self.ecc_add_neighbor(self.ecc_multiply(k // 2, G), G)

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
        return cipher

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
        x, y = pk
        while True:
            k = random.randint(1 << 50, 1 << 100)
            # 生成随机数
            C1 = self.ecc_multiply(k, (self.Gx, self.Gy))
            C1_binary = point2bit(C1)
            C = self.ecc_multiply(k, (x, y))
            C_binary = point2bit(C, False)
            t = self.KDF(C_binary[0], plain_block_bin_len)
            if t.count('0') != plain_block_bin_len:
                break
        C2_binary = bin_xor(plain_block_bin, t)
        C3_hex = self.hash(C_binary[1] + plain_block_bin + C_binary[2])
        C1_hex = hex(int(C1_binary, 2))[2:].zfill(130)
        C2_hex = hex(int(C2_binary, 2))[2:].zfill(plain_block_bin_len // 4)
        return C1_hex + C2_hex + C3_hex

    def decrypt(self, cipher, sk):
        """
        dec
        :param cipher:密文 十六进制字符串
        :param sk: 私钥
        :return: 明文字符串
        """
        cnt = (self.size + 256 + 520) // 4
        cipher_block_list = []
        i = -1
        # 分块
        for i in range(len(cipher) // cnt):
            cipher_block_list.append(cipher[cnt * i + cnt * (i + 1)])
        if math.ceil(len(cipher) / cnt) != len(cipher) // cnt:
            cipher_block_list.append(cipher[cnt * (i + 1):])

        plain_hex = ''
        for block in cipher_block_list:
            plain_hex += self.decrypt_block(block, sk)
        plain = binascii.a2b_hex(plain_hex).decode()
        return plain

    def decrypt_block(self, cipher_block, sk):
        cipher_block_len = len(cipher_block)
        # 拆分密文各个部分
        C1_hex = cipher_block[:130]
        C2_hex = cipher_block[130:cipher_block_len - self.v // 4]
        C3_hex = cipher_block[-self.v // 4:]
        # C1转换为点
        C1_point = hex2point(C1_hex)
        dB_mul_C1 = self.ecc_multiply(sk, C1_point)
        C1_binary = point2bit(dB_mul_C1, False)

        # C2
        C2_binary_len = len(C2_hex) * 4
        C2_binary = bin(int(C2_hex, 16))[2:].zfill(C2_binary_len)

        # 密钥派生
        t = self.KDF(C1_binary[0], C2_binary_len)
        plain_binary = bin_xor(C2_binary, t)
        u = self.hash(C1_binary[1] + plain_binary + C1_binary[2])

        if u != C3_hex:
            exit(-1)
        plain_hex = hex(int(plain_binary, 2))[2:].zfill(len(plain_binary) // 4)
        return plain_hex


if __name__ == '__main__':
    start = time.time()
    sm2_obj = SM2()
    key = sm2_obj.key_produce()
    PB, dB = key
    plain="encryption standard"
    # plain = '123456'
    print('original text:', plain)
    # 加密
    cipher = sm2_obj.encrypt(plain, PB)
    print("cipher text:", cipher)
    # 解密
    p = sm2_obj.decrypt(cipher, dB)
    print("plain text:", p)
    # 判断
    if plain == p:
        print("encrypted and decrypted successfully.")
    else:
        print("some errors occurred.")

    print("time cost:", time.time() - start)
