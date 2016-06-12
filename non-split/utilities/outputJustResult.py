typeToScanFor = input("Insert song type to scan for\n>").strip()

print("1hlixed's category outputter v1.1")
import re
import os
import sys

if sys.version_info[0] == 2:
		print("""You are using Python 2 instead of Python 3.
This program only works in Python 3 because as of PBR2.0 we're moving to python 3!
""")
		raw_input('\n\nPress enter to exit.') #use raw_input because if we're here, we're in python 2!
		exit()

print("This program will output all game+songids of type "+typeToScanFor+". (to change to another type, edit the first line of this program)\n")
filename = input("Enter the filename of the metadata file to analyze (put it in the same directory as this script):\n>")
f = open(filename,"r")
arr = f.readlines()
f.close()

print("Successfully read the file!")

for i in range(len(arr)):
	if(arr[i][-1] != "\n"):
		arr[i] += "\n"

def printnlog(thing):
	f = open("analysis.txt",'a')
	f.write(str(thing)+"\n")
	f.close()
	print(thing)

f = open("analysis.txt",'w') #clear analysis.txt
f.close()

i=0
game=""
songid = ""
songtype = ""
songOfTypeExisted = False

printnlog("--list of songs of type "+typeToScanFor+"--")
try:
	while i < (len(arr)):
		if arr[i].startswith("      - id: "):#new song
			if (songtype != '') and (songtype == typeToScanFor):
				printnlog(game+": "+songid + "")
				songOfTypeExisted=True
			title=""	
			songtype=""
			songid = arr[i].replace("  - id: ","").replace("\n","").strip()
			if songid[0] == '"':
				songid = songid[1:-1]
		elif arr[i].startswith("  - id: "): #new game
			if(songOfTypeExisted):
				printnlog("") #insert newline
				songOfTypeExisted=False
			songtype=""
			songid = ""
			game = arr[i].replace("  - id: ","").replace("\n","")
			if game[0] == '"':
				game = game[1:-1]
		elif arr[i].startswith("        type: "):
			songtype=arr[i].replace("        type: ","").replace("\n","").split("#")[0].strip()
		i += 1

finally:
	printnlog("--end songs of type "+typeToScanFor+"--")
input("\n\nPress enter to exit.")
