#!/usr/bin/python

with open("../pov_1", "rb") as f:
    pov = f.read()
    f.close()

for i in range(4, 100, 4) :
    payload = pov[:-i]
    filename = "shorten_" + str(i).rjust(3, "0")
    with open("./output/" + filename, "wb") as out:
        out.write(payload)
        out.close()
