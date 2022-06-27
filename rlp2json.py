#!/usr/bin/env python3
import sys
import argparse

def read_binary_stdin():
    return sys.stdin.buffer.read(1)[0]

def read_hex_stdin():
    return int(sys.stdin.read(2), 16)

def write(s):
    print(s, end = "")

def get_len(ll):
    l = 0
    for _ in range(ll):
        l = l * 256 + read_byte()
    return l

# return total bytes read
def parse():
    b = read_byte()
    if b < 0xC0:
        write("\"")
        if b < 0x80:
            total = 1
            write("%02x" % b)
        else:
            if b < 0xB8:
                l = b - 0x80
                total = 1 + l
            else:
                ll = b - 0xB8 + 1   # length of L
                l = get_len(ll)
                total = 1 + ll + l
            for _ in range(l):      # L bytes of content
                write("%02x" % read_byte())
        write("\"")
    else:
        write("[")
        if b < 0xF8:
            l = b - 0xC0
            total = 1 + l
        else:
            ll = b - 0xF8 + 1       # length of L
            l = get_len(ll)
            total = 1 + ll + l
        if l > 0:                   # L bytes of content
            l -= parse()
            while l > 0:
                write(",")
                l -= parse()
        write("]")
    return total

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(add_help=False)
    arg_parser.add_argument("--help", action="help")

    group = arg_parser.add_mutually_exclusive_group()
    group.add_argument("-h", "--hex",
        action="store_true", help="hex input (default)")
    group.add_argument("-b", "--binary",
        action="store_true", help="binary input")

    args = arg_parser.parse_args()
    if args.binary:
        read_byte = read_binary_stdin
    else:
        read_byte = read_hex_stdin

    parse()
