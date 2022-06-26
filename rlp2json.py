import sys
import argparse

def read_binary_stdin():
    return sys.stdin.buffer.read(1)[0]

def read_hex_stdin():
    return int(sys.stdin.read(2), 16)

def write(s):
    print(s, end = "")

def get_len(l):
    if l >= 0x38:
        lenlen = l - 0x38 + 1
        l = 0
        for _ in range(lenlen):
            l = l * 256 + read_byte()
        return l, lenlen
    else:
        return l, 0

# return total bytes read
def parse():
    b = read_byte()
    if b >= 0xC0:
        write("[")
        l, lenlen = get_len(b - 0xC0)
        todo = l
        if todo > 0:
            while True:
                todo -= parse() 
                if todo <= 0:
                    break
                write(",")
        write("]")
    else:
        write("\"")
        if b < 0x80:
            l, lenlen = 0, 0
            write("%02x" % b)
        else:
            l, lenlen = get_len(b - 0x80)
            for _ in range(l):
                write("%02x" % read_byte())
        write("\"")
    return 1 + lenlen + l

if __name__ == "__main__":
    arg_parser = argparse.ArgumentParser(add_help=False)
    arg_parser.add_argument("--help", action="help")

    group = arg_parser.add_mutually_exclusive_group()
    group.add_argument("-h", "--hex", action="store_const", dest="input_type",
        const="hex", help="hex input (default)")
    group.add_argument("-b", "--binary", action="store_const", dest="input_type",
        const="binary", help="binary input")
    group.set_defaults(input_type="hex")

    args = arg_parser.parse_args()
    if args.input_type == "binary":
        read_byte = read_binary_stdin
    else:
        read_byte = read_hex_stdin

    parse()