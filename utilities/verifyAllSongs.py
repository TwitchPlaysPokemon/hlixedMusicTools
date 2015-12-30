print("1hlixed's metadata file verifier v3.3")
import re
import os

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

#add newlines to the end of the file; some encodings end up with problems

for i in range(len(arr)):
	if(arr[i][-1] != "\n"):
		arr[i] += "\n"

def printMissingSongTags():
	string = game+": "+songid + " is incomplete! (missing"
	if not songtype:
		string += " type;"
	if not songtitle:
		string += " title;"
	if not songpath:
		string += " path;"
	string += ")"
	printnlog(string)

def printnlog(thing):
	#function to both print and write to analysis.txt at the same time
	f = open("analysis.txt",'a')
	f.write(str(thing)+"\n")
	f.close()
	print(thing)

f = open("analysis.txt",'w') #clear analysis.txt
f.close()

#lists of things to check for
gameTagList = [
'title',
'year',
'platform',
'path',
'series']

validSongtypes = ['betting', 'battle', 'result', 'warning', 'break']

#loop variables
game     =""
gamepath =""

songpath =""
songtitle="-1"
songtype =""
songid   =""

errorsExist = False

#whether to enable testing BRSTM files' existence
otherFolder = os.path.exists("Other")
useOtherFolder = False
if otherFolder:
	useOtherFolder = input("Scan the Other/ folder to ensure each song's BRSTMs exist? (y/n)\n>").lower().strip().startswith('y')

#variables for duplicate-ID detection
idArr = []
gameArr = []

selfDuplicating = {"games":[],"songid":[]}

#surrounded in a try-finally so control+c breaks out
try:
	i=0
	while i < (len(arr)):
		if arr[i].startswith("      - id: "):#new song
			if songtitle == "-1":
				pass
			#ensure song ids are lowercase
			if songid.lower() != songid:	
				printnlog(game+": "+songid + " is not a lowercase song ID!")
				errorsExist=True
			#song IDs shouldn't be over 50 characters
			if len(songid.strip()) > 50:
				printnlog(game+": "+songid + " is over 50 characters!")
			#check for outdated/invalid songtypes
			if (songtype != '') and (songtype.strip() not in validSongtypes):
				printnlog(game+": "+songid + " has the invalid/outdated type of "+songtype+"!")
				errorsExist=True

			#If we have an other folder, ensure the BRSTM exists
			if useOtherFolder and songpath and not os.path.isfile(gamepath+"/"+songpath):
				printnlog("BRSTM not found! ["+game+"] "+gamepath+"/"+songpath)
				errorsExist=True

			#If a song doesn't have a path, title, or type tag, say so
			if not (songpath and songtitle and songtype):
				if songid != '':
					printMissingSongTags()
					errorsExist = True
			songpath=""
			songtitle=""	
			songtype=""
			songid = arr[i].replace("  - id: ","").replace("\n","").strip()
			if songid[0] == '"':
				songid = songid[1:-1]
			#before moving on, test for songs with the same ID as the newly-encountered one
			if songid in idArr:
				if game == gameArr[idArr.index(songid)]:
					printnlog(songid+" (from "+game+") shares an ID with another song from the same game! (duplicate?)")
					selfDuplicating["games"].append(game)
					selfDuplicating["songid"].append(songid)
					errorsExist=True
				else:
					printnlog(songid+" (from "+game+") shares an ID with "+songid+" from "+gameArr[idArr.index(songid)]+"!")
					errorsExist=True
			else:
				idArr.append(songid)
				gameArr.append(game)
		elif arr[i].startswith("  - id: "): #new game
			#Before we get to analyzing the new game, first check the last song of the previous game
			if songtitle == "-1":
				pass
			#If we have an other folder, ensure the BRSTM exists
			elif useOtherFolder and songpath and not os.path.isfile(gamepath+"/"+songpath):
				printnlog("BRSTM not found! ["+game+"] "+gamepath+"/"+songpath)
				errorsExist=True

			#If a song doesn't have a path, title, or type tag, say so
			elif not (songpath and songtitle and songtype):
				if songid != '':
					printMissingSongTags()
					errorsExist = True
			#reset for new game, and log the ID
			songpath=""
			songtitle="-1"
			songtype=""
			songid = ""
			game = arr[i].replace("  - id: ","").replace("\n","")
			if game[0] == '"':
				game = game[1:-1]
			#finally, check for songs: tag; it should be 5 or 6 lines after the "-id" line, depending on if there's a series tag or not
			if not (arr[i+6].startswith("    songs:") or arr[i+5].startswith("    songs:")):
				printnlog("A game ("+game+") doesn't seem to have a 'songs:' tag! (line " +str(i)+")")
				errorsExist=True
		if arr[i].startswith("    path: "): #game path
			gamepath = arr[i].replace("    path: ","").replace("\n","")
			if gamepath[0] == '"':
				gamepath = gamepath[1:-1]
		elif arr[i].startswith("    songs:"):
			#check for all the game tags in the last 5 or so lines
			for tag in gameTagList:
				tagPresent = False
				for j in range(len(gameTagList)):
					thetag = arr[i-j-1].split(":")[0].strip()
					if thetag == tag:
						tagPresent = True
				if not tagPresent:
					printnlog(game + " doesn't have a '"+tag+":' tag!")
					errorsExist = True
		#store song data for future use
		elif arr[i].startswith("        path: "): #song path
			songpath=arr[i].replace("        path: ","").split("#")[0].replace("\n","")
			if songpath[0] == '"':
				songpath = songpath[1:-1]
		elif arr[i].startswith("        title: "): #song title
			songtitle=arr[i].replace("        title: ","").split("#")[0].replace("\n","")
			if songtitle[0] == '"':
				songtitle = songtitle[1:-1]
		elif arr[i].startswith("        type: "): #song type
			songtype=arr[i].replace("        type: ","").replace("\n","").split("#")[0].strip()
		###general formatting tests###

		#check for games indented like a song or songs indented like a game
		if "  - id: " in arr[i]:
			isGame=True
			#check the next 3 tags to see if the current entry is a game or a song
			#We don't check all 5 tags of a game since that would throw an error when checking the last song in the file, which only has 4 lines after it
			for j in range(3):
				if not (arr[i+j+1].split(':')[0].strip() in gameTagList):
					isGame=False
			if (not isGame) and (arr[i].startswith("  - id: ")):
				printnlog(arr[i]+"has the wrong amount of spaces! (line "+str(i)+")")
				errorsExist=True
			elif (isGame) and (arr[i].startswith("      - id: ")):
				printnlog(arr[i]+"has the wrong amount of spaces! (line "+str(i)+")")
				errorsExist=True
		#Check for non-standard indentation; it should be 4, 8, or 0 spaces before a line
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

		#ensure end-of-line comments have spaces before them
		if '#' in arr[i]:
			index = arr[i].index('#')
			if (index > 4) and (arr[i][index-1] != ' '):
				printnlog(" line "+str(i)+" has a comment without a space before it!")	
				errorsExist=True
		#surround titles and paths in quotes
		if ("path:" in arr[i]) or ("title:" in arr[i]):
			if '"' not in arr[i]:
				printnlog("Put quotes around line "+str(i)+": "+arr[i])
				errorsExist=True
		#while we're at it ensure that you don't have mismatched quotes
		amtQuotes = arr[i].count('"') - arr[i].count('\\"')
		if amtQuotes not in [0,2]:
			printnlog(arr[i]+"has the wrong amount of quotes! (line "+str(i)+")")
			errorsExist=True

		#update the while loop
		i += 1

	#finally, import it with pyYaml to see if any errors happen there
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

	#and that's all the tests!

finally:
	if not errorsExist:
		printnlog("\nLooks like all songs in this file have no errors!")
	else:
		#all other errors have been printnlogged already
		#summarize duplicate game ID errors in a nice format
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
	elif not useOtherFolder:
		printnlog("\n[NOTE] An Other/ folder was detected, but you declined to scan it. This analysis is unable to tell if any songs in this metadata file don't have BRSTM files. If you want to check that all songs have BRSTM files, run this program again and enter 'y' when prompted.")

input("\n\nPress enter to exit.")
