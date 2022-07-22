import base64
import hashlib
import zlib
import IDEA
import random
from gmssl import sm2
from hash_utils import cal_md5


# 加密

def server(msg, symmetric_key, public_key_client, private_key_server,msg_enc):
    print("1.计算杂凑值")
    hash_val = cal_md5(msg)
    print('杂凑值:', hash_val)

    print("2.生成文件签名")
    m = int(hash_val, 16).to_bytes(16, 'big')
    print(m)
    sm2_crypt = sm2.CryptSM2(
        public_key=public_key_client,
        private_key=private_key_server)
    signature = sm2_crypt.sign(m, private_key_server)
    print('数字签名:', signature)

    print("3.将消息和数字签名拼接")
    with open(msg, "rb") as f:
        content = f.read()
    data = 'content=' + str(content) + ',signature=' + str(signature)
    print('拼接结果:', data)

    print('4.压缩文件')
    compressed_data = zlib.compress(str.encode(data), zlib.Z_BEST_COMPRESSION)
    print('压缩结果:', compressed_data)

    print('5.加密压缩后的数据')
    idea = IDEA.IDEA(key=symmetric_key)
    blocks = IDEA.string_to_blocks(str(compressed_data))
    encrypt_IDEA_words = []
    for block in blocks:
        encrypt_IDEA_words.append(idea.encrypt(block))
    print(type(symmetric_key), symmetric_key)

    print('6.加密对称会话密钥')
    enc_symmetric_key = sm2_crypt.encrypt(symmetric_key.to_bytes(16, 'big'))
    print(enc_symmetric_key)

    print('7.将加密会话密钥和加密数据级联')
    msg_fin = 'data='
    tmp = []
    for m in encrypt_IDEA_words:
        tmp.append(str(m))
        tmp.append(',')
    msg_fin += ''.join(tmp)

    msg_fin = msg_fin + ',key=' + str(enc_symmetric_key)
    print(msg_fin)
    print('8.级联结果进行Base64编码')
    msg_fin=msg_fin.encode('utf-8')
    data_encoded = base64.b64encode(msg_fin)
    # data_decoded = base64.b64decode(data_encoded)
    with open(msg_enc, 'wb') as f:
        f.write(data_encoded)
    print(data_encoded)
    # print('最终形态:' + str(data_encoded))


if __name__ == '__main__':
    msg = 'msg_file.txt'
    msg_e='cipher_file.txt'
    # symmetric_key = random.getrandbits(128)
    symmetric_key= 65110599130455911078239538504916232360
    print('对称密钥:',str(symmetric_key))
    public_key_client = 'B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A699' \
                        '4B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207'
    private_key_server = '00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5'
    server(msg, symmetric_key, public_key_client, private_key_server,msg_e)
