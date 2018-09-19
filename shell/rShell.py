#! /usr/bin/env python3

import sys, os, time, re

def setIns(auxIn):
    uIn = [auxIn[0]]
    out = "p4-output.txt"
      
    i = 1
    while i < len(auxIn):  
        if auxIn[i] == ">":
            if i+1 < len(auxIn):
                out = auxIn[i+1]
            if (i-1) != 0:
                uIn.append(auxIn[i-1])
        elif auxIn[i] == "<":
            if i+1 < len(auxIn):
                uIn.append(auxIn[i+1])
            if (i-1) != 0:
                out = auxIn[i-1]
            else:
                print("Invalid Argument")
                sys.exit(1)
        i += 1
    return uIn, out
