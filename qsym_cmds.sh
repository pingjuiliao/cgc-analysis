#!/bin/sh


## sample
## ./qsym_cmds.sh ./cromulence/CROMU_00034/Diary_Parser \
##        ./cromulence/CROMU_00034/i ./cromulence/CROMU_00034/o_qsym
##

tmux new-session -d -s test-fuzzer -n afl-master \
    ./afl-docker.py -i $2 -o $3 -m -p p -t afl:base -- $1
sleep 0.5
tmux new-window -t test-fuzzer:1 -n afl-slave \
    ./afl-docker.py -i $2 -o $3 -s afl-slave -p p -t afl:base -- $1
tmux new-window -t test-fuzzer:2 -n qsym \
    ./qsym-docker.py -a afl-slave -o o -p p -t qsym:base $1
tmux attach -t test-fuzzer
