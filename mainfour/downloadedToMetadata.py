import sys
if sys.version_info[0] == 2:
		print("""You are using Python 2 instead of Python 3.
This program only works in Python 3 because 1hlixed hasn't gotten around to porting it to python 2.7. I recommend pestering 1hlixed repeatedly.
""")
		raw_input('\n\nPress enter to exit.') #use raw_input because if we're here, we're in python 2!
		exit()


dlfilename = 'listeningdownloaded.txt'
metafilename = 'metadata_justNew.txt'

print("1hlixed's metadata generator v1.3")
print("\nthis program is intended to work with download.py and listenToSongs.py. For each song in "+dlfilename+" that starts with '[#]' (marking an accepted song), this will create metadata in "+metafilename+". Afterwards, the '[#]' will be changed to '[m]', M for 'Metadata Exists'. Make sure that the Other folder is in the same directory as this program!")
input("\nPress enter to begin.")
import re
import os
f = open(dlfilename)
arr = f.readlines()
f.close()

arr2 = []
try:
	f2 = open(metafilename)
	arr2 = f2.readlines()
	f2.close()
except:
	print("Created "+metafilename+"; this is where the generated metadata will go.")

duplicatedGamefile = 'alreadyexistinggames.txt'

dupGameArr = []
try:
	f2 = open(duplicatedGamefile)
	dupGameArr = f2.readlines()
	f2.close()
except:
	print("Created "+duplicatedGamefile+"; this will contain a list of all games that need to be merged.")




streamGameinfo = {}

streammetafile = input("Oh; and do you have a stream metadata file? I can use that to make merging easier. If so, enter the filename (or enter to leave blank)\n>")

dataDict = {"id":"  - id: ","year":"    year: ","platform":"    platform: ","path":"    path: ","title":"    title: "}

def loadFromStreamMetafile():
	global streamGameinfo
	if streammetafile != "":
		streamdata = []
		try:
			f3 = open(streammetafile)
			streamdata = f3.readlines()
			f3.close()
		except:
			print("Couldn't find "+streammetafile+". Are you sure you typed it corectly?")
			return
		currSongData = {}
		for i in streamdata:
			if "    songs: " in i:
				currTitle = currSongData["title"]
				streamGameinfo[currTitle.replace('"',"")] = currSongData #remove "" from outside
				currSongData = {}
			else:
				for thing in dataDict:
					if dataDict[thing] in i:
						currSongData[thing] = i.replace(dataDict[thing],"").replace("\n","")
	
loadFromStreamMetafile()

gameList = []
def findgameindex(gamepath):
	if "/" not in gamepath:
		gamepath = "\"Other/"+gamepath.replace('\"','')+'\"'
	if '"' not in gamepath:
		gamepath = '"' + gamepath + '"'

	for i in range(len(arr2)-2):
		if (arr2[i].startswith("    path: ")) & (arr2[i+1].startswith("    songs:")):
			if (gamepath.strip() == arr2[i].split("    path: ")[1].strip()):
				return i+2
	print("Unable to find index of "+gamepath)
	print(1/0)
#populate gameList
for i in range(len(arr2)-2):
	if (arr2[i].startswith( "    path: ")) & (arr2[i+1].startswith("    songs:")):
		game = arr2[i].split("    path: ")[1].strip()
		gameList.append(game)

def updatefile():
	f = open(dlfilename,'w')
	f.writelines(arr)
	f.close()

	f2 = open(metafilename,'w')
	f2.writelines(arr2)
	f2.close()

	f3 = open(duplicatedGamefile,'w')
	f3.writelines(dupGameArr)
	f3.close()
	print("Metadata files updated!")

displaySongs = not (input("Display names of songs as they're added? (y/n):\n>").strip().lower().startswith("n"))

movedGames = {}

#actually do stuff
insertionIndex =len(arr2) #the line # where the new text will be inserted
try:
	counter=0
	for i in range(len(arr)):
		data = "]".join(arr[i].split("]")[1:]).split("|||")
		checkbox = arr[i].split("]")[0]+"]"
		try:
			gamepath = data[0].strip()
			gamename = gamepath
			songtitle=data[1].strip()
			filename = data[2].strip()
			songtype=data[3]
		except:
			print("Error getting data from line " + str(i))
			print(data)
			updatefile()
			exit()
		
		if checkbox == '[#]':
			#first, make sure the game's folder doesn't contain a ":" or a "'"
			inmoved=False
			if(gamepath in movedGames):	
				print("Found this game in movedGames!")
				gamename = movedGames[gamepath][1].replace('"',"")
				gamepath = movedGames[gamepath][0]
				inmoved = True

			elif (gamepath.replace(":","_") != gamepath): 
				print("Folder name contains :, renaming...")
				if not os.path.isdir("Other/"+gamepath.replace(":","_")):
					if os.path.isdir("Other/"+gamepath): #if we can rename
						os.rename("Other/"+gamepath,"Other/"+gamepath.replace(":","_"))
						print("Renaming "+gamepath+" folder to "+gamepath.replace(":","_"))
						gamepath = gamepath.replace(":","_")
					else:
						input("Other/"+gamepath+" folder not found! Press enter after you resolve the issue.")
				else:
					print("Oh; it's already renamed. Convenient!")
					gamepath = gamepath.replace(":","_")

			#first, add the game's info
			if ('"Other/'+gamepath+'"' in gameList) or inmoved:
				insertionIndex = findgameindex(gamepath)
			else:	
				gamename = input("What is the title of the game in the "+gamepath+" folder? (enter to keep as identical, f to attempt an automatic fix)\n>")
				if(gamename == ""):
					gamename = gamepath
				if(gamename.lower() == 'f'):
					gamename = gamepath.replace("s ","\'s ").replace("_",":").replace("Pokemon","Pokémon")
					t2 = input("Is "+gamename+" the right name? If so, press enter, if not, enter correct name:\n>")
					if t2 != '':
						gamename = t2

				newArr = []

				if (gamename in streamGameinfo) or (gamename.replace("Pokemon","Pokémon") in streamGameinfo):
					print("Found that title in the stream metadata folder!")
					dupGameArr.append(gamename+"\n")
					gameinfo = ""
					if gamename in streamGameinfo:
						gameinfo = streamGameinfo[gamename]
					else:
						gameinfo = streamGameinfo[gamename.replace("Pokemon","Pokémon")]
					for datapart in ['id','title','platform','year','path']:
						newArr.append(dataDict[datapart] + gameinfo[datapart]+'\n')
					if gameinfo['path'] != 'Other/'+gamename:
						shouldmove = input("The game folder isn't in the right place for a merge! Want me to move it to the "+gameinfo['path']+" folder for you to make merging possible? (y/n)\n>")
						if shouldmove.startswith('y'):
							if not os.path.isdir(gameinfo['path'].replace('"','')):
								try:
									os.makedirs(gameinfo['path'].replace('"',''))
								except FileExistsError:
									pass
								if os.path.exists("Other/"+gamepath):
									os.rename("Other/"+gamepath,gameinfo['path'].replace('"',''))
									print("Done!")
								elif os.path.exists("Other/"+gamepath.replace("_",":")): #Worth a shot
									os.rename("Other/"+gamepath.replace("_",":"),gameinfo['path'].replace('"',''))
									print("Done!")
								else:
									input("Wait; the Other/"+gamepath +"folder doesn't exist! Is it misnamed? Rename it to '"+gamepath+"' and press enter.")
									os.rename("Other/"+gamepath,gameinfo['path'].replace('"',''))
									print("Done!")
							else:
								print("Oh; it was already renamed. Convenient!")
							movedGames[gamepath] = [gameinfo['path'].replace('"',""),gameinfo['title']] #let the song part of the program know the BRSTM still exists
							gamepath = gameinfo['path'].replace('"',"")
							print(gamepath)
							gamename = gameinfo['title'].replace('"',"")
					newArr.append("    songs:\n")
				else:
					titledata    = "    title: \""+gamename+"\"\n"
					gameid = "  - id: "+gamename.replace("!","").replace("&","").replace(":","_").replace(" ","_").lower()+"\n"
					platform    = "    platform: \""+input("Enter platform for " +gamename+"\n>")+"\"\n"
					year    = "    year: "+input("Enter year for " +gamename+"\n>")+"\n"
					filenamePath    = "    path: \"Other/"+gamepath+"\"\n"
					newArr = [gameid,titledata,year,platform,filenamePath,"    songs:\n"]


				good=True
				for data in newArr:
					if data == "":
						good=False
				
				if "/" not in gamepath:
					gamepath = "Other/" + gamepath

				if '"'+gamepath.replace('"','')+'"' not in gameList:
					if good:
						lastIndex = len(arr2)
						if arr2[lastIndex-1].strip() == "...":
							lastIndex -= 1
						arr2 = arr2[:lastIndex]+newArr+arr2[lastIndex:]
						if displaySongs:
							print("Added game info for "+gamename)
						insertionIndex = lastIndex + len(newArr)
						#add new game to gameList
						gameList.append('"'+gamepath.replace('"','')+'"')
					else:
						print("Some of that data wasn't good!")
				else:
					print("Game already in; using that")
					insertionIndex = findgameindex(gamepath)
					
			#gamename = data[0]
			#songtitle=data[1]
			#filename = data[2]
			#songtype=data[3]

			if "/" not in gamepath:
				gamepath = "Other/" + gamepath

			fileExists = os.path.isfile(gamepath+"/"+filename)
			if (not fileExists) and (gamepath in movedGames): #check if the game was just moved
				if os.path.isfile(gamepath.replace('"',"")+"/"+filename): #no Other/ here
					fileExists = True
			if fileExists:
				songid = filename.replace(".brstm","").replace(" ","_").replace("!","").lower()
				songiddata   = "      - id: "+songid+"\n"
				filenamePath = "        path: \""+filename+"\"\n"
				thetype  = "        type: "+songtype #There's a \n at the end here; no need to add one!
				title = "        title: \""+songtitle+"\"\n"
				newArr = [songiddata,title,filenamePath,thetype]
				arr2 = arr2[:insertionIndex]+newArr+arr2[insertionIndex:]
				insertionIndex += len(newArr)
				if displaySongs:
					print("Added metadata for "+songtitle + "\n\t(game: "+gamename+")")
				checkbox = '[m]'
				arr[i] = arr[i].replace("[#]","[m]")
			else:
				print("WARNING! No BRSTM for "+gamepath+"/"+filename+"!")
			
			counter+=1
			if(counter%10==0):
				counter=0
				updatefile()
finally:
	print("Quitting...")
	updatefile()
