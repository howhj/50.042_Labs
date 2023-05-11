#!/usr/bin/env python3

import sys
import argparse
import os
import hashlib
import random

ref = "abcdefghijklmnopqrstuvwxyz"

def saltedhash(pt):
    i = random.randrange(0, 26)
    pt = pt.strip() + ref[i]
    hashed = hashlib.md5(pt.encode()).hexdigest()
    return pt, hashed


def doStuff(filein, fileoutp, fileouth):
    random.seed(100) # static seed for reproducability
    resultp = ""
    resulth = ""

    with open(filein, mode="r", encoding="utf-8", newline="\n") as fin:
        for line in fin:
            res = saltedhash(line)
            resultp += res[0] + "\n"
            resulth += res[1] + "\n"
    
    with open(fileoutp, mode="w", encoding="utf-8", newline="\n") as fout:
        fout.write(resultp)
    
    with open(fileouth, mode="w", encoding="utf-8", newline="\n") as fout:
        fout.write(resulth)

if __name__ == "__main__":
    # set up the argument parser
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", dest="filein", help="input file", required=True)
    parser.add_argument("-op", dest="fileoutp", help="output file", required=True)
    parser.add_argument("-oh", dest="fileouth", help="output file", required=True)

    # parse our arguments
    args = parser.parse_args()
   
    filein = args.filein
    try:
        if not os.path.exists(filein):
            raise argparse.ArgumentTypeError()
    except(argparse.ArgumentTypeError):
        print(f"Error: {filein} does not exist")
        sys.exit()

    fileoutp = args.fileoutp
    fileouth = args.fileouth

    doStuff(filein, fileoutp, fileouth)