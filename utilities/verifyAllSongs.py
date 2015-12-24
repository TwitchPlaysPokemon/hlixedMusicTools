print("1hlixed's metadata file verifier v3.2")
import re
import os
import sys

import sys
if sys.version_info[0] == 2:
		print("""You are using Python 2 instead of Python 3.
This program only works in Python 3 because as of PBR2.0 we're moving to python 3!
""")
		raw_input('\n\nPress enter to exit.') #use raw_input because if we're here, we're in python 2!
		exit()


print("This program will ensure that all the songs in a metadata file have the right format, and also tell you if a song's BRSTM file doesn't exist.\n")
filename = input("Enter the filename of the metadata file to analyze (put it in the same directory as this script):\n>")
f = open(filename,"r")
arr = f.readlines()
f.close()

print("Successfully read the file!")

for i in range(len(arr)):
	if(arr[i][-1] != "\n"):
		arr[i] += "\n"


def updatefile():
	f2 = open(filename,'w')
	f2.writelines(arr)
	f2.close()
	print("Metadata files updated!")

#first, make sure all games have "song:" tags
i=0
stuffChanged=False
game = ""
hasSongs=False
scannedThisGame = False



def printnlog(thing):
	f = open("analysis.txt",'a')
	f.write(str(thing)+"\n")
	f.close()
	print(thing)

#First, do a pass correcting spaces
i=0
while i < (len(arr)):
	if arr[i].startswith("    path: Other/"):
		game = arr[i].replace("    path: Other/","")
		if not arr[i+1].startswith("    songs:"):
			hasSongs=True
		scannedThisGame = False
	if arr[i].startswith("      - id: "): #song id
		if not hasSongs and not scannedThisGame and (game != ""):
			#arr[i-1:i-1] = ["    songs:\n"]
			printnlog("A game ("+game+") doesn't have a 'songs:' tag! (line " +str(i)+")")
			hasSongs=False
		scannedThisGame = True
	#check for wrong indentation
	if "  - id: " in arr[i]:
		isGame=True
		for j in range(3):
			if not (arr[i+j+1].startswith("    platform: ") or arr[i+j+1].startswith("    year: ") or arr[i+j+1].startswith("    path: ") or arr[i+j+1].startswith("    title: ")):
				isGame=False
		if (not isGame) and (arr[i].startswith("  - id: ")):
			printnlog(arr[i]+"has the wrong amount of spaces! (line "+str(i)+")")
		elif (isGame) and (arr[i].startswith("      - id: ")):
			printnlog(arr[i]+"has the wrong amount of spaces! (line "+str(i)+")")
	#while we're at it check for non-standard indentation
		normalArr = ["        ","    "]
		whitespacestr = arr[i].replace("-",' ')
		good=False
		for thing in normalArr:
			if whitespacestr.replace(thing,'')[0].isalpha():
				good=True
		if arr[i].strip().startswith('#'):
			good=True
		if not good:
			printnlog(" line "+str(i)+" had bad whitespace: "+arr[i])
			errorsExist=True

	#ensure comments have spaces before them
	if '#' in arr[i]:
		index = arr[i].index('#')
		if (index > 4) and (arr[i][index-1] != ' '):
			printnlog(" line "+str(i)+" has a comment without a space before it!")	
			errorsExist=True
	#surround titles and paths in quotes
	if ("path:" in arr[i]) or ("title:" in arr[i]):
		if '"' not in arr[i]:
			printnlog("Put spaces around line "+str(i)+": "+arr[i])
	#while we're at it ensure that you don't have only one quote
	if arr[i].count('"')==1:
		printnlog(arr[i]+"has the wrong amount of quotes! (line "+str(i)+")")

	
		
	i += 1
if stuffChanged:
	updatefile()

f = open("analysis.txt",'w') #clear analysis.txt
f.close()


songidarr=[]
songarr = []
prevGame = ""
i=0
game=""
songpath=""
title="-1"
songtype=""
songid = ""
brokeCount=0
gamepath = ""
yearExists = False

errorsExist = False


otherFolder = False
#if os.path.exists("Other"):
#	otherFolder = True

idArr = []
gameArr = []

selfDuplicating = {"games":[],"songid":[]}
try:
	while i < (len(arr)):
		if arr[i].startswith("    path: "): #game path
			gamepath = arr[i].replace("    path: ","").replace("\n","")
			if gamepath[0] == '"':
				gamepath = gamepath[1:-1]

		elif arr[i].startswith("      - id: "):#new song
			if title == "-1":
				pass
			if songid.lower() != songid:	
				printnlog(game+": "+songid + " is not a lowercase song ID!")
				errorsExist=True
			if len(songid.strip()) > 50:
				printnlog(game+": "+songid + " is over 50 characters!")
			if (songtype != '') and (songtype.strip() not in ['betting', 'battle', 'result', 'warning', 'break']):
				printnlog(game+": "+songid + " has the invalid/outdated type of "+songtype+"!")
				errorsExist=True

			elif songpath and title and songtype:
				if not os.path.isfile(gamepath+"/"+songpath) and otherFolder:
					printnlog("BRSTM not found! ["+game+"] "+gamepath+"/"+songpath)
					errorsExist=True
			else:
				if songid != '':
					string = game+": "+songid + " is incomplete! (missing"
					if not songtype:
						string += " type;"
					if not title:
						string += " title;"
					if not songpath:
						string += " path;"
					string += ")"
					printnlog(string)

					brokeCount += 1
					errorsExist = True
			songpath=""
			title=""	
			songtype=""
			songid = arr[i].replace("  - id: ","").replace("\n","").strip()
			if songid[0] == '"':
				songid = songid[1:-1]
			if songid not in idArr:
				idArr.append(songid)
				gameArr.append(game)
			else:
				if game == gameArr[idArr.index(songid)]:
					printnlog(songid+" (from "+game+") shares an ID with another game with the same id!")
					selfDuplicating["games"].append(game)
					selfDuplicating["songid"].append(songid)
				else:
					printnlog(songid+" (from "+game+") shares an ID with "+songid+" from "+gameArr[idArr.index(songid)]+"!")
		elif arr[i].startswith("  - id: "): #new game
			if brokeCount > 5:
				#printnlog("TAKE A LOOK AT "+game+" it may have songs missing!")
				pass
			brokeCount=0
			if title == "-1":
				pass
			elif songpath and title and songtype:
				if not os.path.isfile(gamepath+"/"+songpath) and otherFolder:
					printnlog("BRSTM not found! ["+game+"] "+gamepath+"/"+songpath)
					errorsExist=True
			else:
				string = game+": "+songid + " is incomplete! (missing"
				if not songtype:
					string += " type;"
				if not title:
					string += " title;"
				if not songpath:
					string += " path;"
				string += ")"
				printnlog(string)

				brokeCount += 1
				errorsExist = True
			songpath=""
			title="-1"	
			songtype=""
			songid = ""
			game = arr[i].replace("  - id: ","").replace("\n","")
			if game[0] == '"':
				game = game[1:-1]
			yearExists = False
		elif arr[i].startswith("    year:"):
			yearExists = True

		elif arr[i].startswith("    songs:"):
			if not yearExists:
				printnlog(game + " doesn't have a 'year:' attribute!")
				errorsExist = True
		elif arr[i].startswith("        path: "):
			songpath=arr[i].replace("        path: ","").split("#")[0].replace("\n","")
			if songpath[0] == '"':
				songpath = songpath[1:-1]
		elif arr[i].startswith("        title: "):
			title=arr[i].replace("        title: ","").split("#")[0].replace("\n","")
			if title[0] == '"':
				title = title[1:-1]
		elif arr[i].startswith("        type: "):
			songtype=arr[i].replace("        type: ","").replace("\n","").split("#")[0].strip()
		i += 1

#finally, import it with python's built-in tools to see if any errors happen
	f = open(filename,"r")

	printnlog("Attempting to load the file with a YAML parser...")
	try:
		import yaml
		yaml.load(f.read())
		printnlog("YAML parser test comes up clean!")
	except ImportError:
		printnlog("No PyYaml library detected, not using YAML parser test. Use pip3 to install it if you want.")
	except yaml.YAMLError as e:
		printnlog("\n===The YAML parser test encountered an error! Here it is:===")
		printnlog(e)
		if hasattr(e, 'problem_mark'):
			mark = e.problem_mark
			printnlog("(check line "+str(mark.line+1)+"!)")
		errorsExist=True
		printnlog("Note that the YAML parser crashes on the first error it finds; run me again after fixing that error.")

finally:
	if not errorsExist:
		printnlog("\nLooks like all songs in this file have no errors!")
	else:
		if len( selfDuplicating["games"]) > 0:
			printnlog("\n\nThe following games have duplicate game ID errors:")
			printed = []
			for i in selfDuplicating["games"]:
				if i not in printed:
					printed.append(i)
					string = i + " - contains "
					for j in range(len(selfDuplicating["games"])):
						if selfDuplicating["games"][j] == i:
							string += selfDuplicating["songid"][j]+ ","
					printnlog(string[:-1]) #chop trailing comma
		printnlog("\nMake sure to fix those errors!")


	if not otherFolder:
		printnlog("\n[WARNING] An Other/ folder was not detected, so this program is unable to tell if any songs don't have BRSTM files. If you want to check that all songs have BRSTM files, add an Other folder and put the BRSTM files in their respective game folder that to enable BRSTM scanning.")

input("\n\nPress enter to exit.")
