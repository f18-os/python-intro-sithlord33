import sys
import re
import os
import subprocess

#sentence = "Hello, world!"
#print sentence
#print len(sentence)

inFileName = sys.argv[1]
outFileName = sys.argv[2]

f = open(inFileName, "r+")

contents = f.read()

words = contents.split()
actual = ["none"] * 10

for i in words:
    for j in actual:
        if i == j:
            #actual.append(i)

print len(actual)

for x in range(len(actual)):
    print actual(x)
    
f = open(outFileName, "w+")

#f.write(actual)
