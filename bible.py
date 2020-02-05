import datetime
import json
import subprocess

length = 240
id = "1"
start = "00:00:00,000" 
to = "-->"
end = " 00:01:00,000"
words = "Is that you on the beach?"
toString = id + "\n" + start + "\n" + to + "\n" + end + "\n" + words + "\n\n"

totalVerses = 31102
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


def getBibleTopic(topic):
  verses = []
  file = open("bible.json", "r")
  json_data = json.load(file)
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
	words = verse["word"]
	toString = id + "\n" + start + " " + to + " " + end + "\n" + words + "\n\n"
	print(toString)
	currentID = currentID + 1
	if currentID>totalVerses:
	  currentID = 1
	subtitles = subtitles + toString

outfile = open("bible-subtitles.srt", "w")
outfile.write(subtitles)
outfile.close()
title = input("title: " )
assfile = "bible-subtitles.ass"
convertoass =  "ffmpeg -i bible-subtitles.srt " + assfile
subprocess.call(convertoass, shell=True)

moviefilename = title + ".mp4"
style = ":force_style='Alignment=6,ScaleX=1%,ScaleY=1%,MarginL=5,MarginR=5'"
command = "ffplay -vf subtitles="+assfile + style+" -i " + moviefilename;
subprocess.call(command, shell=True)
