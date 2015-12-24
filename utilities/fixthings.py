import getch

print("1hlixed's metadata file fixer v1.8")
import re
import os

import sys
if sys.version_info[0] == 2:
		print("""You are using Python 2 instead of Python 3.
This program only works in Python 3 because as of PBR2.0 we're moving to python 3!
""")
		raw_input('\n\nPress enter to exit.') #use raw_input because if we're here, we're in python 2!
		exit()


print("This program will autofix things wrong with a metadata file, but will always ask for permission first.\n")
filename = input("Enter the filename of the metadata file to analyze (put it in the same directory as this script):\n>")
f = open(filename,"r")
arr = f.readlines()
f.close()

print("Successfully read the file!")

for i in range(len(arr)):
	if(arr[i][-1] != "\n"):
		arr[i] += "\n"


arr2 = []

def updatefile():
	f2 = open(filename,'w')
	f2.writelines(arr)
	f2.close()
	print("Metadata files updated!")

def cgetch():
	key = getch.getch() #this blocks
	if key == '\x03': #control+c
		print("Quitting...")
		exit()
	return key


cache = {}
def generate_suffix(gameid):
	toReturn = ""
	if gameid in cache:
		return cache[gameid]

	arr = gameid.split("_") 
	if arr[0] == 'pokemon': #for pokemon_omega_ruby return omega_ruby
		toReturn = '_'.join(arr[1:])
	if arr[0] == 'touhou':
		#return the initials of the game: 
		#touhou_suimusou_immaterial_and_missing_power -> iamp
		string = ''
		for word in arr[2:]:
			string += word[0]
		toReturn = string
	twowordshortenings = {'final_fantasy':'ff','mario_kart':'mk','sonic_adventure':'sa'}
	if len(arr) >= 3:
		firsttwo = arr[0]+'_'+arr[1]
		for shortening in twowordshortenings:
			if firsttwo in twowordshortenings:
				return twowordshortenings[firsttwo]+'_'.join(arr[2:])
	if toReturn == "":
		toReturn = input("Enter the suffix for the game with id "+gameid+"\n>")
	cache[gameid] = toReturn
	return toReturn


idArr = []
gameArr = []

selfDuplicating = []

#First, do a pass correcting spaces
i=0
while i < (len(arr)):
	if "  - id: " in arr[i]:
		isGame=True
		for j in range(4):
			if not (arr[i+j+1].startswith("    platform: ") or arr[i+j+1].startswith("    year: ") or arr[i+j+1].startswith("    path: ") or arr[i+j+1].startswith("    title: ")):
				isGame=False
		if (not isGame) and (arr[i].startswith("  - id: ")):
			print(arr[i]+"is a game when it should be a song!")
			arr[i] = arr[i].replace("  - id: ","      - id: ")
		elif (isGame) and (arr[i].startswith("      - id: ")):
			print(arr[i]+"is a song when it should be a game!")
			arr[i] = arr[i].replace("      - id: ","  - id: ")
	#surround titles and paths in quotes
	if "title:" in arr[i]:
		if '"' not in arr[i]:
			beginningSpaces = arr[i].split("title:")[0]
			try:
				title = arr[i].split("title:")[1].strip()
				arr[i] = beginningSpaces + "title: " + '"' + title + '"\n'
				print("Put spaces around "+title)
			except IndexError:
				print("Error putting quotes around line "+str(i)+"! skipping...")

	if "path:" in arr[i]:
		if '"' not in arr[i]:
			beginningSpaces = arr[i].split("path:")[0]
			try:
				path = arr[i].split("path:")[1].strip()
				arr[i] = beginningSpaces + "path: " + '"' + path + '"\n'
				print("Put spaces around "+path)
			except IndexError:
				print("Error putting quotes around line "+str(i)+"! skipping...")
	i += 1


i=0
try:
	while i < (len(arr)):
		if arr[i].startswith("      - id: "):#new song
			songid = arr[i].replace("      - id: ","").replace("\n","").strip()
			if songid[0] == '"':
				songid = songid[1:-1]
			if songid not in idArr:
				idArr.append(songid)
				gameArr.append(game)
			else:
				if game == gameArr[idArr.index(songid)]:
					#(songid+" (from "+game+") shares an ID with another game with the same id!")
					if game not in selfDuplicating:	
						selfDuplicating.append(game)
				#else:
					#(songid+" (from "+game+") shares an ID with "+songid+" from "+gameArr[idArr.index(songid)]+"!")
		elif arr[i].startswith("  - id: "): #new game
			songid = ""
			game = arr[i].replace("  - id: ","").replace("\n","")
			if game[0] == '"':
				game = game[1:-1]
		i += 1
finally:
	pass


i=0


#now that we have the DB, fix errors
try:
	while i < (len(arr)):
		if arr[i].startswith("      - id: "):#new song
			songid = arr[i].replace("  - id: ","").replace("\n","").strip()
			if songid[0] == '"':
				songid = songid[1:-1]
			if songid.lower() != songid:	
				print(game+": "+songid + " is not a lowercase song ID! Press f to fix.")
				key = cgetch()
				if key == 'f':
					arr[i] = arr[i].lower()
				print("Renamed to "+songid.lower()+".")
			if len(songid.strip()) > 50:
				newid = input(game+": "+songid + " is over 50 characters! Enter new id or press enter to do nothing\n>")
				if newid.strip() != '':
					arr[i] = "      - id: "+newid.replace("\n","").strip()+"\n"
					print("Changed to "+newid+".")
			if songid in idArr:
				if game == gameArr[idArr.index(songid)]:
					#print(songid+" (from "+game+") shares an ID with another game with the same id! I can't do anything about chat; check it out manually.")
					pass
				else:
					print(songid+" (from "+game+") shares an ID with "+songid+" from "+gameArr[idArr.index(songid)]+"!\nfix by adding suffix? (f=fix)")
					key = cgetch()
					if key == 'f':
						newsongid = songid + "_"+generate_suffix(game)
						if(len(newsongid) > 50):
							print("The new song ID is over 50 characters! Aborting...")
						else:
							print("is "+newsongid+"OK? y=ok, c=enter custom suffix, anything else = abort")
							key = cgetch() 
							if key == 'c':
								newsongid = input("Enter new suffix:\n>").strip()
								if newsongid != "":
									arr[i] = "      - id: "+newsongid+"\n"
									print("Done")
							if key == 'y':
								arr[i] = "      - id: "+newsongid+"\n"
								print("Done")
							else:
								print("OK; skipping this for now. Run me again if you want to fix this.")
		elif arr[i].startswith("        type: "):
			songtype = arr[i].replace("        type: ","")
			if (songtype != '') and (songtype.split("#")[0].strip() not in ['betting', 'battle', 'result', 'warning', 'break']):
				print(game+": "+songid + " has the invalid/outdated type of "+songtype+"! f = fix, anything else = continue")
				key = cgetch()
				if key == 'f':
					if songtype == 'results':
						print("Assuming 'results' means 'result'.")
						arr[i] = arr[i].replace("results","result")
					else:
						type=""
						while type.split("#")[0].strip() not in ['betting', 'battle', 'result', 'warning', 'break']:
							type = input("Enter new type\n>")
						arr[i] = "        type: "+type+"\n"
		elif arr[i].startswith("  - id: "): #new game
			songid = ""
			game = arr[i].replace("  - id: ","").replace("\n","")
			if game[0] == '"':
				game = game[1:-1]
		i += 1
finally:
	updatefile()


input("\n\nPress enter to exit.")
