#!/usr/bin/env python3

import sys
import argparse
import os

def countLetters(text):
    count = {}
    ref = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for i in range(len(ref)):
        count[ref[i]] = 0

    for i in range(len(text)):
        if text[i] in ref:
            count[text[i]] += 1

    return count

def freqAnalysis(count):
    sortedValues = sorted(count.values())
    freq = ""
    for i in sortedValues:
        if i == 3:
            if "N" not in freq:
                freq += "N"
            else:
                freq += "Z"
        elif i == 50:
            if "V" not in freq:
                freq += "V"
            else:
                freq += "M"
        else:
            for k in count.keys():
                if count[k] == i:
                    freq += k
                    break

    print(freq)
    return freq

def replaceV1(text, freq):
    standard = "qjzxvkwyfbghmpduclsntoirae" #"eariotnslcudpmhgbfywkvxzjq"
    for i in range(26):
        text = text.replace(freq[i], standard[i])
        print(freq[i])
        print(standard[i])
    return text

def replaceV2(text, freq):
    a = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    b = "klmnopqrstuvwxyzabcdefghij"
    standard = "qjzxvkwyfbghmpduclsntoirae"
    for i in range(26):
        if a[i] != b[i]:
            text = text.replace(a[i], b[i])
            freq = freq.replace(a[i], "")
            standard = standard.replace(b[i], "")
    
    for i in range(len(freq)):
        text = text.replace(freq[i], standard[i])
        print(freq[i])
        print(standard[i])

    return text

def doStuff(filein, fileout):
    newText = ""

    with open(filein, mode="r", encoding="utf-8", newline="\n") as fin:
        text = fin.read()
        count = countLetters(text)
        freq = freqAnalysis(count)
        newText = replaceV2(text, freq)
    
    with open(fileout, mode="w", encoding="utf-8", newline="\n") as fout:
        fout.write(newText)

if __name__ == "__main__":
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