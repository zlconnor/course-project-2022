import base64
import zlib
import random
from gmssl import sm2
import IDEA
from hash_utils import cal_md5

pk = 'B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A699' \
     '4B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207'
sk = '00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5'
K = sk
symmetric_key = random.getrandbits(128)
sm2_crypt = sm2.CryptSM2(public_key=pk, private_key=sk)


def server(msg_ori, msg_enc):
    print('>>>1.计算邮件哈希值')
    hash_val = cal_md5(msg_ori)
    print('\t杂凑值:', hash_val)

    print('>>>2.生成文件签名')
    msg_ori_bytes = int(hash_val, 16).to_bytes(16, 'big')
    print(msg_ori_bytes)
    signature = sm2_crypt.sign(msg_ori_bytes, K)
    print('\t数字签名:', signature)

    print('>>>3.将消息和数字签名拼接')
    with open(msg_ori, "rb") as f:
        content = f.read()
    data = 'content=' + str(content) + ',signature=' + str(signature)
    print('\t拼接结果:', data)
    print('>>>4.压缩文件')
    msg_compressed = zlib.compress(str.encode(data), zlib.Z_BEST_COMPRESSION)
    print('\t压缩结果:', msg_compressed)

    print('>>>5.加密压缩后的数据')

    idea = IDEA.IDEA(key=symmetric_key)
    blocks = IDEA.string_to_blocks(str(msg_compressed))
    encrypt_IDEA_words = []
    for block in blocks:
        encrypt_IDEA_words.append(idea.encrypt(block))
    # print(type(symmetric_key), symmetric_key)

    print('>>>6.加密对称会话密钥')

    symmetric_key_cipher = sm2_crypt.encrypt(symmetric_key.to_bytes(16, 'big'))
    print('\t原始状态:', symmetric_key)
    print('\t密钥明文:', symmetric_key.to_bytes(16, 'big'))
    print('\t加密结果:', symmetric_key_cipher)
    print('\t解密结果:', sm2_crypt.decrypt(symmetric_key_cipher))
    print('\t数值状态:', int.from_bytes(sm2_crypt.decrypt(symmetric_key_cipher), 'big'))
    print('>>>7.将加密会话密钥和加密数据级联')
    msg_to_send = 'data='
    tmp = []
    for m in encrypt_IDEA_words:
        tmp.append(str(m))
        tmp.append(',')
    msg_to_send += ''.join(tmp)

    msg_to_send = msg_to_send + ',key=' + str(symmetric_key_cipher)
    print('\t级联结果:', type(msg_to_send))
    print('>>>8.级联结果进行Base64编码')
    msg_to_send = msg_to_send.encode('utf-8')
    data_encoded = base64.b64encode(msg_to_send)
    # data_decoded = base64.b64decode(data_encoded)
    with open(msg_enc, 'wb') as f:
        f.write(data_encoded)
    print('\t最终形态:', data_encoded)


def client(msg_enc, msg_dec):
    # 服务器发来base64编码的密态消息msg_enc
    print('>>>1.Base64解码')
    with open(msg_enc, 'r') as f:
        msg = f.read()
    msg = base64.b64decode(msg)
    print('\t解码结果:',msg)
    print('>>>2.密钥和数据分离')
    msg = str(msg)
    data_extract = msg.split('data=')[1]
    data_enc, key_enc = data_extract.split('key=')[0], msg.split('key=')[1][:-1]
    print('\t数据部分:', type(data_enc), data_enc)
    print('\t密钥部分:', type(key_enc), key_enc)
    print(bytes(eval(key_enc)))
    print('>>>3.解密得到对称密钥')
    symmetric_key_dec=sm2_crypt.decrypt(eval(key_enc))
    print('\t对称密钥:',symmetric_key_dec)
    print('\t数值:',int.from_bytes(symmetric_key_dec,'big'))

    # print('4.解密数据')
    # blocks = data_enc.split(',')[:-1]
    # idea = IDEA.IDEA(key=decrypt_IDEA_key)
    # decrypt_IDEA_words = []
    # for block in blocks:
    #     decrypt_IDEA_words.append(idea.decrypt(block))
    # msg = idea.blocks_to_string(decrypt_IDEA_words)
    # msg = bytes(msg[2:-1], encoding='utf-8')
    # init_msg = codecs.escape_decode(msg, 'hex-escape')
    # print('5.解压缩')
    # data_uncompress = zlib.decompress(init_msg[0])
    # print('6.签名数据分离')
    # data_uncompress = str(msg)
    # tmp = data_uncompress.split('content=', 1)[1]
    # content, signature = tmp.rsplit('signature=', 1)[0], tmp.rsplit('signature=', 1)[1][:-1]
    # content = bytes(content[2:-1], encoding='utf-8')
    # print('7.签名解密')
    # signature_decrypt = sm2_crypt.decrypt(signature)
    # print('8.验签')
    # md5_obj = hashlib.md5()
    # md5_obj.update(content)
    # hash_val = md5_obj.hexdigest()
    # if hash_val == signature_decrypt:
    #     print('valid signature')
    # else:
    #     print('invalid signature')


if __name__ == '__main__':
    msg_o = 'msg_file.txt'
    msg_e = 'cipher_file.txt'
    msg_d = 'msg_dec.txt'
    server(msg_o, msg_e)
    client(msg_e,msg_d)
