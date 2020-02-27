import subprocess
import re
import json
import string

movietitle = input("title: ")
f = open(movietitle+".srt") 
subtitle_string = f.read() 
f.close()
json_data = {} 
sublist = subtitle_string.split("\n\n") 
#print(sublist)


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

def get_sec(time_str):
    """Get Seconds from time."""
    h, m, s = time_str.split(':')
    splitseconds = s.split(",")
    s = splitseconds[0]
    return int(h) * 3600 + int(m) * 60 + int(s)

def getId(sub):
   id = 1
   return id

def getStart(sub):
  time = '1:23:45'
  result = get_sec(time)
  return result

def getEnd(sub):
  time = '0:00:45'
  result = get_sec(time)
  return result

def getText(sub):
  result = "hello"
  return result

def findWholeWord(w):
    return re.compile(r'\b({0})\b'.format(w), flags=re.IGNORECASE).search


def loadBadWords(): 
 json_file = open("C:\\Users\\14400\\PythonProjects\\bad-language-filter\\create-filtered-movie\\badwords2.json")
 data = json.load(json_file)
 json_file.close()
 return data["badwords"]

badids = []
badlanguage = loadBadWords()

#command = "#!/usr/bin/env bash\n\n"

numberofbadlanguage = 0
for i in range(0, len(sublist)-1):
 #print(sublist[i]+"\n\n")
 id = i
 split = sublist[i].split("\n")
 
 time = split[1]
 timesplit  = time.split(" --> ")
 #print(timesplit)
 start = get_sec(timesplit[0])-1 
 end = get_sec(timesplit[1])+2
 
 #print(word_list)
 #print(word)
 #print(split[2])
 time = [start, end]
 text = split[2].lower()
 if len(split)>3:
    text+= " " + split[3].lower()
 found = []
 for word in badlanguage:
  unmasked = unmaskBadWord(word)
  p = re.search(r"\b" + re.escape(unmasked) + r"\b", text) 
  if p:
    found.append(word)

         #command += "volume=enable='between(t," + str(start) + "," + str(end) + ")':volume=0, " + "\\\n"
   #numberofbadlanguage+=1
    #print(str(id) + sublist[i])
   #badids.append(time)
 
 if len(found)!=0:
   #print(found)
      #print(str(id) + split[3].lower())
   badids.append(time)
      #numberofbadlanguage+=1

 json_data[id] = {}
 json_data[id]["start"] = int(start)
 json_data[id]["end"] = int(end)
 json_data[id]["text"] = text
 text = ""
#print(json_data) 

#print(badids)
#print("total:" + str(numberofbadlanguage))
filter_text = ""
for start, end in badids:
  filter_text += "volume=enable='between(t," + str(start) + "," + str(end) + ")':volume=0, "

filter_text = filter_text[:-2]
f = open("filter.txt", "w")
f.write(filter_text)
f.close()
command = "ffmpeg -i " + movietitle + ".mp4 -filter_complex_script \"filter.txt\" -vf subtitles="+movietitle+"-filtered.srt:force_style='Alignment=6' "+ movietitle + "-filtered.mp4"

print(command)


for word in badlanguage:
 unmasked = unmaskBadWord(word)
 if re.search(unmasked, subtitle_string, re.IGNORECASE):
     r = re.compile(r"\b"+re.escape(unmasked)+ r"\b", re.IGNORECASE)
     subtitle_string = r.sub(r'***', subtitle_string)

f = open(movietitle+"-filtered.srt", "w")
f.write(subtitle_string)
f.close()

subprocess.call(command, shell=True)
