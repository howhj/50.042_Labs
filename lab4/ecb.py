#!/usr/bin/env python3
# ECB wrapper skeleton file for 50.042 FCS

from present import *
import argparse

nokeybits=80
blocksize=64


def ecb(infile,outfile,key,mode):
    with open(infile, mode="r", encoding="utf-8", newline="\n") as fin:
        data = fin.readlines()
        stream = convert64bits(data[4:])
        result = getresult(data, stream)

    with open(outfile, mode="w", encoding="utf-8", newline="\n") as fout:
        fout.writelines(result)

def convert64bits(data):
    stream = []
    block = 0
    counter = 0

    for i in range(len(data)):
        line = data[i].strip()
        pixels = line.split(" ")

        for num in pixels:
            byte = int(num)
            block += byte << 8*(7-counter)
            counter += 1

            if counter == 8:
                stream.append(block)
                block = 0
                counter = 0

    if counter > 0:
        stream.append(block)
    
    return stream

def getresult(data, stream):
    result = []
    for i in range(4):
        result.append(data[i])

    for block in stream:
        if mode == "e":  
            temp = present(block, key)
        elif mode == "d":
            temp = present_inv(block, key)

        line = ""
        for i in range(8):
            byte = temp >> (56-8*i)
            temp -= byte << (56-8*i)
            line += f"{byte}"
            line += " "
        result.append(line.strip() + "\n")
    
    return result

if __name__=="__main__":
    parser=argparse.ArgumentParser(description='Block cipher using ECB mode.')
    parser.add_argument('-i', dest='infile',help='input file')
    parser.add_argument('-o', dest='outfile',help='output file')
    parser.add_argument('-k', dest='keyfile',help='key file')
    parser.add_argument('-m', dest='mode',help='mode')

    args=parser.parse_args()
    infile=args.infile
    outfile=args.outfile
    keyfile=args.keyfile
    mode = args.mode.lower()

    key = 0x0
    with open(keyfile, mode="rb") as keyf:
        data = keyf.read()
        temp = []
        for i in range(len(data)):
            temp.append(data[i])
        
        for i in range(len(temp)):
            key += temp[i] << 8*i

    ecb(infile, outfile, key, mode)

