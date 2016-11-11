import sys
import os



def help():
    print ("""
Directory content checker:

Arguments :

    [-f] [arg]     >    filepath
    [-d] [arg]     >    directory
    [-o] [arg]     >    operator
    [-i]           >    ignore filetype (adjust only for names)
    Writes all files found in the directory to the file file specified
    of an operator is given it will instead check contents of both according casual
    set-operations

    == , < , > , != 

    Example :
        dircontentchecker.py -d ./spamspam/egg -f ./eggspam/egg.txt
    or: dircontentchecker.py -d ./spamspam/egg -o < -f ./eggspam/egg.txt
   
""")
    exit()

if sys.argv[1] == "--help":
    help()

filename = None
params = {}
opt = None
ignorefiletypes = False

args = sys.argv
i = 0
for arg in args:

    if i < 2:
        if arg == "-f":       
            params[i] = ("f", args[args.index(arg) + 1])
            filename = params[i][1]            
            i = i + 1
        if arg == "-d":
            params[i] = ("d", args[args.index(arg) + 1])
            i = i + 1
        if arg == "-m":
            params[i] = ("m", "To be inputted")
            i = i + 1

    if arg == "-o":
        opt = args[args.index(arg) + 1]
    if arg == "-i":
        ignorefiletypes = True

def killfiletype(string):
    s = string.find(".")    
    if not s is -1:
        return string[:s]
    return string
        
def getstr(type, val):
           if type is "m":
               val = input("input a string : ")
               splitter  = input ("input split character : ")
               val = val.split(splitter)
               print ("VAL _____________________ ", val)
           if type is "f":
               val = open(val, "r").readlines()
               val = [f.rstrip() for f in val]
           if type is "d":
               val = os.listdir(val)
               
           
           if ignorefiletypes:
               val = [killfiletype(f) for f in val]
           
           return val;

def getsource():
    for pt in params:
        if params[pt][0] != "f":
            return getstr(params[pt][0], params[pt][1])

def mwrite():
    f = open(filename, "w")
    src = getsource()
    print("Write to ", filename)
    i = 0
    for file in src:
        f.write(file + "\n")
        i = i + 1
    print ("listed ", i, " files")
    

if not opt:
    if filename:
        mwrite()
        exit()
    else :
        print("No filename was specified !")
        exit()

if not len(params) is 2:
    print ("not enough arguments")
    exit()



def check(l, r, o):

    for e in l:
        print ("L     ", e)

    print(r)
    for e in r:
        print ("R     ", e)
    
    if o == "<":
        print ("< \n")
        for e in left:
            if not e in right:

                print (e, " ->>>  ", not e in right)
                
                return "FAIL"
        return "SUCCESS"

    elif o == ">":
        print ("> \n")
        return check(right, left, ">")

    elif o == "==":
        print ("== \n")
        if check(left, right, "<") == "SUCCESS" and check(right, left , "<") == "SUCCESS":
            return "SUCCESS"
        return "FAIL"

    elif o == "!=":
        print ("!= \n")
        for e in left:
            if e in right:
                return "FAIL"
            return "SUCCESS"

    else :
        print ("Invalid Operator")
        exit()
        

left = getstr(params[0][0], params[0][1])
right = getstr(params[1][0], params[1][1])

print (check(left, right, opt))
           


