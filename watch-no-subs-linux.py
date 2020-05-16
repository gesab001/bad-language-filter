import subprocess
import re
import json
import string
import datetime

windows_mainfolder = ""
movietitle = input("title: ")

#print(sublist)


#result = "#!/usr/bin/env bash\n\n"
#fontSize = input("font size: ")
position_bible = input("bible verse position(6=top,2=bottom)")
repeat = input("repeat (0=forever): ")
position_movie = "6"
if position_bible=="6":
  position_movie = "2"
elif position_bible=="2":
  position_movie = "6"  
bible_style = ":force_style='Alignment="+position_bible+"'"
movie_style = ":force_style='Alignment="+position_movie+"'"

command = "ffplay -vf subtitles=bible-subtitles.ass"+bible_style + " -i "+movietitle+".mp4 "
print("command : " + command)

length = 240
id = "1"
start = "00:00:00,000" 
to = "-->"
end = " 00:01:00,000"
words = "Is that you on the beach?"
toString = id + "\n" + start + "\n" + to + "\n" + end + "\n" + words + "\n\n"

totalVerses = 31102
file = open("bible.json", "r")
json_data = json.load(file)

def getCurrentID():
   first_time = datetime.datetime(2018,6,23)
   later_time = datetime.datetime.now()    
   duration = later_time - first_time
   duration_in_s = duration.total_seconds() 
   minutes = divmod(duration_in_s, 60)[0]  
   currentID = minutes
   while currentID>totalVerses:
      currentID = currentID - totalVerses
   return int(currentID)

def getBooks():
  verses = json_data["bible"]
  books = []
  for verse in verses:
   book = verse["book"]
   if book not in books:
      books.append(book)
  return books
  
def getBibleTopic(topic):
  verses = []  
  if topic=="all":
    verses = json_data["bible"]
  else:
    bible = json_data["bible"]
    for item in bible:
        verse = item["word"]
        if topic.lower() in verse.lower():
           verses.append(item)
           print(verse)		   
  return verses
 
 
def getBookVerses(bookTitle):
    verses = []
    bible = json_data["bible"]
    for item in bible:
        verse = item["book"]
        if bookTitle.lower() in verse.lower():
           verses.append(item)
           print(verse)		   
    return verses
bible = []
choice = input("topic or book: ")

if choice=="book":
 books = getBooks()
 topic = input("book name: " )
 for book in books:
  if topic.lower() == book.lower():
   bookName = book
   bible = getBookVerses(bookName)
else:  
 topic = input("topic: " )
 bible = getBibleTopic(topic)  

totalVerses = len(bible)
  
def getVerse(id):

	verse = bible[id-1]
	return verse
   
def getMinute(minutes):
   result = '{:02d}:{:02d}:00,000'.format(*divmod(minutes, 60 ))
   return result
 
currentID =  getCurrentID() 
subtitles = ""
for i in range(1, length, 1):
	id = str(i)
	start = getMinute(i-1)
	end = getMinute(i)
	verse = getVerse(currentID)	
	words = verse["word"] + " " + verse["book"] + " " + str(verse["chapter"]) + ":" + str(verse["verse"])
	toString = id + "\n" + start + " " + to + " " + end + "\n" + words + "\n\n"
	print(toString)
	currentID = currentID + 1
	if currentID>totalVerses:
	  currentID = 1
	subtitles = subtitles + toString

outfile = open("bible-subtitles.srt", "w")
outfile.write(subtitles)
outfile.close()
assfile = "bible-subtitles.ass"
convertoass =  "ffmpeg -i bible-subtitles.srt " + assfile
subprocess.call(convertoass, shell=True)

subprocess.call(command, shell=True)
