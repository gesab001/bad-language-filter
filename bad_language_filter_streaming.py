import subprocess
import re
import json

movietitle = input("title: ")
f = open(movietitle+".srt") 
subtitle_string = f.read() 
f.close()
json_data = {} 
sublist = subtitle_string.split("\n\n") 
#print(sublist)
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
 json_file = open("badwords.json")
 data = json.load(json_file)
 json_file.close()
 return data["badwords"]

badids = []
badlanguage = loadBadWords()

#result = "#!/usr/bin/env bash\n\n"
command = "ffplay -vf subtitles="+movietitle+"-filtered.srt -i "+movietitle+".mp4 -af \"\n"
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
  p = re.search(r"\b" + re.escape(word) + r"\b", text) 
  if p:
    found.append(word)

         #result += "volume=enable='between(t," + str(start) + "," + str(end) + ")':volume=0, " + "\\\n"
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
for start, end in badids:
  command += "volume=enable='between(t," + str(start) + "," + str(end) + ")':volume=0, " + "\\\n"

command =  command[:-4] + "\""
#print(result)
f = open("languagefilter-streaming.sh", "w")
f.write(command)
f.close()


for word in badlanguage:
 if re.search(word, subtitle_string, re.IGNORECASE):
     r = re.compile(r"\b"+re.escape(word)+ r"\b", re.IGNORECASE)
     subtitle_string = r.sub(r'***', subtitle_string)

f = open(movietitle+"-filtered.srt", "w")
f.write(subtitle_string)
f.close()

subprocess.call(command, shell=True)
