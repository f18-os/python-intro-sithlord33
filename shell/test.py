#!/usr/bin/env python3

import sys, os, time, re

def execFile(args, out):
    os.close(1)
    sys.stdout = open(out, "w")
    fd = sys.stdout.fileno()
    os.set_inheritable(fd, True)
    os.write(2, ("Child: opened fd=%d for writing\n" % fd).encode())
    for dir in re.split(":", os.environ["PATH"]):
        prog = "%s/%s" % (dir, args[0])
        try:
            os.execve(prog, args, os.environ)
        except FileNotFoundError:
            pass

def execScreen(args):
    for dir in re.split(":", os.environ["PATH"]):
        prog = "%s/%s" % (dir, args[0])
        try:
            os.execve(prog, args, os.environ)
        except FileNotFoundError:
            pass
    

def main():
    while True:
        r, w = os.pipe()
        
        cm = input("" ).split()
        #print(cm)
        
        if cm[0] == 'exit':  
            sys.exit()

        run(cm)

def run(cm):
    pid = os.getpid()
    os.write(1, ("About to fork (pid=%d)\n" % pid).encode())
    rc = os.fork()
    
    if "|" in cm:
        j = 0
        for i in cm:    
            if i == "|":  
                break
            j += 1
        left = cm[0:j]
        print(left)
        right = cm[(j+1):]
        print(right)
                
        if rc<0:        
            os.write(2, ("fork failed, returning %d\n" % rc).encode())
            sys.exit(1)
        elif rc==0:
            if "<" in left:
                sys.exit(1)
            elif ">" in right:
                sys.exit()
            else:
                os.close(1)
                os.dup(w)
                for i in (r,w):
                    os.close(i)
                fd = sys.stdout.fileno()
                os.set_inheritable(fd, True)
                os.write(2, ("Child: opened fd=%d for writing\n" % fd).encode())
                execScreen(left)
        os.wait()
        os.close(0)
        os.dup(r)
        for i in (r,w):
            os.close(i)
        fd = sys.stdin.fileno()
        os.set_ingeritable(fd, True)
        os.write(2, ("Child: opened fd=%d for writing\n" % fd).encode())
        execscreen(right)
                            
    elif "<" in cm:
        if len(cm) == 3:
            args = [cm[0], cm[2]]
            execScreen(args)
        else:
            args = [cm[0], cm[3]]
            out = cm[1]
            execFile(args, out)
    elif ">" in cm:
        args = [cm[0], cm[1]]
        out = cm[3]
        execFile(args, out)
    else:
        execScreen(cm)
        os.write(1, ("Parent: My pid=%d. Child's pid=%d\n" % (pid, rc)).encode())
                    
                        

if __name__ == "__main__":
        main()
