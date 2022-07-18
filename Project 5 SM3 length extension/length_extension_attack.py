from gmssl import sm3, func
import random
import sm3_modified
import struct

def forge(h0, length, appending):
    iv = []
    msg = ""
    # 将原始消息的杂凑值进行分组 得到最新的初始向量值
    for i in range(0, len(h0), 8):
        iv.append(int(h0[i:i + 8], 16))

    # 伪造等长的消息 如果长度大于64 用z填充
    if length > 64:
        for i in range(0, int(length / 64) * 64):
            msg += 'z'
    for i in range(0, length % 64):
        msg += 'z'
    msg = func.bytes_to_list(bytes(msg, encoding='utf-8'))
    msg = padding(msg)
    msg.extend(func.bytes_to_list(bytes(appending, encoding='utf-8')))
    return sm3_modified.sm3_hash(msg, iv)


def padding(msg):
    length = len(msg)
    msg.append(0x80)
    length += 1
    tail = length % 64
    range_end = 56
    if tail > range_end:
        range_end = range_end + 64
    for i in range(tail, range_end):
        msg.append(0x00)
    bit_len = (length - 1) * 8
    msg.extend([int(x) for x in struct.pack('>q', bit_len)])
    for j in range(int((length - 1) / 64) * 64 + (length - 1) % 64, len(msg)):
        global pad
        global pad_str
        pad.append(msg[j])
        pad_str += str(hex(msg[j]))
    return msg



m0 = str(random.random())
h0 = sm3.sm3_hash(func.bytes_to_list(bytes(m0, encoding='utf-8')))
len0 = len(m0)
appending = "201900301107张麟康"   # 附加消息
pad_str = ""
pad = []

h1 = forge(h0, len0, appending)
m1 = func.bytes_to_list(bytes(m0, encoding='utf-8'))
m1.extend(pad)
m1.extend(func.bytes_to_list(bytes(appending, encoding='utf-8')))
m1_str = m0 + pad_str + appending

h2 = sm3.sm3_hash(m1)


print("原始消息m: "+m0)
print("原始消息m的长度:%d" % len(m0))
print("原始消息杂凑值h:" + h0)
print("附加消息m':", appending)
print("待伪造杂凑值h1:" + h1)
print("构造新消息: \n" + m1_str)
print("新消息杂凑值h2:" + h2)

