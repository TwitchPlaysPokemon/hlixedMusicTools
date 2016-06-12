import os
import sys

metadataFile = 'metadata_justNew.txt'
def printThenQuit(msg):
  print(msg)
  raw_input('\n\nPress enter to exit.')
  quit()

if sys.version_info[0] == 3:
  printThenQuit("""You are using Python 3 instead of Python 2.
This program only works in Python 2. You can download Python at http://python.org
""")

print("==1hlixed1's metadata adder v1.3==")

print("Opening "+metadataFile+"...")
f = None
try:
  f = open(metadataFile,'r')
except:
  printThenQuit("No file found named "+metadataFile+"! Put it in the same directory as this program.")
arr = f.readlines()
f.close()

if not os.path.exists("Other"):
  printThenQuit("No 'Other' folder found! Make a folder named \"Other\" in the same directory as this one. Then, put one folder for each game you want to add music from and put your BRSTMs in there.\n\n(So if I want to add music from Pokemon Red, I'd make a folder named 'Pokemon Red', put it inside the 'Other' folder, and then put any BRSTM files from that game in there).")

def prompt(x,emptyStrOK=False):
  response=""
  while(response==""):
    response = raw_input(x+":\n>").strip()
    if(emptyStrOK == True):
      break
  return response
def promptFromOptions(x,options):
  good=False
  while not good:
    theinput = prompt(x)
    if theinput in options:
      return theinput
    else:
      print("Invalid option.")

def contains(a,b):
  return a.lower().find(b.lower()) != -1

def addSong(foldername,filename=None):
  global arr
  foundGame=False
  if True: #I'm lazy and don't want to de-indent everything
    for i in range(len(arr)-2):
      if (not foundGame) & (arr[i].startswith( "    path: Other/"+foldername)) & (arr[i+1].startswith("    songs:")):
        foundGame=True
        i+=2
        if filename==None:
          filename = prompt("BRSTM filename")
        if not(contains(filename,".brstm")):
          filename += ".brstm"
          print("Filename: "+filename)
        if os.path.isfile("Other/"+foldername+"/"+filename):
          songid = filename.replace(".brstm","").replace(" ","_").replace("!","")
          print("ID: "+songid)
          songiddata   = "      - id: "+songid+"\n"
          title    = "        title: \""+prompt("Song title (leave blank to just use the file name)",True)+"\"\n"
          if title=="        title: \"\"\n":
            title="        title: "+filename.replace(".brstm","")+"\n"
            print("Title left blank; defaulting to: "+filename.replace(".brstm",""))
          filenamePath = "        path: "+filename+"\n"
          thetype  = "        type: "+promptFromOptions("Type (result, battle, warning, final_battle, leaderboard, betting)",["result", "battle", "warning", "final_battle", "leaderboard", "betting"])+"\n"
          newArr = [songiddata,title,filenamePath,thetype]
          good=True
          for data in newArr:
            if data == "":
              good=False
          if good:
            arr = arr[:i]+newArr+arr[i:]
            print("\nMetadata added! Make sure to save your changes by pressing enter at the 'enter a folder name' prompt, otherwise "+metadataFile+ " won't be changed.")
        else:
          print("No BRSTM file detected in Other/"+foldername+"/"+filename)
    if not foundGame:
      if(prompt("Metadata for this game not found. Want to add some?(y/n)").lower() == "y"):
        title=prompt("Game title")
        titledata    = "    title: "+title+"\n"
        gameid = "  - id: "+title.replace("!","").replace("&","").replace(":","").replace(" ","_")+"\n"
        print("ID: "+gameid)
        platform    = "    platform: "+prompt("Platform")+"\n"
        filenamePath    = "    path: Other/"+foldername+"\n"
        newArr = [gameid,titledata,platform,filenamePath,"    songs:\n"]
        good=True
        for data in newArr:
          if data == "":
            good=False
        if good:
          arr = arr[:len(arr)-1]+newArr+arr[len(arr)-1:]
          print("Added metadata for "+title+"!")
          addSong(foldername,filename) #Hopefully no recursion...

done = False
while not done:
  theInput = raw_input("Enter a folder name (Press enter to save and quit):")
  if(theInput == ""):
    done=True
  else:
    if os.path.exists("Other/"+theInput):
      if len(os.listdir("Other/"+theInput))>1 and (raw_input("Add metadata for all songs in the folder? (y/n)\n>").lower() == "y"):
          try:
            for file in os.listdir("Other/"+theInput):
              addSong(theInput,file)
            print("\nThat's all the BRSTM files in the "+theInput+" folder.\n")
          except KeyboardInterrupt:
            print("\nPress control+C again to quit, but your changes will be lost.")
      else:
        try:
          doneAddingSongs = False
          while not doneAddingSongs:
            addSong(theInput)
            continueText = raw_input("Enter another song? (y/n)\n>")
            if(continueText.lower() != "y"):
              doneAddingSongs=True
        except KeyboardInterrupt:
          print("\nPress control+C again to quit, but your changes will be lost.")
    else:
      print("This game doesn't have a folder yet! To add metadata for that game, make a folder inside the \"Other\" folder with same name as the game you're trying to add songs for, then put your BRSTMs inside that and try again.")
try:
  f = open(metadataFile,'w')
  f.writelines(arr)
  f.close()
except:
  printThenQuit("ERROR: Failed to save the changes!")

printThenQuit("Success! Metadata file updated!")
