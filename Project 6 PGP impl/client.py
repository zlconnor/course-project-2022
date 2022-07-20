import base64
import hashlib
import zlib
from gmssl import sm2
import codecs
import IDEA


def client(msg_enc, private_key_client, public_key_server, msg_dec):
    # 服务器发来base64编码的密态消息msg_enc
    print('1.Base64解码')
    msg = base64.b64decode(msg_enc)  # base64解码
    print('2.密钥和数据分离')
    data_extract=msg.split('data=')[1]
    data_enc, key_enc = data_extract.split('key=')[0], msg.split('key=')[1][:-1]
    print('数据部分:',data_enc)
    print('密钥部分:',key_enc)
    print('3.解密得到对称密钥')
    sm2_crypt=sm2.CryptSM2(public_key='A',private_key='B')
    decrypt_IDEA_key=sm2_crypt.decrypt(key_enc)
    print('对称密钥:',decrypt_IDEA_key)
    print('4.解密数据')
    blocks=data_enc.split(',')[:-1]
    idea=IDEA.IDEA(key=decrypt_IDEA_key)
    decrypt_IDEA_words=[]
    for block in blocks:
        decrypt_IDEA_words.append(idea.decrypt(block))
    msg=idea.blocks_to_string(decrypt_IDEA_words)
    msg=bytes(msg[2:-1],encoding='utf-8')
    init_msg=codecs.escape_decode(msg,'hex-escape')
    print('5.解压缩')
    data_uncompress=zlib.decompress(init_msg[0])
    print('6.签名数据分离')
    data_uncompress= str(msg)
    tmp = data_uncompress.split('content=', 1)[1]
    content, signature = tmp.rsplit('signature=', 1)[0], tmp.rsplit('signature=', 1)[1][:-1]
    content=bytes(content[2:-1],encoding='utf-8')
    print('7.签名解密')
    signature_decrypt=sm2_crypt.decrypt(signature)
    print('8.验签')
    md5_obj = hashlib.md5()
    md5_obj.update(content)
    hash_val = md5_obj.hexdigest()
    if hash_val==signature_decrypt:
        print('valid signature')
    else:
        print('invalid signature')


