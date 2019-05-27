#!/usr/bin/env python
from pwn import *

with open("../pov_1", "rb") as  :
    pov = f.read()
    f.close()

for i in range(0, 0xffff) :
    payload = pov.replace("\x08\xff", u16(i))
    p = process("../../")
