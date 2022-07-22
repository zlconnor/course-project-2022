def point2bit(point, mode=True):
    """
    将椭圆曲线上的点转换为比特串
    :param point: 椭圆曲线上的点坐标
    :param mode: 值为true时转换C1；值为False转换其他点
    :return: 椭圆曲线上的点对应的二进制串
    """
    x = point[0]
    y = point[1]
    pc = '00000100'  # 单一字节 04
    x_binary = bin(x)[2:].zfill(256)
    y_binary = bin(y)[2:].zfill(256)
    # 若为C1
    if mode:
        return pc + x_binary + y_binary
    else:
        return x_binary + y_binary, x_binary, y_binary


def bin_xor(a_binary, b_binary):
    if len(a_binary) != len(b_binary):
        return -1
    res = ''
    length = len(a_binary)
    for i in range(length):
        res += str(int(a_binary[i]) ^ int(b_binary[i]))
    return res


def hex2point(s_hex, mode=True):
    """
    :param s_hex: 十六进制字符串
    :param mode: 为True时转换C1 为False转换其他
    :return: 对应的点
    """
    x = int(s_hex[-128:-64], 16)
    y = int(s_hex[-64:], 16)

    if mode:
        if int(s_hex[:2], 16) == 4:
            return x, y
        else:
            return False
    else:
        return x, y


def mod_inverse(n, p):
    a = [0] * 1000  # 注意 1000 可能不够长，适时调整即可
    b = [0] * 1000
    a[0] = p
    b[0] = n
    i = 0
    while a[i] % b[i]:
        a[i + 1] = b[i]
        b[i + 1] = a[i] % b[i]
        i += 1
    i -= 1
    div_a = 1
    div_b = -(a[i] // b[i])
    while i != -1:
        if i >= 1:
            tmp = div_a
            div_a = div_b
            div_b = tmp - a[i - 1] // b[i - 1] * div_b

        i -= 1

    return div_b % a[0]
