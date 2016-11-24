## you need a file called sqlkeywords.txt in the directory of the script
## the script contains the lot of sql keywords you can find... feel free to add


import sys

if len(sys.argv) != 2:
 exit()

file = open(sys.argv[1], "r")

text = ""
for line in file:
 text += line.lower()

words = open("sqlkeywords.txt", "r")

print text
print words

def findandcaps(words, text):
 for word in words:
  word = word.strip()
  text = text.replace(word.lower(), word.upper()) 
 return text

file.close()
file = open(sys.argv[1], "w")
file.write(findandcaps(words, text))
file.close()
words.close()


