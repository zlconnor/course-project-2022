from gm import sm3
import string
import random
import time
start_time = time.time()
N = 32
TRUNC = 12
char_set = string.ascii_letters+string.digits
trial_times = 0
record = {}
MAX_TRIAL=12000000

def reduced_sm3(m):
    return sm3.SM3(m)[:TRUNC]


def get_random_input():
    random_input = ''.join(random.sample(char_set, N))
    res = ''
    for x in random_input:
        res += str(ord(x))
    return res


def hex2ord(hex_str):
    res=''
    for i in range(len(hex_str)//2):
        res+=str(int(hex_str[2*i:2*(i+1)],16))
    return res

hash = ''
random_input = ''

record={}
h=get_random_input()
h_=h





for i in range(MAX_TRIAL):
    hash=sm3.SM3(h)
    hash_=sm3.SM3(hex2ord(sm3.SM3(h)))
    record[h]=hash[:TRUNC]
    record[h_]=hash_[:TRUNC]
    if len(record) !=len(set(record.values())):
        print(h,h_)
        break
    h=hex2ord(hash)
    h_=hex2ord(hash_)



print(record)