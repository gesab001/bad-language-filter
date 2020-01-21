# bad-language-filter
This will mute the coarse language in movies. 

Tested in Windows 10 and Linux and MacOS.

Requirements:
- Install FFMPEG
- Install Python 3+
- an mp4 file
- an srt file (subtitles)

Instructions:
1. Download movie and subtitle for the movie. Make sure they are in sync. Simply play the movie with the subtitle to ensure they are synced.
2. Copy the badwords.json and the bad_language_filter_streaming.py into the movie folder.
3. Rename the movie filename to something simpler. Make sure the srt filename is the same as the movie filename.
4. Go to the movie folder.
3. execute the python file in the terminal:
   In windows command prompt, type py bad_language_filter_streaming.py
   In Linux/Mac terminal, type python3 bad_language_filter_streaming.py
   
