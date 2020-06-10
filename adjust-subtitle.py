import subprocess
import re
import json
import string
import datetime
import time

windows_mainfolder = ""
movietitle = input("title: ")
try:
  f = open(movietitle+".srt", encoding="utf8")
except:
  subprocess.call("ffplay " + movietitle+".mp4", shell=True)  
movie_subtitle_file = movietitle + "-filtered.srt"
movie_assfile = movietitle + "-filtered.ass"

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
 json_file = open("badwords2.json")
 data = json.load(json_file)
 json_file.close()
 return data["badwords"]

badids = []
badlanguage = loadBadWords()

#result = "#!/usr/bin/env bash\n\n"
#fontSize = input("font size: ")
position_bible = input("bible verse position(6=top,2=bottom)")
repeat = input("repeat (0=forever): ")
adjust_time = int(input("adjust time: "))
position_movie = "6"
if position_bible=="6":
  position_movie = "2"
elif position_bible=="2":
  position_movie = "6"  
bible_style = ":force_style='Alignment="+position_bible+"'"
movie_style = ":force_style='Alignment="+position_movie+"'"

command = "ffplay -vf subtitles=bible-subtitles.ass"+bible_style + ",subtitles="+movie_assfile+movie_style + " -i "+movietitle+".mp4 -af \""
print("command : " + command)
numberofbadlanguage = 0
result = ""
for i in range(0, len(sublist)-1):
 #print(sublist[i]+"\n\n")
 id = i
 split = sublist[i].split("\n")
 
 timesub = split[1]
 timesplit  = timesub.split(" --> ")
 #print(timesplit)
 start = get_sec(timesplit[0])+ adjust_time
 end = get_sec(timesplit[1]) + adjust_time
 
 #print(word_list)
 #print(word)
 #print(split[2])
 text = split[2].lower()
 if len(split)>3:
    text+= " " + split[3].lower()
 print()
 print(id+1)
 result += str(id+1)
 result += "\n" 
 starttime = time.strftime('%H:%M:%S,000', time.gmtime(start))
 endtime = time.strftime('%H:%M:%S,000', time.gmtime(end))

 print(str(starttime) + " --> " + str(endtime))
 result += str(starttime) + " --> " + str(endtime)
 result += "\n"  
 print(text)
 result += text
 result += "\n\n" 
 text = ""

with open("rambo-adjusted.srt", "w") as outfile:
   outfile.write(result)
