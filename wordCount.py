import sys
import re
import os
import subprocess

#sentence = "Hello, world!"
#print sentence
#print len(sentence)

#input and output text files
inFileName = sys.argv[1]
outFileName = sys.argv[2]

f = open(inFileName, "r+")

contents = f.read()

#list of words in the input file
words = contents.split()
#list of words not repeated
actual = []

#check of word is already in list or add it
for i in words:
    for j in actual:
        if i != j:
            actual.append(i)

#print(*words, sep = "\n"),
print('\n'.join(map(str, words)))
    
f = open(outFileName, "w+")

#f.write(actual)
