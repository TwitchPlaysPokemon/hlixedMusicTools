import sys
if sys.version_info[0] == 2:
    print("""You are using Python 2 instead of Python 3.
This program only works in Python 3 because 1hlixed hasn't gotten around to porting it to python 2.7. I recommend pestering 1hlixed repeatedly.
""")
    raw_input('\n\nPress enter to exit.') #use raw_input because if we're here, we're in python 2!
    exit()


print("1hlixed's automatic BRSTM downloader v1.1")
#Todo: make 2.7 version
import urllib.request
import re
import os

suggestionfilename = "suggestions.txt"

print("To use this, copypaste everyone's submissions into a giant file named "+suggestionfilename+", making sure to give each brawlcustommusic URL a new line. This will auto-download the BRSTM and fill in the name from the BRSTM's page. Then, it will be placed in downloaded.txt, so you can use it with listenToSongs.py.")
input("\nPress enter to begin")

print("Reading submissions from "+suggestionfilename)
arr = []
try:
	f = open(suggestionfilename)
	arr = f.readlines()
	f.close()
except:
	print("Hey; that doesn't exist! To use this program, make a file named "+suggestionfilename+" and format each line with people's submissions. People should have submitted them as \"brawlcustommusic.com/<blah> (<type>)\"; place a \"[ ]\" before each line. When a BRSTM is downloaded, the \"[ ]\" will be filled with \"[d]\" to tell you that song is [D]ownloaded.\nOne way to do this is to find-replace \"\\nhttp://\" to \"\\n[ ]http://\"")
	input("\n\nPress enter to exit.")
	exit()

arr2 = []
try:
	f2 = open('downloaded.txt')
	arr2 = f2.readlines()
	f2.close()
except:
	print("Creating downloaded.txt! This will contain some data about each track; run downloadedToMetadata.py to convert this into metadata formatted for TPP.")

smashcustommusicre = re.compile('http://(www.)*smashcustommusic.(com|net)/\d+')

gameregex = re.compile('(?<=<span id="game"><a href="/game/).*?(?=</a><br>)')
#<td><span id="name">Fighting of the Spirit (Arrange Version)</span>

nameregex = re.compile('(?<=(<span id="name">)).*?(?=</span>)')

typeregex = re.compile('\((battle|betting|warning|victory|30 seconds|results|result|break)\)',re.I)

def updatefile():
	f = open(suggestionfilename,'w')
	f.writelines(arr)
	f.close()

	f2 = open('downloaded.txt','w')
	f2.writelines(arr2)
	f2.close()
	print("downloaded.txt updated!")


print("All done; time to download some BRSTMs!")
try:
	counter=0
	for i in range(len(arr)):
		arr[i] = arr[i].replace("brawlcustommusic","smashcustommusic") #you never know
		if (arr[i][0:3] == "[ ]") and (re.search(smashcustommusicre,arr[i])):
			url = re.search(smashcustommusicre,arr[i]).group()
			
			number = url.split("/")[-1]
			response = urllib.request.urlopen(url)
			html = str(response.read())
			try:
				game = re.search(gameregex, html).group().split(">")[1]
				songname = re.search(nameregex, html).group().replace("\\'","\'")
			except:
				print("Error! No game found!")
				arr[i] = arr[i].replace("[ ]","[e]")
				continue

			print("Downloading "+songname +" from "+game+"...")
			if not os.path.exists("Other/"+game):
			    os.makedirs("Other/"+game)
			urllib.request.urlretrieve ("http://www.brawlcustommusic.com/brstm/"+number, "Other/"+game+"/"+songname.replace("/","")+".brstm")
			print("downloaded "+"Other/"+game+"/"+songname.replace("/","")+".brstm")
			songtype = re.search(typeregex,arr[i])
			if songtype:
				if (songtype == "results") or (songtype == "victory"):
					songtype = "result"
				if songtype == "30 seconds":
					songtype = "warning"
				arr2.append(game+"|||"+songname+"|||"+songname+".brstm|||"+songtype.group()[1:-1].lower()+"\n")
				print("Type: "+songtype.group()[1:-1])
			else:
				arr2.append(game+"|||"+songname+"|||"+songname+".brstm|||1hlixed_forgot_to_fill_in\n")
				print("No type detected; manual fill in required. Listen to the BRSTM and delete the line if it doesn't fit, or enter a type if it does.")
			arr[i] = arr[i].replace("[ ]","[d]")
			counter+=1
			if(counter%10==0):
				counter=0
				updatefile()
	print("Done! You might want to run removeDuplicatesListening.py to remove any duplicate songs, though.")
finally:
	print("Quitting...")
	updatefile()
