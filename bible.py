import datetime
import json
import subprocess

length = 180
id = "1"
start = "00:00:00,000" 
to = "-->"
end = " 00:01:00,000"
words = "Is that you on the beach?"
toString = id + "\n" + start + "\n" + to + "\n" + end + "\n" + words + "\n\n"

def getCurrentID():
   first_time = datetime.datetime(2018,6,23)
   later_time = datetime.datetime.now()    
   duration = later_time - first_time
   duration_in_s = duration.total_seconds() 
   minutes = divmod(duration_in_s, 60)[0]  
   currentID = minutes
   while currentID>31102:
      currentID = currentID - 31102
   return int(currentID)
   
file = open("bible.json", "r")
json_data = json.load(file)
bible = json_data["bible"]

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
	subtitles = subtitles + toString

outfile = open("bible-subtitles.srt", "w")
outfile.write(subtitles)
outfile.close()

title = input("title: " )
command = "ffplay -vf subtitles=bible-subtitles.srt:force_style='Alignment=6' -i " + title + ".mp4"
subprocess.call(command, shell=True)
