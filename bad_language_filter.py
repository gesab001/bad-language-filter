import subprocess

f = open("input.srt") 
text = f.read() 
f.close()
json_data = {} 
sublist = text.split("\n\n") 

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

badids = []
badlanguage = ["god", "dick", "penis", "cunt", "jesus", "christ", "shit", "lord", "fuck", "ass", "bitch"]
result = "#!/usr/bin/env bash\n\n"
result += "ffmpeg -i input.mp4 -af \"\n"
numberofbadlanguage = 0
for i in range(0, len(sublist)-1):
 #print(sublist[i]+"\n\n")
 id = i
 split = sublist[i].split("\n")
 
 time = split[1]
 timesplit  = time.split(" --> ")
 #print(timesplit)
 start = get_sec(timesplit[0])-2 
 end = get_sec(timesplit[1])+2
 
 #print(word_list)
 #print(word)
 #print(split[2])
 time = [start, end]
 if any(word in split[2].lower() for word in badlanguage):
         #result += "volume=enable='between(t," + str(start) + "," + str(end) + ")':volume=0, " + "\\\n"
      numberofbadlanguage+=1
         #print(str(id) + split[2].lower())
      badids.append(time)
 if len(split)>3:
   if any(word in split[3].lower() for word in badlanguage):
     
      badids.append(time)
      numberofbadlanguage+=1

 json_data[id] = {}
 json_data[id]["start"] = int(start)
 json_data[id]["end"] = int(end)
 json_data[id]["text"] = text
 text = ""
#print(json_data) 

#print(badids)
#print("total:" + str(numberofbadlanguage))
for start, end in badids:
  result += "volume=enable='between(t," + str(start) + "," + str(end) + ")':volume=0, " + "\\\n"

result =  result[:-4] + "\" output.mp4"
#print(result)
f = open("languagefilter2.sh", "w")
f.write(result)
f.close()

subprocess.call("./languagefilter2.sh")
