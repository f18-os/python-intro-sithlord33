#!/usr/bin/env python3

import sys, os, time, re

#executes commands from the PATH
def executeCommand(arg):
    for dir in re.split(":", os.environ["PATH"]):
        prog = "%s/%s" % (dir, arg[0])
        try:
            os.execve(prog, arg, os.environ)
        except FileNotFoundError:
            pass

#write to file        
def toFile(arg):
    if (arg != ""):
        os.close(1)
        sys.stdout = open(arg, "w")
        fd = sys.stdout.fileno()
        os.set_inheritable(fd, True)

def splitRed(arg):
    temp = arg.split(" ")    #splits the list if needed. Part before or after "|" 
    first = [temp[0]]        #first part will always be the first element of the list
    second=""                #we don't know if there will be a second part
    i=1
    while i < len(temp):     #check for I/O redirection
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

#main running function
def run(arg):
    pid = os.getpid()
    os.write(1, ("About to fork (pid=%d)\n" % pid).encode())
    
    #j=0
    isPipe = False
    temp = arg.split(" | ")  #splits the argument to detect if a pipe command was called
    if len(temp)>1:
        isPipe = True
        i=1
        while i<len(temp):         #separates the remaining two parts of the command if it determines a pipe function
            if temp[i][0]==" ":    #portion of code explained and provided by Ricardo Alvarez
                temp[i]=temp[i][1:]
            length = len(temp)-1
            if temp[i][length]==" ":
                length-=1
                temp[i]=temp[i][:length]
            i+=1
    """
    for i in arg: 
        if (i == '|'):
            isPipe =True
            break
        else:
            isPipe=False
        j+=1"""
            
    if isPipe:
        #left = arg[0:j]
        #right = arg [j+1:]
        #print(left)
        #print(right)
        r,w = os.pipe()         #readable and writteable part of piping
        for fd in (r,w):
            os.set_inheritable(fd, True)
                    
    rc = os.fork()              #fork first child
    if rc<0:
        os.write(2, ("fork failed, returning %d\n" % rc).encode())
        sys.exit(1)
    elif rc==0:                       
        first, second = splitRed(temp[0])   #split (if needed) the left part of the command
        if isPipe:
            os.close(1)       #close file descriptor 1
            os.dup(w)         #put writeable part of pipe in open fd
            for i in (r,w):   #close r and w to use in other child
                os.close(i)
        else:
            toFile(second)               #if the command was not a pipe and determines it was an i/O redirection 
        executeCommand(first)            #executes the command 
    else:
        if isPipe:   
            rc2 = os.fork()      #fork second child
            if rc2<0:
                os.write(2, ("fork failed, returning %d\n" % rc).encode())
                sys.exit(1)
            elif rc2==0:
                first, second = splitRed(temp[1])
                os.close(1)
                os.dup(w)
                for i in (r,w):
                    os.close(i)
                    executeCommand(first)
                else:
                    #childPID = os.wait()
                    for pfd in (w,r):
                        os.close(pfd)
        #child2PID = os.wait()


#main function
def main():
    while True:
        arg = input("$ ")
        
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
        run(arg)                          #calls main running method

#this makes python recognize the main function as the first thing to be called        
if __name__ == "__main__":
    main()
                        
