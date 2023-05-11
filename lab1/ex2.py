#!/usr/bin/env python3
# SUTD 50.042 FCS Lab 1
# Simple file read in/out


# Import libraries
import sys
import argparse
import os

def doStuff(filein, fileout):
    result = bytearray()

    with open(filein, mode="rb") as fin:
        c = fin.read()
        for i in range(len(c)):
            byte = c[i]
            x = shift(byte, key)
            result.append(x)
    
    with open(fileout, mode="wb") as fout:
        fout.write(result)


def shift(byte, key):
    new_byte = byte + key
    if new_byte > 255:
        new_byte -= 256
    elif new_byte < 0:
        new_byte += 256
    return new_byte

# our main function
if __name__ == "__main__":
    # set up the argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", dest="filein", help="input file", required=True)
    parser.add_argument("-o", dest="fileout", help="output file", required=True)
    parser.add_argument("-k", dest="key", type=int, help="integer key value; valid range is 0 to 255 inclusive", required=True)
    parser.add_argument("-m", dest="mode", type=str, help="sets the mode; use 'e' for encrypt, 'd' for decrypt", required=True)

    # parse our arguments
    args = parser.parse_args()

    filein = args.filein
    try:
        if not os.path.exists(filein):
            raise argparse.ArgumentTypeError()
    except(argparse.ArgumentTypeError):
        print(f"Error: {filein} does not exist")
        sys.exit()

    fileout = args.fileout

    key = args.key
    try:
        if key < 0 or key > 255:
            raise argparse.ArgumentTypeError()
    except(argparse.ArgumentTypeError):
        print("Error: invalid key; valid range is 0 to 255 inclusive")
        sys.exit()

    mode = args.mode.lower()
    try:
        if mode == "e":
            pass
        elif mode == "d":
            key = -key
        else:
            raise argparse.ArgumentTypeError()
    except(argparse.ArgumentTypeError):
        print("Error: invalid mode; use 'e' for encrypt, 'd' for decrypt")
        sys.exit()
    
    doStuff(filein, fileout)

    # all done
