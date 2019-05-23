#!/usr/bin/env python

import argparse
import os
import subprocess


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--input', type=str,
            help='fuzzing input directory')
    parser.add_argument('-o', '--output', type=str,
            help='fuzzing output directory')
    parser.add_argument('-p', '--program', type=str,
            help='fuzzing program directory')
    parser.add_argument('-m', '--master', action="store_true",
            help='set as master')
    parser.add_argument('-s', '--slave', type=str,
            help='slave tag')
    parser.add_argument('-cgc', '--libcgc', type=str,
            help='libcgc.so path') ## load library into /lib32/libcgc.so
    parser.add_argument('-aes', '--libaes', type=str,
            help='libtiny-AES128-C.so path')
    parser.add_argument('-q', '--qemu', action="store_true",
            help='use QEMU mode')
    parser.add_argument('-t', '--imagetag', type=str,
            help='image tag', required=True)

    parser.add_argument('cmdline', nargs='*')
    args = parser.parse_args()

    cmdline = ['docker', 'run', '-it', '--rm',
            '--cap-add=SYS_PTRACE',
            '--mount',
            "type=bind,source={},target=/i".format(os.path.abspath(args.input)),
            '--mount',
            "type=bind,source={},target=/o".format(os.path.abspath(args.output)),
            '--mount',
            "type=bind,source={},target=/p".format(os.path.abspath(args.program)),
            '--mount',
            "type=bind,source={},target=/lib32/libcgc.so".format(os.path.abspath(args.libcgc)),
            '--mount',
            "type=bind,source={},target=/lib32/libtiny-AES128-C.so".format(os.path.abspath(args.libaes)),
            args.imagetag,
            '/afl/afl-fuzz', '-m', '8192', '-i', '/i', '-o', '/o']
    if args.qemu:
        cmdline.append('-Q')
    if args.master:
        cmdline.append('-M')
        cmdline.append('afl-master')
    else:
        if args.slave != None:
            cmdline.append('-S')
            cmdline.append(args.slave)

    cmdline.append('--')

    cmdline += args.cmdline

    print(cmdline)
    print(' '.join(cmdline))
    os.system(' '.join(cmdline))

if __name__ == '__main__':
    main()
