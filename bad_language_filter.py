import json

json_file = open("badwords.json")
data = json.load(json_file)
json_file.close()

while True:
  word = input("word: " )

  if word=="exit":
     break
  else:
    data["badwords"].append(word)
    print(data)
    outfile = open("badwords.json", "w")
    json.dump(data, outfile)
    outfile.close()

