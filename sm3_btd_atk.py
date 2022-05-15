from gm import sm3
import string
import random
import time
start_time = time.time()
N = 32
TRUNC = 8
char_set = string.ascii_letters+string.digits
trial_times = 0
record = {}

def reduced_sm3(m):
    return sm3.SM3(m)[:TRUNC]


def get_random_input():
    random_input = ''.join(random.sample(char_set, N))
    res = ''
    for x in random_input:
        res += str(ord(x))
    return res


hash = ''
random_input = ''

for i in range(1200000):
    print(trial_times)
    trial_times+=1
    random_input = get_random_input()
    hash = reduced_sm3(random_input)
    if hash not in record.keys():
        try: 
            record[hash] = random_input
        except MemoryError:
            print("LOG: MemoryError")
            hashed_dict = {}
    else:
        if record[hash] == random_input:
            print("String Already Used!")
            print("Number of evaluations made so far", trial_times)
        else:
            break

colliding=record[hash]
colliding_hash=reduced_sm3(colliding)
print(colliding,random_input)
print(colliding_hash)
