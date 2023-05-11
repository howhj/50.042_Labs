#!/usr/bin/env python3
# ECB plaintext extraction skeleton file for 50.042 FCS

import argparse

def getInfo(headerfile):
    with open(headerfile, mode="r", encoding="utf-8", newline="\n") as fhead:
        return fhead.read() + "\n"

def extract(infile,outfile,headerfile):
    with open(infile, mode="rb") as fin:
        result = getInfo(headerfile)

        data = fin.read()
        arr = bytearray()
        for i in range(15, len(data)):
            arr.append(data[i])

        string = ""
        counter = 0
        for byte in arr:
            string += f"{byte} "
            counter += 1
            if counter == 10:
                result += string.strip() + "\n"
                string = ""
                counter = 0

    with open(outfile, mode="w", encoding="utf-8", newline="\n") as fout:
        fout.write(result)
    
    return True

if __name__=="__main__":
    parser=argparse.ArgumentParser(description='Extract PBM pattern.')
    parser.add_argument('-i', dest='infile',help='input file, PBM encrypted format')
    parser.add_argument('-o', dest='outfile',help='output PBM file')
    parser.add_argument('-hh', dest='headerfile',help='known header file')

    args=parser.parse_args()
    infile=args.infile
    outfile=args.outfile
    headerfile=args.headerfile

    print('Reading from: %s'%infile)
    print('Reading header file from: %s'%headerfile)
    print('Writing to: %s'%outfile)

    success=extract(infile,outfile,headerfile)

            
