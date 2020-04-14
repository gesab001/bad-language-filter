#!/usr/bin/env python
import subprocess
from subprocess import call
import cgitb
import cgi
import json
import string
import re
#import mysql.connector as conn
cgitb.enable()    


# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields
#first_name = form.getvalue('first_name')
#last_name  = form.getvalue('last_name')
#movietitle = form.getvalue('movie_title')
#position_bible = form.getvalue('position_bible')
#repeat = form.getvalue('repeat')
movietitle = "batman"
position_bible = 2
repeat = 1

#print("Content-Type: text/html;charset=utf-8")
#print "Content-type:text/html\r\n\r\n"
print (movietitle)
print (position_bible)
print (repeat)

movie_subtitle_file = movietitle + "-filtered.srt"
movie_assfile = movietitle + "-filtered.ass"

f = open("../html/videos/"  + movietitle+".srt")  

subtitle_string = f.read() 
f.close()
#print (subtitle_string)

json_data = {} 
sublist = subtitle_string.split("\n\n") 
print(sublist)



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
#print(badlanguage)

for i in range(0, len(sublist)-1):
 print(sublist[i]+"\n\n")
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
 #print(text)
 for word in badlanguage:
  unmasked = unmaskBadWord(word)
  p = re.search(r"\b" + re.escape(unmasked) + r"\b", text) 

  x = re.findall(r'\b'+unmasked+'\w+', text)
  if p:
    found.append(word)
  if x:
    found.append(word)
    #print(text)
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
print(json_data) 


f = open("../html/videos/"+movie_subtitle_file, "w", encoding="utf8")
f.write(subtitle_string)
#print(subtitle_string)
f.close()
convert_movie_assfile =  "ffmpeg -i " + "../html/videos/"+movie_subtitle_file + " "  + "../html/videos/"+movie_assfile
#print("convert_movie_assfile: " + convert_movie_assfile)
subprocess.call(convert_movie_assfile, shell=True)

