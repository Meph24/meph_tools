import sys
import re

#TODO
def help():
 print('Help !')

def error(code):
 print('Error:\n' + code)

inputf = 0
outputf = 0
mashineID = 0
#args are input filename, output filename, mashineID
if (len(sys.argv) == 4):
 inputf = sys.argv[1]
 outputf = sys.argv[2]
 mashineID = sys.argv[3]
elif (len(sys.argv) == 1):
 print("Manual input routine :")
 inputf = input("please type your dea description file")
 outputf = input("please type the filename/path to the output file")
 mashineID = input ("please type a unique name for the mashine")
	
else:	
 help()
 exit()

#TODO arg checking with regex



inputf = open(inputf, "r")
input = inputf.readlines()

print(input)

alphalist = []
funclist = []

for line in input:
 line = line.replace(" ", "")
 line = line.rstrip("\n")

 if re.match("Q:[{].*[}]", line):
  qstatement = line
 if re.match("s[(][a-zA-Z_][\w]*[)]:[{].*[}]", line):
  alphalist.append(line)
 if re.match("d[(][a-zA-Z_][\w]*[,].*[)]*[=]*", line):
  funclist.append(line)
 if re.match("q0:", line):
  startstate = line
 if re.match("F:[{].*[}]", line):
  finitestates = line
        
print(qstatement)
print(alphalist)
print(funclist)
print(startstate)
print(finitestates)

def getStatesFromSet(states):
 states = re.search("[{].*[}]", states).group()
 states = (states.strip('{}'))
 states = states.split(',')
 states = [q.strip() for q in states]
 return states

qstatement = getStatesFromSet(qstatement)
finitestates = getStatesFromSet(finitestates)

print(qstatement)
print(finitestates)

startstate = (startstate.split(':'))[1].strip()

print(startstate)

def getSubExpression(istr):
 if istr == "":
  return "(1)"
 if istr.find("\\") !=  -1:
  istr = istr.split("\\")
  return "(" + getSubExpression(istr[0]) + "&& !"+ getSubExpression(istr[1])+ ")"
 elif istr.find("-") != -1:
  istr = istr.split("-")
  return "((sym >= '" + istr[0].strip() + "') && (sym <= '" + istr[1].strip()+ "'))"
 else :
  return "(sym == '" + istr + "')"

def getExpression(istr):
 istr = istr.split(",")
 istr = (x.strip() for x in istr)
 retstr = ""
 for s in istr:
  retstr += (getSubExpression(s) + " || ")        
 retstr = "("+retstr[:-4]+")"
 return retstr

def tuplelize(istr):
 name = re.search("[(][\w]*[)]", istr)
 name = name.group()
 name = name.strip("()")
 expr = re.search("[{].*[}]", istr)
 expr = expr.group()   
 expr = expr.strip("{}") 
 expr = getExpression(expr)
 istr = (name, expr)
 return istr

def getAlphabeth(ilist):
 ilist = [tuplelize(x) for x in ilist]
 dict = {}
 for x in ilist:
  dict[x[0]] = x[1]
 return dict
    
alphalist = getAlphabeth(alphalist)

def getFunction(istr):
 istr = istr.split("=")
 print(istr)
 left = re.search("[(].*[)]", istr[0])
 left = left.group()
 left = left.strip("()")
 left = left.split(",")
 param1 = left[0]
 param2 = left[1]
 res = istr[1]
 return (param1 , (param2, res))
    
funclist = [getFunction(x) for x in funclist]

def funcjoin(l):
 fl = []
 innerlist = []
 for x in qstatement:
  for y in l:
   if x == y[0]:
    innerlist.append(y[1])
  fl.append((x, innerlist))
  innerlist = []
        
 return fl

funclist = funcjoin(funclist)

inputf.close()

#now we can print to a file

writef = open (outputf, 'w')



#writing standard header

writef.write(
    """
#ifndef DEACODER_STATEMASHINE
#define DEACODER_STATEMASHINE
struct deacoder_statemashine
{
\tint q;
};
#endif
""")

#write state enum

writef.write(
    """
enum """ + mashineID.lower() + """_states
{
\ttrap = -1,\t\t//default trap state
""")

i = 0
for x in qstatement:
 writef.write("\t" + qstatement[i] + " = " + str(i) +",\n")
 i += 1

writef.write("""
\tNUM_"""+mashineID.upper()+"""_STATES
};
""")

#write init function
writef.write("""
void """+ mashineID.lower() + """_init(deacoder_statemashine* M)
{
    M->q = """+ mashineID.lower() + """_states::"""+startstate+""";
}
""")

#write d funtion
writef.write("""
void """+ mashineID.lower() + """_d(deacoder_statemashine* M, char sym)
{
    switch(M->q)
    {
    """)

def writeif(wf):
 wf.write("""
\t\t\tif(""" + alphalist[ifst[0]] + """)
\t\t\t{
\t\t\t    M->q = """+ mashineID.lower() + """_states::""" + ifst[1] + """;
\t\t\t}
""")

def writeelseif(wf):
 wf.write("""
\t\t\telse if(""" + alphalist[ifst[0]] + """)
\t\t\t{
\t\t\t    M->q = """+ mashineID.lower() + """_states::""" + ifst[1] + """;
\t\t\t}
""")

for func in funclist:
 if func[1] != []:       
  writef.write("""
\t\tcase """+ mashineID.lower()+"""_states::"""+ func[0]+ """:
""")
  i = 0
  for ifst in func[1]:
   if i == 0 :
    writeif(writef)
   else:
    writeelseif(writef)
   i += 1
	    
  writef.write("""
\t\t\telse
\t\t\t{
\t\t\t    M->q = """+ mashineID.lower() + """_states::trap;
\t\t\t}

\t\tbreak;
""")



writef.write("""
\t\tcase """ + mashineID.lower() + """_states::trap:
\t\tdefault:
\t\tbreak;
\t\t}
}
""")

#at last the exit function
writef.write("""
int """ + mashineID.lower() +"""_exit(deacoder_statemashine* M)
{
	int cs = M->q;
	return (""")

i = 0
for f in finitestates:
 if i != 0:
  writef.write(" || ")
 writef.write("(M->q == " + f + ")")
 i += 1

writef.write(""");
}""")

writef.close()


        



