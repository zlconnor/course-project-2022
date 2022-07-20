import hashlib
import os
import zipfile
import zlib
import base64
import time
from gmssl import sm2
import rsa


def server(msg_file, idea_key, ce, cn, sd, sn, decrypt_file):
    print("1.计算杂凑值")
    hash_val=hashlib.md5(msg_file)
    print("2.生成文件签名")
    m=int(hash_val,16)
    signature=rsa.sign(m,sd,sn)
    print("3.将消息和数字签名拼接")
    with open(msg_file,'rb') as f:
        raw_data=f.read()
    data='content='+str(raw_data)+'signature='+str(signature)
    print('4.压缩文件')
    compressed_data=zlib.compress(str.encode(data),zlib.Z_BEST_COMPRESSION)
    print('5.加密压缩后的数据')






