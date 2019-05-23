#!/usr/bin/env python

import argparse
import os
import subprocess


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--afl', type=str,
            help='afl-slave tag')
    parser.add_argument('-o', '--output', type=str,
            help='fuzzing output directory')
    parser.add_argument('-p', '--program', type=str,
            help='fuzzing program directory')
    parser.add_argument('-t', '--imagetag', type=str,
            help='image tag', required=True)
    parser.add_argument('-cgc', '--libcgc', type=str,
            help='path of libcgc.so', required=True)
    parser.add_argument('-aes', '--libaes', type=str,
            help='path of libtiny-AES128-C.so', required=True)
    parser.add_argument('cmdline', nargs='*')
    args = parser.parse_args()

    cmdline = ['docker', 'run', '-it', '--rm',
            '--cap-add=SYS_PTRACE',
            '--mount',
            "type=bind,source={},target=/o".format(os.path.abspath(args.output)),
            '--mount',
            "type=bind,source={},target=/p".format(os.path.abspath(args.program)),
            '--mount',
            "type=bind,source={},target=/lib32/libcgc.so".format(os.path.abspath(args.libcgc)),
            '--mount',
            "type=bind,source={},target=/lib32/libtiny-AES128-C.so".format(os.path.abspath(args.libaes)),
            args.imagetag,
            '/workdir/qsym/bin/run_qsym_afl.py', '-a', args.afl, '-o', '/o', '-n', 'qsym', '--']

    cmdline += args.cmdline

    print(cmdline)
    print(' '.join(cmdline))
    os.system(' '.join(cmdline))

if __name__ == '__main__':
    main()
