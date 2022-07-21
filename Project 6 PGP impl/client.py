import base64
import hashlib
import zlib
from gmssl import sm2
import codecs
import IDEA


def client(msg_enc=b'ZGF0YT0xMDI2MzM0MjY4ODA5NjczMDMyMSwxNjE4ODY0MDk2NzAzODE5NDMzMiw5NTE5NzMzMTY5Njg4NTExNzAwLDY5NzI1ODQ4NDcwMDE0MzE3NTIsNjE2MDQ4ODI1NjIwMjY4NjI2OSwxMzA4OTExODA0MTg2NDcwNjAxNCwxNjU3NTgzNTU4MDA0OTEyNjA0NCw5MTU1ODMyODIxNjQxNTk3MjA0LDEzNTgwNDY2ODU0MzU0MDc3NDQ4LDcxNjE5NjE1Nzk4NjczNDM1MjIsMTAyNDg2NDk5MjY1NjcwMDIwNzAsMjY3MDI5NjkxNjg2MTExNzIxMiwxODAyMDY5OTQ3OTMyNDcyNjcwMyw2MzMyNDEyMzM4MTE3Nzk5OTQsMjQzMzA0OTg1ODQ0MzY2NjIyOCwyMTIyNjMwNTMxMTgyODY0NDc4LDQ4ODgyOTczMzg0NjQ5ODIzNTAsMTU4MTU1NDkxNjAxMTk1NTQzOSwxMjA5MzQ5NDAyOTQ1NjU0ODE1Nyw3NDM2ODg2MjAxMDUxODE0NzY0LDExNzcyNTEwMjgwMjQyMTQwNDU1LDgzMjA2MjQwMDg2OTE0MDYzMDUsMTgwOTI0MDA3OTA4Nzg5MDQ2NjgsNzY0Nzk1NjA0NTgxMDUxMDAzOSwxMjgzNzUwMzM5Mzk4NDI4NjA4NCw5MjM0NzA5Mjk0ODgyNjYzMTg0LDQ0ODk1Mzg1NzA0NDAzMjkxMzQsMTY1MDI2MTY5MDExNzk4ODk1MzgsMzI4MDA1MTczNjQyNTY2NDU1MiwxMjQ0NDkyNzc1NzU2NjY5MDI5Miw3NzExNjg0NjY4ODY0Mzc2MTg0LDMyMjY5ODUwODkwMzA3NjAxMzEsMTE3MzU1OTA5NjkyMTM2MTQ2NCw4Mzg2Mzg5Njc0NTEyMjkzMjIsMTQ2NDEzMDg0Njg5NjE2NzQ0MjgsMTc2ODAzODI4NDk5NjQxODMwNjcsMTMxMzk0ODAxMzczMTEyNzIwNCw5MDQ0OTEzMTY4NTc5NDk1Nzg5LDc2Njk0NTczNjU2OTcyODk4MywxNDkxMDkyNzI2MTA1NDc1NTc4MCwzNTUxMTQ0MDQ1OTM5MjYzMTA2LDEzMTM5MDcwNTMwNzc2MTA4MTg3LDE1ODE1Mjg2OTM4MDIwNTc3ODE3LDE1ODUyNDMzOTk5MzMyOTM4OTQwLDE3MzAwMDIyNTQ0MDA0NjE0NDgzLDg3MjQ0ODI1MzE1NDU4MzczNDIsMTA1MTc4ODg4MTc2MzY3NTI3MDcsa2V5PWInXHhlYXhtXHg4NFx4YjlceDkzXHhhZlx4OTFceGE0XHgwOFx4YmNceGExcGx8XHg5MFx4OTExLGlceGMzXHg4Zlx4ZjhceDEwYFx4MTJdK1x4YThceGZhLVx4MWFzXHgxNVx4ODdceDE0XHg4Mlx4ZDlceDdmRVx4Yjh4XHg5N1x4YmNceDE1XHhkMlx4MTZ3XHg5M1x4OTNceGJmXHhiZVx4OGFceDk4XHgxOFx4OGRceGFhfHtceGM1Jlx4MTFceGMyNXRxXHg5NVx4MTVceDAxXHgwNlx4YWFceGYxXHhiODJceGU5XHhjY04uVXVIXHhmZFx4MGJceGVhUFx4OThHV1x4N2ZceDgzXHhhOFx4MWRceGRjVlx4YzNceDg1UEdFXHhlZjhceGNjXHgxYXVmXHg4NFx4OWNceDg5XHhiOFx4ZDhceGFkdyc='
, private_key_client='00B9AB0B828FF68872F21A837FC303668428DEA11DCD1B24429D0C99E24EED83D5', public_key_server='B9C9A6E04E9C91F7BA880429273747D7EF5DDEB0BB2FF6317EB00BEF331A83081A6994B8993F3F5D6EADDDB81872266C87C018FB4162F5AF347B483E24620207', msg_dec=0):
    # 服务器发来base64编码的密态消息msg_enc
    print('1.Base64解码')
    msg = base64.b64decode(msg_enc)  # base64解码
    print(msg)
    print('2.密钥和数据分离')
    msg=str(msg)
    data_extract=msg.split('data=')[1]
    data_enc, key_enc = data_extract.split('key=')[0], msg.split('key=')[1][:-1]
    print('数据部分:',data_enc)
    print('密钥部分:',key_enc)
    print('3.解密得到对称密钥')
    sm2_crypt=sm2.CryptSM2(public_key=public_key_server,private_key=private_key_client)
    key_enc=eval(key_enc)
    decrypt_IDEA_key=sm2_crypt.decrypt(key_enc)

    decrypt_IDEA_key=int.from_bytes(decrypt_IDEA_key,'big')
    print('对称密钥:', decrypt_IDEA_key)
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


if __name__ == '__main__':
    client()