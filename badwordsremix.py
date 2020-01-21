import json
import string

def loadBadWords(): 
 json_file = open("badwords.json")
 data = json.load(json_file)
 json_file.close()
 return data["badwords"]

def maskBadWord(word):
   letters = list(string.ascii_lowercase)
   wordList = list(word)
   for x in range(0, len(wordList)):
      letter = wordList[x]
      #print("letter:" + letter)
      letterindex = string.ascii_lowercase.index(letter.lower())
      nextletterIndex = letterindex + 1
      nextletter = letters[nextletterIndex]
      wordList[x] = nextletter
       
   newword = "".join(wordList)
   return newword

def unmaskBadWord(word):
   letters = list(string.ascii_lowercase)
   wordList = list(word)
   for x in range(0, len(wordList)):
      letter = wordList[x]
      #print("letter:" + letter)
      letterindex = string.ascii_lowercase.index(letter.lower())
      nextletterIndex = letterindex - 1
      nextletter = letters[nextletterIndex]
      wordList[x] = nextletter
       
   badword = "".join(wordList)
   return badword

badwords = loadBadWords()

for x in range(0,len(badwords)):
   word = badwords[x]
   maskedword = maskBadWord(word)
   badword = unmaskBadWord(maskedword)
   #print(maskedword + "|" + badword)
   badwords[x] = maskedword


print(badwords)

json_data = {}
json_data["badwords"] = badwords
outfile = open("badwords2.json", "w")
json.dump(json_data,outfile)
outfile.close()
