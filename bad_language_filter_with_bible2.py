import subprocess
import re
import json
import string
import datetime

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


def getVerse(id):

	verse = bible[id-1]
	return verse

def getMinute(minutes):
   result = '{:02d}:{:02d}:00,000'.format(*divmod(minutes, 60 ))
   return result


movietitle = input("title: ")
try:
    f = open(movietitle + ".srt")
    subtitle_string = f.read()
    f.close()

    movie_subtitle_file = movietitle + "-filtered.srt"
    movie_assfile = movietitle + "-filtered.ass"

    json_data = {}
    sublist = subtitle_string.split("\n\n")

    badids = []
    badlanguage = loadBadWords()

    position_bible = input("bible verse position(6=top,2=bottom)")
    repeat = input("repeat (0=forever): ")
    position_movie = "6"
    if position_bible == "6":
        position_movie = "2"
    elif position_bible == "2":
        position_movie = "6"
    bible_style = ":force_style='Alignment=" + position_bible + "'"
    movie_style = ":force_style='Alignment=" + position_movie + "'"

    command = "#!/usr/bin/env bash\n\n"
    command += "ffmpeg -i " + movietitle + ".mp4 -vf subtitles=bible-subtitles.ass" + bible_style + ",subtitles=" + movie_assfile + movie_style + " -af \""
    numberofbadlanguage = 0
    for i in range(0, len(sublist) - 1):
        # print(sublist[i]+"\n\n")
        id = i
        split = sublist[i].split("\n")

        time = split[1]
        timesplit = time.split(" --> ")
        # print(timesplit)
        start = get_sec(timesplit[0]) - 1
        end = get_sec(timesplit[1]) + 2

        # print(word_list)
        # print(word)
        # print(split[2])
        time = [start, end]
        text = split[2].lower()
        if len(split) > 3:
            text += " " + split[3].lower()
        found = []
        for word in badlanguage:
            unmasked = unmaskBadWord(word)
            p = re.search(r"\b" + re.escape(unmasked) + r"\b", text)
            if p:
                found.append(word)
            x = re.findall(r'\b' + unmasked + '\w+', text)
            if x:
                found.append(word)

                # command += "volume=enable='between(t," + str(start) + "," + str(end) + ")':volume=0, " + "\\\n"
            # numberofbadlanguage+=1
            # print(str(id) + sublist[i])
            # badids.append(time)

        if len(found) != 0:
            # print(found)
            # print(str(id) + split[3].lower())
            badids.append(time)
            # numberofbadlanguage+=1

        json_data[id] = {}
        json_data[id]["start"] = int(start)
        json_data[id]["end"] = int(end)
        json_data[id]["text"] = text
        text = ""
    # print(json_data)

    # print(badids)
    # print("total:" + str(numberofbadlanguage))
    for start, end in badids:
        command += "volume=enable='between(t," + str(start) + "," + str(end) + ")':volume=0, "

    filtered_movie_title = movietitle + "-filtered.mp4"
    command = command[:-2] + "\" " + filtered_movie_title
    # print(command)

    for word in badlanguage:
        unmasked = unmaskBadWord(word)
        if re.search(unmasked, subtitle_string, re.IGNORECASE):
            r = re.compile(r"\b" + re.escape(unmasked) + r"\b",
                           re.IGNORECASE)  # searches for any word that matches this word
            subtitle_string = r.sub(r'***', subtitle_string)
            r = re.compile(r'\b' + unmasked + '\w+',
                           re.IGNORECASE)  # searches for any string that starts with this word
            subtitle_string = r.sub(r'***', subtitle_string)

            # subprocess.call("bible", shell=True)
    f = open(movie_subtitle_file, "w", encoding="utf8")
    f.write(subtitle_string)
    print(subtitle_string)
    f.close()
    convert_movie_assfile = "ffmpeg -i " + movie_subtitle_file + " " + movie_assfile
    print("convert_movie_assfile: " + convert_movie_assfile)
    subprocess.call(convert_movie_assfile, shell=True)

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

    bible = []
    choice = input("topic or book: ")

    if choice == "book":
        books = getBooks()
        topic = input("book name: ")
        for book in books:
            if topic.lower() == book.lower():
                bookName = book
                bible = getBookVerses(bookName)
    else:
        topic = input("topic: ")
        bible = getBibleTopic(topic)

    totalVerses = len(bible)

    currentID = getCurrentID()
    subtitles = ""
    for i in range(1, length, 1):
        id = str(i)
        start = getMinute(i - 1)
        end = getMinute(i)
        verse = getVerse(currentID)
        words = verse["word"] + " " + verse["book"] + " " + str(verse["chapter"]) + ":" + str(verse["verse"])
        toString = id + "\n" + start + " " + to + " " + end + "\n" + words + "\n\n"
        print(toString)
        currentID = currentID + 1
        if currentID > totalVerses:
            currentID = 1
        subtitles = subtitles + toString

    outfile = open("bible-subtitles.srt", "w")
    outfile.write(subtitles)
    outfile.close()
    assfile = "bible-subtitles.ass"
    convertoass = "ffmpeg -i bible-subtitles.srt " + assfile
    subprocess.call(convertoass, shell=True)

    subprocess.call(command, shell=True)
    shutdown = "shutdown -h now"

    subprocess.call(shutdown, shell=True)
except:

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
    bible = []

    position_bible = input("bible verse position(6=top,2=bottom)")
    repeat = input("repeat (0=forever): ")
    position_movie = "6"
    if position_bible == "6":
        position_movie = "2"
    elif position_bible == "2":
        position_movie = "6"
    bible_style = ":force_style='Alignment=" + position_bible + "'"
    movie_style = ":force_style='Alignment=" + position_movie + "'"
    filtered_movie_title = movietitle + "-filtered.mp4"

    command = "#!/usr/bin/env bash\n\n"
    command += "ffmpeg -y -i " + movietitle + ".mp4 -vf subtitles=bible-subtitles.ass" + bible_style + " " + filtered_movie_title

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
    # shutdown = "shutdown -h now"
    #
    # subprocess.call(shutdown, shell=True)

