#!/usr/bin/env python3
# SUTD 50.042 FCS Lab 1
# Simple file read in/out


# Import libraries
import sys
import argparse
import string
import os

limit = len(string.printable)

def doStuff(filein, fileout):
    result = ""

    with open(filein, mode="r", encoding="utf-8", newline="\n") as fin:
        text = fin.read()
        for i in range(len(text)):
            char = text[i]
            x = shift(char, key)
            result += x
    
    with open(fileout, mode="w", encoding="utf-8", newline="\n") as fout:
        fout.write(result)


def shift(char, key):
    new_index = string.printable.index(char) + key
    if new_index > limit - 1:
        new_index -= limit
    elif new_index < 1:
        new_index += limit
    return string.printable[new_index]

# our main function
if __name__ == "__main__":
    # set up the argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", dest="filein", help="input file", required=True)
    parser.add_argument("-o", dest="fileout", help="output file", required=True)
    parser.add_argument("-k", dest="key", type=int, help="integer key value; valid range is 1 to 99 inclusive", required=True)
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
        if key < 1 or key > limit - 1:
            raise argparse.ArgumentTypeError()
    except(argparse.ArgumentTypeError):
        print("Error: invalid key; valid range is 1 to 99 inclusive")
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
