#!/usr/bin/env python3

import sys, os, time, re

def executeCommand(arg):
    for dir in re.split(":", os.environ["PATH"]):
        prog = "%s/%s" % (dir, arg[0])
        try:
            os.execve(prog, arg, os.environ)
        except FileNotFoundError:
            pass
        
def toFile(arg):
    if (arg == ""):
        os.close(1)
        sys.stdout = open(arg, "w")
        fd = sys.stdout.fileno()
        os.set_inheritable(fd, True)

def splitRed(arg):
    temp = arg.split(" ")
    first = [temp[0]]
    second=""
    i=1
    while i < len(temp): 
        if temp[i] == ">":
            if i+1 < len(temp):
                second = temp[i+1]
            if (i-1) != 0:
                    first.append(temp[i-1])
        elif temp[i] == "<":
            if i+1 < len(temp):
                first.append(temp[i-1])
            if (i-1) != 0:
                second = temp[i+1]
            else:
                print("Invalid Argument")
                sys.exit(1)
        elif len(temp) ==2:
            first.append(temp[1])
            i+=1
    return first, second
                    
def changeDir(arg):                        
    try:         
        os.chdir(arg)
    except:
        os.write(3, ("\nIncorrect location\n").encode())

def run(arg):
    pid = os.getpid()
    os.write(1, ("About to fork (pid=%d)\n" % pid).encode())
    
    j=0
    for i in arg: 
        if (i == '|'):
            isPipe =True
            break
        else:
            isPipe=False
        j+=1
            
    if isPipe:
        left = arg[0:j]
        right = arg [j+1:]
        #print(left)
        #print(right)
        r,w = os.pipe()
        for fd in (r,w):
            os.set_inheritable(fd, True)
                    
    rc = os.fork()
    if rc<0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)
    elif rc==0:                       
        first, second = splitRed(arg)
        if isPipe:
            os.close(1)
            os.dup(w)
            os.close(1)
            os.dup(w)
            for i in (r,w):
                os.close(i)
        else:
            toFile(second)
            executeCommand(first)
    else:
        if isPipe:   
            rc2 = os.fork()
            if rc2<0:
                os.write(2, ("fork failed, returning %d\n" % rc).encode())
                sys.exit(1)
            elif rc2==0:
                first, second = splitRed(right)
                os.close(1)
                os.dup(w)
                os.close(1)
                os.dup(w)
                for i in (r,w):
                    os.close(i)
                    executeCommand(first)
                else:
                    childPID = os.wait()
                    for pfd in (w,r):
                        os.close(pfd)
        child2PID = os.wait()


def main():
    while True:
        arg = input("" ).split()
        
        #print(arg)
        if arg:
            if arg[0] == 'exit': 
                sys.exit()
            if arg[0:2] == "cd":
                try:
                    changeDir(arg[3:])
                except:
                    print("Incorrect path")
                    pass
                    
        #if (arg[0] != "" ):
        run(arg)
                    
if __name__ == "__main__":
    main()
                        
