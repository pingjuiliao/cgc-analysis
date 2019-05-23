#!/usr/bin/env python
import argparse
import os
import sys
import shutil
import time



def main() :
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str, help='input directory')
    parser.add_argument('-o', '--output', type=str, help='output directory' )
    parser.add_argument('-p', '--program', type=str, help='program path')
    ## QEMU mode always disabled
    ## always mounted
    args = parser.parse_args()
    if not args.input or not args.output or not args.program:
        parser.print_help()
        quit()
    if not os.path.exists(args.input) :
        print "Input Path absent"
        quit()
    if not os.path.exists(args.output) :
        print "Output Path absent"
        quit()
    if not os.path.exists(args.program) :
        print "Program absent"
        quit()

    run_command(args)

def run_command(args) :
    user_home = os.environ['HOME']
    if not user_home :
        print "User not exists"
        quit()
    program_directory = os.path.abspath( user_home + \
                        "/cgc-analysis/cb-multios/build/challenges")
    program_path = args.program
    abs_program_path = os.path.abspath(program_path)
    program_name = program_path.split('/')[-1]
    if abs_program_path.find(program_directory) < 0 :
        print "Not a cgc binary in " + program_directory
        quit()
    program_path_in_docker = abs_program_path.replace(program_directory, "/p")
    print program_path_in_docker

    afl_docker = "./afl-docker.py"
    qsym_docker= "./qsym-docker.py"
    libcgc = "./libcgc/libcgc.so"
    libaes = "./libcgc/libtiny-AES128-C.so"
    tmux_tag = program_name + "_Fuzzer"

    afl_master_cmd = ["tmux", "new-session", "-d", "-s",
                     tmux_tag, "-n", "afl-master", \
                    afl_docker,
                    "-i", args.input, "-o", args.output,\
                    "-cgc", libcgc, \
                    "-aes", libaes, \
                    "-p", program_directory, \
                    "-m", "-t", "afl:base-i386", \
                    "--", program_path_in_docker]
    print afl_master_cmd
    afl_slave_cmd = ["tmux", "new-window", "-t", \
                        tmux_tag + ":1", "-n", "afl-slave", \
                        afl_docker, \
                        "-i", args.input, "-o", args.output, \
                        "-cgc", libcgc, \
                        "-aes", libaes, \
                        "-p", program_directory, \
                        "-s", "afl-slave", "-t", "afl:base-i386", \
                        "--", program_path_in_docker]
    print afl_slave_cmd
    qsym_cmd = ["tmux", "new-window", "-t", tmux_tag + ":2", \
                "-n", "qsym", \
                qsym_docker, "-a", "afl-slave", \
                "-o", args.output, \
                "-p", program_directory, \
                "-cgc", libcgc, \
                "-aes", libaes, \
                "-t", "qsym:base", \
                program_path_in_docker]
    print qsym_cmd

    os.system(" ".join(afl_master_cmd))
    os.system(" ".join(afl_slave_cmd))
    time.sleep(.5)
    os.system(" ".join(qsym_cmd))

    os.system("tmux attach -t " + tmux_tag )


    #afl_master = "tmux new-session -d -s test-fuzzer -n afl-master "+ "./afl-docker.py -i i -o o -q -m -p p -t afl:base -- /p/cat"

    #afl_slave = "tmux new-window -t test-fuzzer:1 -n afl-slave " + "./afl-docker.py -i i -o o -q -s afl-slave -p p -t afl:base -- /p/cat"

    #qsym = "tmux new-window -t test-fuzzer:2 -n qsym " + \
        #"./qsym-docker.py -a afl-slave -o o -p p -t qsym:base /p/cat"

    #os.system("tmux attach -t test-fuzzer")


if __name__ == "__main__" :
    main()


