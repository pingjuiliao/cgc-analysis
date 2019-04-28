#!/usr/bin/python
import os
import sys

DEBUG = 0

def human_readable_bytestring_to_bytes(s) :
    if (len(s)%4) != 0 :
        print "incorrect_length %d for string : %s" % (len(s), s)
        quit()
    string = ""
    for i in range(0, len(s), 4) :
        try:
            x = int(s[i+2:i+4], 16)
            string += chr(x)
        except:
            print "incorrect format of bytes string : %s" % s
            quit()
    return string



def is_pov_dir(p) :
    return p[0:4] == "pov_" and ( 0x30 <= ord(p[4]) and ord(p[4]) <= 0x39)

if len(sys.argv) < 2 :
    print "Usage: %s <path>" % sys.argv[0]
    print "E.g. %s ~/cgc-analysis/cb-multios/challenges/CGC_Planet_Markup_Language_Parser" \
            % sys.argv[0]
    quit()


path = sys.argv[1]
if not os.path.exists(path) and not os.path.isdir(path) :
    print "Path does not exists or it's not an directory"
    quit()

## debug
if DEBUG :
    print os.listdir(path)
    print path

pov_dir_path = [ path + f for f in os.listdir(path) if is_pov_dir(f) ]
print pov_dir_path



#write0_0 = "write_00000_00000[]"

keywords = [ "write_" + str(i).rjust(5, "0") + "_00000[]" for i in range(0, 33000) ]

print keywords

for d in pov_dir_path :
    if not os.path.isdir(d) :
        print "not a directory"
        break
    pov_file = d + "/pov.c"
    if not os.path.exists(pov_file) :
        print "pov_file path not exists"
        break

    f = open(pov_file, "rb")
    content = f.read()
    byte_readable = ""
    for keyword in keywords :
        print "finding keyword %s" % keyword
        if content.find(keyword) < 0 :
            break
        line = content[content.find(keyword):]
        line = line[:line.find(";")]
        start = line.find("=") + 1 ;
        byte_readable += line[start:].replace("\"", "").replace("\n", "").replace(" ", "")

    print "byte_readable is %s with length %d" % (byte_readable, len(byte_readable))
    payload = human_readable_bytestring_to_bytes(byte_readable)
    print "payload is %s with length %d" % (payload, len(payload))

    f.close()

    written_file_name = "./" + d[d.rfind("/")+1:]
    print written_file_name
    with open(written_file_name, "wb") as w :
        w.write(payload)
        w.close()
