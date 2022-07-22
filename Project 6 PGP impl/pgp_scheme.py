import base64
import codecs
import zlib
import random
from gmssl import sm2
import IDEA
from utils import cal_md5, blks2str

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
    # print(msg_ori_bytes)
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
    # print(blocks)
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

    msg_to_send = msg_to_send + 'key=' + str(symmetric_key_cipher)
    print('\t级联结果:', msg_to_send.encode('utf-8'))

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
    msg = (base64.b64decode(msg)).decode('utf-8')
    print('\t解码结果:', msg)
    print('>>>2.密钥和数据分离')
    data_extract = msg.split('data=')[1]
    print(data_extract)
    data_enc = data_extract.split('key=')[0]
    key_enc = eval(msg.split('key=')[1])
    print('\t数据部分:', type(data_enc), data_enc)
    print('\t密钥部分:', type(key_enc), key_enc)
    print('>>>3.解密得到对称密钥')
    symmetric_key_dec_bytes = sm2_crypt.decrypt(key_enc)
    symmetric_key_dec_int = int.from_bytes(symmetric_key_dec_bytes, 'big')
    print('\t对称密钥(bytes):', symmetric_key_dec_bytes)
    print('\t对称密钥(int):', symmetric_key_dec_int)

    print('>>>4.解密数据')
    blocks = data_enc.split(',')[:-1]
    idea = IDEA.IDEA(key=symmetric_key_dec_int)
    decrypt_IDEA_words = []
    for block in blocks:
        decrypt_IDEA_words.append(idea.decrypt(int(block)))
    msg = blks2str(decrypt_IDEA_words)

    msg = bytes(msg[2:-1], encoding='utf-8')
    init_msg = codecs.escape_decode(msg, 'hex-escape')
    print('压缩后消息:', init_msg)
    print('>>>5.解压缩')
    data_uncompressed = zlib.decompress(init_msg[0])
    print('解压缩结果:', data_uncompressed)
    print('>>>6.签名数据分离')
    data_uncompressed = str(data_uncompressed)
    # print(data_uncompressed)
    tmp = data_uncompressed.split('content=', 1)[1]
    content, signature = tmp.rsplit('signature=', 1)[0], tmp.rsplit('signature=', 1)[1][:-1]
    content_bytes = bytes(content[2:-2], encoding='utf-8')
    with open(msg_dec, 'wb') as f:
        f.write(content_bytes)
    content = content[2:-2]
    print('\t数据部分:', content)
    print('\t签名部分:', signature)

    print('>>>8.验签')
    hash_val = cal_md5(msg_dec)
    # print(hash_val)
    # print(signature)

    hash_val_bytes = int(hash_val, 16).to_bytes(16, 'big')
    if sm2_crypt.verify(signature, hash_val_bytes):
        print('\tvalid signature.')
    else:
        print('\tinvalid signature.')


if __name__ == '__main__':
    msg_o = 'msg_file.txt'
    msg_e = 'cipher_file.txt'
    msg_d = 'msg_dec.txt'
    print('PGP协议模拟')
    print('***********************************************************服务器（加密）****************************************************************************************************************')
    server(msg_o, msg_e)
    print('***********************************************************客户端（解密）****************************************************************************************************************')
    client(msg_e, msg_d)
