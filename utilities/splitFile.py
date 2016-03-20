print("1hlixed's giga-metadata-file splitter v1.3")
import re
import os

import sys
if sys.version_info[0] == 2:
		print("""You are using Python 2 instead of Python 3.
This program only works in Python 3 because as of PBR2.0 we're moving to python 3!
""")
		raw_input('\n\nPress enter to exit.') #use raw_input because if we're here, we're in python 2!
		exit()


print("This program will split an old PBR1.0 metadata file into one files per game for musicCat.\n")
filename = input("Enter the filename of the metadata file to analyze (put it in the same directory as this script):\n>")
f = open(filename,"r")
arr = f.readlines()
f.close()

print("Successfully read the file!")

for i in range(len(arr)):
	if(arr[i][-1] != "\n"):
		arr[i] += "\n"
	if not (0 <= arr[i].find('#') <= 8):
		arr[i] = arr[i][4:]

headerArr = ["---\n"]

versionNum = input("Add a version number? If so, enter it, otherwise just press enter without typing anything:\n>").replace(" ","").replace("\n","").strip()

if versionNum != "":
	headerArr += ["info:\n",
"    version: "+versionNum+"\n"]


lastIndex = 0
gamepath = ""
i=0
while i < (len(arr)):
	if arr[i].startswith("s: "): #games:
		lastIndex=i
	if arr[i].startswith("path: "): #game path
		print("found path")
		gamepath = arr[i].replace("path: ","").replace("\n","")
		if gamepath[0] == '"':
			gamepath = gamepath[1:-1]
	if arr[i].startswith("id: "): #new game
		if lastIndex+1 == i:
			i += 1
			continue
		print(gamepath)
		toBeWritten = arr[lastIndex:i]
		#print(arr[lastIndex+1:i])
		try:
			os.makedirs(gamepath)
		except:
			pass
		#add header info
		toBeWritten = headerArr + toBeWritten
		if not toBeWritten[-1].strip().startswith("..."):
			toBeWritten.append("...\n")
		f2 = open(gamepath+"/metadata.yaml",'w')
		f2.writelines(toBeWritten)
		f2.close()
		lastIndex=i
	i += 1
		

input("\n\nPress enter to exit.")
