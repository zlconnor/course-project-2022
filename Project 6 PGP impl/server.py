import base64
import hashlib
import zlib
import IDEA
import random
from gmssl import sm2


# 加密

def server(msg, symmetric_key, public_key_client,private_key_server):
    print("1.计算杂凑值")
    md5_obj = hashlib.md5()
    md5_obj.update(msg.encode('utf-8'))
    hash_val = md5_obj.hexdigest()
    print('杂凑值:',hash_val)

    print("2.生成文件签名")
    m = int(hash_val, 16).to_bytes(16, 'big')
    sm2_crypt = sm2.CryptSM2(
        public_key=public_key_client,
        private_key=private_key_server)
    signature = sm2_crypt.sign(m, private_key_server)
    print('数字签名:',signature)
    print("3.将消息和数字签名拼接")
    data = 'content=' + msg + ',signature=' + str(signature)
    print('拼接结果:',data)
    print('4.压缩文件')
    compressed_data = zlib.compress(str.encode(data), zlib.Z_BEST_COMPRESSION)
    print('压缩结果:',compressed_data)
    print('5.加密压缩后的数据')
    idea = IDEA.IDEA(key=symmetric_key)
    blocks = IDEA.string_to_blocks(str(compressed_data))
    encrypt_IDEA_words = []
    for block in blocks:
        encrypt_IDEA_words.append(idea.encrypt(block))
    print(type(symmetric_key),symmetric_key)
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
    print(msg_fin.encode('utf-8'))
    data_encoded = base64.b64encode(msg_fin.encode('utf-8'))
    print('最终形态:' + str(data_encoded))
    data_decoded=base64.b64decode(b'ZGF0YT05NDQ5NzkyOTMzMTgxODMzODIxLDExNjA0MDY2NzgyODg2MDQ0NTc1LDIxMjkxMTMzODkzNDYyNzk5NzIsMTU2NzQwNDA1MzUxMDgwNDIxMTAsMTA5OTgyOTkwMzI4NTU1MTYzNyw3NDYzNjIzNDg4NjQzMjMyNTQ1LDMzNDI5NjkyNzk1MjEzOTA0OTEsNTY5OTc1MjMxMjk0NTU3MjQ4OCwxNDI2MDU3ODcwNjEwNDI0ODg3OSwxMTMxMTE4OTUyOTAyMTcwNjUyOCwxNTcxOTczNzI2Mjk2ODY2NTkzNSw2MDUwNTI5NzkyMTExMTk3Nzc2LDM5NjE5MzMxODM5MTU3Nzc1MDMsMTYyMTk4MTQwODU4MDg4NjM4NTAsNjEwMzIzNjk5MzA3NjEzMzQzMiwxMjQ0ODIwODc0ODIwODcxMDc2Niw3NzE4NzA2NDQ5MjM3NDc1Njk0LDEyMTkyMDk4OTc2OTgyNTgwNzg3LDE3MzAyNzUwMDQ3Njk3OTc1NTQ0LDk2NzgwMjg3MTE1NTIyOTM3OTgsMzY1NjE3NjUxNDE4MjUyMjAzLDE2ODczMzA4MTg0MzM4ODkwMCw4OTg3MjU2MTI5NDE0NTI4MjEzLDE3MjYyMzY5MjQ3ODExNzIyODUwLDYwMTM0OTYzNTQ0MDUxNjYwOTIsMTQ1MDE1MzgzMzMzNjQ2MDM2NzEsOTI3MjU0NzkzODEzOTEyMzkyNSw4ODg4NTIyNTE0MDAxNjQ0NzM5LDE0NTY0NjI0ODEwMjU3OTkwMjM4LDE5Njk5NDU1MDA0MjczNDEzNjQsMTUxMTcwODU5MzgxOTAwNTcxNTAsNjI5NTA1MDgyNjI2MjQxOTc2OSwxMjMxMzQzMjc5ODQ0NDc0MDk3NiwyMDIzNzc1NTI2NDg3MjIxMDIzLDY3MDczNjkwMjgzNjQyNTUwMzEsODc1MjkzNTcyMjk2NzE2OTk5MywxNDA0OTI1Mjc1OTU0NzY3NTA0NCw5Mjg4OTgxODc4MjM3MjI5ODQwLDk5OTkyNDIxNTg0NDU0OTExNzYsNjA1OTY2NTMyMTM0NDU5MzgwOSwxNTA1NjUzNzg2ODU3MjQ5OTE2OCwxMjM1Njk0NjgzMTY3MjUzNTYxLDkwODY4ODU3MTcyMTE3MDQ1MDQsMTYyMDI0NTIyODE4NzA3NTg4MzcsMjMzODA4NTIwMDMzOTkwMzkyMSwxNjg1MjI0NzY3NzU5NTk3NjM5MywxNjc4NDc2NzczNDMwNTc0NDM1MCxrZXk9YidceGUxY2xceGY3c1UgXHhlOENceDhkXHhkZFx4OGJceDAwXHhlY1wnXHg5NkUwJlx4ZThceGJmXHhiMVx4YWJceGU4XHg5M1x4YjVceGM3XHgxME9ceGUwa1x4YjVceDFmQ1x4YTBceGI5MVx4ODNyXHhiYTVceGMzXHgwNk5ceDE1XHhiMlx4ZTRceGU5XHg4OVx4ZjVceGVlXHhjZGtceGQwdzxceDg3XHgxMlx4YmVQXHg4NFx4OWVceGZjXHgxZVx4MDhrXHhiYlx4OTlGa1x4ZmFceGYxXHhlMlxyUE1ceGIyUFx4YzNceGYwXHg4M1x4ZDRceGRjSkpceGNmISxaXHg5NVx4OTdceDk0XHgxM1x4ZmRceGYwblx4Y2U5XHhmMTdceDg2XHhhNjZceGQ3ZnIiXHg5NTtceGY3ayIn'.decode('utf-8'))
    print(data_decoded)


if __name__ == '__main__':
    msg='hello world'
    symmetric_key = random.getrandbits(128)
    public_key_client='B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A699' \
                      '4B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207'
    private_key_server='00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5'
    server(msg,symmetric_key,public_key_client,private_key_server)
