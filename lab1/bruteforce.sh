#!/bin/bash

rm -r result
mkdir result
touch result/file.txt
for i in {0..255}
do
    python3 ex2.py -i flag -o result/out${i} -k ${i} -m d
    file result/out${i} >> result/file.txt
done
