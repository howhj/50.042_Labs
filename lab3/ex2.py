#!/usr/bin/env python3

import sys
import argparse
import os
import hashlib
import time

ref = "abcdefghijklmnopqrstuvwxyz0123456789"

def decrypt(hash):
    for a in range(36):
        for b in range(36):
            for c in range(36):
                for d in range(36):
                    for e in range(36):
                        test = ref[a] + ref[b] + ref[c] + ref[d] + ref[e]
                        #print(f"{hashlib.md5(test.encode())}\n")
                        if f"{hashlib.md5(test.encode()).hexdigest()}\n" == hash:
                            print(test)
                            return test
    print("FAILED!")
    return "FAILED!"


def doStuff(filein, fileout):
    result = ""

    with open(filein, mode="r", encoding="utf-8", newline="\n") as fin:
        for line in fin:
            result += decrypt(line) + "\n"
    
    with open(fileout, mode="w", encoding="utf-8", newline="\n") as fout:
        fout.write(result)

if __name__ == "__main__":
    start_time = time.time()

    # set up the argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", dest="filein", help="input file", required=True)
    parser.add_argument("-o", dest="fileout", help="output file", required=True)

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

    doStuff(filein, fileout)

    print(f"{time.time() - start_time} sec")