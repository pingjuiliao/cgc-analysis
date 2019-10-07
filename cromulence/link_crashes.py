#!/usr/bin/python
import os
import sys
from shutil import rmtree

def is_one_of_the_crash(filename) :
    return filename[0:3] == "id:"

def main() :
    if not os.path.isdir("o") :
        print "fuzzing result not found !"
        quit()

    if not os.path.isdir("o/crashes") :
        print "fuzzing result not found !"
        quit()

    srcs = [ f for f in os.listdir("o/crashes") if is_one_of_the_crash(f) ]
    print srcs

    if len(srcs) < 0 :
        print "no crashes file to symlink"
        quit()

    target_dir = "./linked_crashes"
    if os.path.exists(target_dir) :
        rmtree(target_dir)

    os.mkdir(target_dir)

    for src in srcs :
        src_path = "../o/crashes/" + src

        dst_path = target_dir + "/" + "id" + str(int(src[3:9]))
        os.symlink(src_path, dst_path)


s = \
"""
###########################################################################################################
## sometimes crashes are too much  and we dont want to type ./binary < o/crashes/id:000001:09fkwsoijfqooiqwj
##                                                          ./binary < o/crashes/id:000002:qwifkjwopqifjwiqo
##                                                          ...............(too much work) ................
##
## so we symlink them to ./id0, ./id1, ./id2 ......
############################################################################################################
"""

if __name__ == '__main__' :
    print s
    main()
