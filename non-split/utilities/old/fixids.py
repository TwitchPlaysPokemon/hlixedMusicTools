import string

print("1hlixed's song ID fixer v1.3")

name = raw_input("Metadata file name>")
f = open(name)
arr = f.readlines()
f.close()
def updateFile():
  f = open(name+".fixed","w")
  f.writelines(arr)
  f.close()

  print("\n\nA music file with fixed song IDs has been saved to "+name+".fixed so check that out!")
  raw_input("\n\nPress enter to exit.")


for i in range(len(arr)):
  line = arr[i]
  if line.startswith("      - id: ") or line.startswith("  - id: "): #game ID, song ID
    prefix = ""
    if line.startswith("      - id: "):
      prefix = "      - id: "
    if line.startswith("  - id: "):
      prefix = "  - id: "
    currSongTitle = line.replace("      - id: ","").replace("  - id: ","").strip().lower()
    #song IDs can't have anything other than _ or - in them
    badchars = []
    for j in currSongTitle:
      if j not in ("_-0123456789"+ (string.ascii_lowercase)):
        badchars.append(j)
    if len(badchars) > 0:
      print(currSongTitle + " has the following invalid characters: " + str(badchars))
      for j in badchars:
        currSongTitle = currSongTitle.replace(str(j),"")
        pass
    arr[i] = prefix + currSongTitle + "\n"

updateFile()
