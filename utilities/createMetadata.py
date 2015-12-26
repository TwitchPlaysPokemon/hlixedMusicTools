import sys
if sys.version_info[0] == 2:
		print("""You are using Python 2 instead of Python 3.
This program only works in Python 3 because we're switching to py3 for PBR2.0!
""")
		raw_input('\n\nPress enter to exit.') #use raw_input because if we're here, we're in python 2!
		exit()


print("Music Pack maker v1.3")
print("\nThis program is intended to work with Revo's pack-making process! If you're not Revo, you can still use this, but ask him for the folder setup to use.")
input("\nPress enter to begin.")


import os

absolute_path = os.path.abspath(os.curdir).split(os.sep)
gamename = absolute_path[-1]
system = absolute_path[-2]
print("Beginning work on the game "+gamename+" for the "+system+"!")

categorylist = ["battle", "betting", "break", "result", "warning"]

filelist = os.listdir()

missingtypes = [stype for stype in categorylist if stype not in filelist]

if len(missingtypes) > 0:
	if len(missingtypes) == 1:
		print("Hey; I didn't see a "+missingtypes[0]+" folder! (This is normal if you didn't put any songs into that type)")
	else:
		print("I didn't see a folder for "+ ' or '.join(missingtypes) + "! (This is normal if you didn't put any songs into those types)")
	if input("Are you sure you want to continue? (y/n)\n>").startswith('n'):
		exit()

metaarr = []
gameid = gamename.strip().replace(" ","_").replace("!","").lower()
if '.' in gameid:
	gameid = ".".join(gamename.split(".")[:-1])
theinput = input("Enter game ID (or press enter to default to "+gameid+")\n>").strip()
if(theinput != ''):
	gameid = theinput
	print("Changed the game ID for "+gamename+" to "+gameid+"!")

gameseries = input("Enter series for "+gameid+": (you may want to check other games in a metadata file to ensure the same series name is used)\n>").strip().lower()

year=None
while year == None:
	try:
		theinput = input("Enter the year "+gamename+" was first released:")
		year = int(theinput)
	except ValueError:
		print("That wasn't a number!")

#start off with the game info
metaarr = ['  - id: '+gameid+'\n',
'    title: "'+gamename+'"\n',
'    series: '+gameseries+'\n',
'    year: '+str(year)+'\n',
'    platform: "'+system+'"\n',
'    path: "'+system+'/'+gamename+'"\n',
'    songs:\n']

if system.lower().strip() == 'other':
	platform = input("Enter the platform for "+gamename+"\n>")
	metaarr[3] ='    platform: "'+platform+'"\n'
	

presenttypes = [stype for stype in categorylist if stype in filelist]

def convertTitle(filename):
	filearr = filename.split(" ")
	if filearr[0].isnumeric(): #remove initial number
		filearr = filearr[1:]

		if '.' in filearr[-1]: #oh, and remove the extension as well
			lastword = filearr[-1].split('.')
			extension = lastword[-1]
			actualLastword = lastword[0]
			filearr[-1] = actualLastword

	newtitle = " ".join(filearr).strip()
	print("Assuming the title for "+filename+" is "+newtitle+"!")
	if '.brstm' in newtitle:
		newtitle = newtitle.replace(".brstm","")
		print("Oh; but the title contains .brstm. Assuming that the title is "+newtitle+"!")
	return newtitle


for songtype in presenttypes:
	for filename in os.listdir(songtype):
		path = filename
		title = convertTitle(filename)
		songid = title.replace(" ","_").replace("!","").replace(":","_").replace("'","").replace("__","_").lower()
		if '.' in songid:
			songid = ".".join(songid.split(".")[:-1])
		theinput = input("Enter song ID for "+title+" (or press enter to default to "+songid+")\n>").strip()
		if(theinput != ''):
			songid = theinput
			print("Changed the song ID for "+filename+" to "+songid+"!")
		metaarr.append('      - id: '+songid+"\n")
		metaarr.append('        title: "'+title+"\"\n")
		metaarr.append('        path: "'+filename+"\"\n")
		metaarr.append('        type: '+songtype+"\n")

if input("Move music files to root directory?(y/n)\n>").startswith('y'):
	for songtype in presenttypes:
		for filename in os.listdir(songtype):
			os.rename(songtype+os.sep+filename,filename)
		os.rmdir(songtype)
	print("Done!")
else:
	print("Okay, I won't, then. Run this program again if you want to do it later.")


if len(metaarr) > 0:
	f = open("metadata_"+gameid+".txt",'w')
	f.writelines(metaarr)
	f.close()
	input("\n\nWrote to metadata_"+gameid+".txt!\n\nPress enter to exit.")
else:
	quit()
