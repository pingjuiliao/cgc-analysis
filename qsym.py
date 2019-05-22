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
    program_directory = os.path.abspath("/home/liaop/cgc-analysis/cb-multios")
    program_path = args.program
    abs_program_path = os.path.abspath(program_path)
    program_name = program_path.split('/')[-1]
    program_path_in_docker = "/p" + abs_program_path[abs_program_path.find("/cb-multios"):]
    print program_path_in_docker

    afl_docker = "~/fuzzers/scripts/afl-docker.py"
    qsym_docker= "~/fuzzers/scripts/qsym-docker.py"

    afl_master_cmd = ["tmux", "new-session", "-d", "-s",
                     program_name + "_Fuzzer", "-n", "afl-master", \
                    afl_docker, "-i", args.input, "-o", \
                    args.output, "-p", "p", "-m", "-t", \
                    "afl:base-i386", "--", program_path_in_docker]
    print afl_master_cmd
    afl_slave_cmd = ["tmux", "new-window", "-t", program_name + "_Fuzzer:1", \
                        "-n", "afl-slave", afl_docker, "-i", args.input, \
                        "-o", args.output, "-p", "p", \
                        "-s", "afl-slave", "-t", "afl:base-i386", \
                        "--", program_path_in_docker]
    qsym_cmd = ["tmux", "new-window", "-t", program_name + "_Fuzzer:2", \
                "-n", "qsym", qsym_docker, "-a", "afl-slave", "-o", args.output, \
                "-p", "p", "-t", "qsym:base", \
                program_path_in_docker]

    if os.path.exists("p") :
        shutil.rmtree("p")
    os.mkdir("p")
    time.sleep(0.5)
    shutil.copytree(program_directory, "./p/" + program_directory)
    os.system(" ".join(afl_master_cmd))
    os.system(" ".join(afl_slave_cmd))
    time.sleep(0.5)
    os.system("tmux attach -t " + program_name + "_Fuzzer")

    #os.system("mkdir i; mkdir o; cp /etc/passwd i; mkdir p; cp /bin/cat p/cat")

    #afl_master = "tmux new-session -d -s test-fuzzer -n afl-master "+ "./afl-docker.py -i i -o o -q -m -p p -t afl:base -- /p/cat"

    #afl_slave = "tmux new-window -t test-fuzzer:1 -n afl-slave " + "./afl-docker.py -i i -o o -q -s afl-slave -p p -t afl:base -- /p/cat"

    #qsym = "tmux new-window -t test-fuzzer:2 -n qsym " + \
        #"./qsym-docker.py -a afl-slave -o o -p p -t qsym:base /p/cat"

    #os.system("tmux attach -t test-fuzzer")


if __name__ == "__main__" :
    main()


