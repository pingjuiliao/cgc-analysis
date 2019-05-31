#!/usr/bin/python
import os
from pwn import *
from random import randint

### params
injection_times = 2



p16_list = []
for s in os.listdir("./output_2222") :
    num_s = s[s.find("_")+1:]
    try :
        n = int(num_s)
        p16_list.append(n)
    except :
        continue

with open("../pov_1", "rb") as f :
    pov = f.read()
    f.close()



prefix = "\x22\x22"
idx_list = []
for _ in range(injection_times) :
    index = 14 + 4 * randint(0, 1016/4)
    idx_list.append(index)

idx_list = sorted(idx_list)
print idx_list
payload = pov

for i in range(0, injection_times) :
    idx = idx_list[i] + i * 4
    seq = p16(0x2222) + p16(p16_list[randint(0, len(p16_list)-1)])
    payload = payload[:idx] + seq + payload[idx:]


with open("payload" , "wb") as o :
    o.write(payload)
    o.close()
