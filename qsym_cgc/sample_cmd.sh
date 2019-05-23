#!/bin/sh
sudo rm -rf i o p
mkdir i o
echo "a" | tr -d '\n' > i/seed
tmux new-session -d -s test-fuzzer -n afl-master \
    ./afl-docker.py -i i -o o -cgc ./libcgc/libcgc.so \
    -aes ./libcgc/libtiny-AES128-C.so \
    -p ../cb-multios/build -m -t afl:base-i386 -- /p/challenges/Diary_Parser/Diary_Parser
