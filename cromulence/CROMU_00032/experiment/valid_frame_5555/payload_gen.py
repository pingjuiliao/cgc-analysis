#!/usr/bin/env python
from pwn import *

with open("../pov_1", "rb") as f :
    pov = f.read()
    f.close()

for i in range(0, 0xffff) :
    payload = pov.replace("\x08\xff", p16(i))
    p = process("../../CGC_Video_Format_Parser_and_Viewer")
    p.send(payload)
    s = p.recvrepeat(1)
    p.shutdown()
    if s.find("ERROR") < 0 :
        filename = "frame_" + str(i)
        print "Writing " + filename + " ..."
        with open("./output/" + filename, "wb") as out :
            out.write(payload)
            out.close()

