import base64
import hashlib
import zlib
import IDEA
import random
from gmssl import sm2


def server(msg='hello world', symmetric_key=0, public_key_client=0,
           private_key_server='00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5', decrypt_file=0):
    symmetric_key = random.getrandbits(128)
    print("1.计算杂凑值")
    md5_obj = hashlib.md5()
    md5_obj.update(msg.encode('utf-8'))
    hash_val = md5_obj.hexdigest()
    print("2.生成文件签名")
    m = int(hash_val, 16).to_bytes(16, 'big')

    sm2_crypt = sm2.CryptSM2(public_key='', private_key=private_key_server)
    signature = sm2_crypt.sign(m, private_key_server)
    print(signature)
    print("3.将消息和数字签名拼接")
    data = 'content=' + msg + 'signature=' + str(signature)
    print('4.压缩文件')
    compressed_data = zlib.compress(str.encode(data), zlib.Z_BEST_COMPRESSION)
    print('5.加密压缩后的数据')
    idea = IDEA.IDEA(key=symmetric_key)
    blocks = IDEA.string_to_blocks(str(compressed_data))
    encrypt_IDEA_words = []
    for block in blocks:
        encrypt_IDEA_words.append(idea.encrypt(block))
    print('6.加密对称会话密钥')
    print(symmetric_key.to_bytes(16, 'big'))
    enc_symmetric_key = sm2_crypt.encrypt(symmetric_key.to_bytes(16, 'big'))
    print('7.将加密会话密钥和加密数据级联')
    msg_fin = 'data='
    tmp = []
    for m in encrypt_IDEA_words:
        tmp.append(str(m))
        tmp.append(',')
    msg_fin += ''.join(tmp)
    msg_fin = msg_fin + 'key=' + str(enc_symmetric_key)
    print('8.级联结果进行Base64编码')
    data_encoded = base64.b64encode(msg_fin.encode('utf-8'))
    print('最终结果:' + data_encoded)


if __name__ == '__main__':
    server()
