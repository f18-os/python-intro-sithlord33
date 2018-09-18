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
actual = ["init"]

x = 0

#check of word is already in list or add it
for i in range(len(words)):
    for j in range(len(actual)):
        if words[i] != actual[j]:
            actual.append(words[i])

print len(actual)

#print list using maps
#print('\n'.join(map(str, words)))
    
#f = open(outFileName, "w+")

with open(outFileName, 'w') as f:
    for item in actual:
        print >> thefile, item

#f.write(actual)
