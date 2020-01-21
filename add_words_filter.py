import json
import string

json_file = open("badwords2.json")
data = json.load(json_file)
json_file.close()


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

while True:
  word = input("word: " )

  if word=="exit":
     break
  else:
    maskedWord = maskBadWord(word)
    data["badwords"].append(maskedWord)
    data["badwords"].sort()
    print(data)
    outfile = open("badwords2.json", "w")
   
    json.dump(data, outfile)
    outfile.close()

