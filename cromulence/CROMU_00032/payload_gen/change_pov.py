#!/usr/bin/env python
from pwn import *

gen_file = False

with open("pov_1", "rb") as f :
    pov_1 = f.read()
    f.close()

magic = p16(0xff08)

maximum = 0x10000
count = 0

#replacer = p32(i)
for i in range(1, maximum) :
    replacer = p16(i)
    payload = pov_1.replace(magic, replacer)
    p = process("../CGC_Video_Format_Parser_and_Viewer")
    p.send(payload)
    recv = p.recvall(timeout=5)
    if i % 100 == 0 :
        print i
    if recv.find("[ERROR]") < 0 :
        count += 1
        if gen_file :
            with open("./o/pov_1_replace_" + str(i), "wb") as o :
                o.write(payload)
                o.close()


print "Count/ Total : %d/ %d (%f)" % (count, maximum, count/float(maximum))

