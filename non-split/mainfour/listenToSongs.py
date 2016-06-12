import sys
if sys.version_info[0] == 2:
		print("""You are using Python 2 instead of Python 3.
This program only works in Python 3 because 1hlixed hasn't gotten around to porting it to python 2.7. I recommend pestering 1hlixed repeatedly.
""")
		raw_input('\n\nPress enter to exit.') #use raw_input because if we're here, we're in python 2!
		exit()



print("1hlixed's song listener v1.1")
print("\nthis program is intended to work with download.py, and will play the BRSTM using aplay for each song in the 'downloaded.txt' that download.py creates. ")
print("\nNote that this version of the program only works with linux and with my BRSTM playing script (since I never thought I'd be releasing this). To make a version for other OSes, replace the playbrstm() and stopbrstm() functions with winamp-related functionality.")
input("\nPress enter to begin.")
import re
import os
import getch
import subprocess
#call(["ls", "-l"])


listenedfile = 'listeningdownloaded.txt'

try:
	f = open(listenedfile)
except:
	print("No "+listenedfile+" detected; making a copy of downloaded.txt...")
	f = open('downloaded.txt')
	f2 = open(listenedfile,'w')
	arr = f.readlines()
	for i in range(len(arr)):
		arr[i] = '[ ]'+arr[i]
	f2.writelines(arr) #copy downloaded.txt into it
	f.close()
	f2.close()

f = open(listenedfile)
arr = f.readlines()
f.close()

def updatefile():

	f2 = open(listenedfile,'w')
	f2.writelines(arr)
	f2.close()
	print("Metadata files updated!")



playshplace = os.path.expanduser("~/Downloads/vgmstream/play.sh") #This is where I keep the script that lets me play BRSTM files since I use linux.
#If you play BRSTMs with winamp you'd overwrite this function below
#os.path.expanduser() lets me substitute ~ for the home directory
def playbrstm(songfile):
	subprocess.Popen(["sh", playshplace, songfile,"&"],stderr=subprocess.DEVNULL,stdout=subprocess.DEVNULL)

def stopbrstm():
  #Again, change if you use winamp
	subprocess.call(["killall","aplay"])

def cgetch():
	key = getch.getch() #this blocks
	if key == '\x03': #control+c
		print("Quitting...")
		updatefile()
		stopbrstm()
		exit()
	return key

undoing=False
try:
	arrlen = len(arr)
	i=0
	while i < arrlen:
		try:
			gamename,songname,filename,songtype = arr[i][3:].split("|||")
		except:
			print(i)
		checkbox = arr[i][:3]
		if (checkbox == '[ ]') or undoing:
			undoing=False
			playbrstm('Other/'+gamename+'/'+filename)
			print("\nNow playing: "+songname+ " from "+gamename)
			print("Submitted for: "+songtype)
			print("u: undo | n: No | c: Change type | y: Yes | q:quit | r:restart song |f:fix BRSTM not playing")
			key = cgetch()
			stopbrstm()
			#do stuff
		

			if (key == 'r'):
				continue
			if (key == 'f'):
				fixdict = {'\\xc3\\xa9':'e',"\\'":"",':':'_',"\\xe2\\x84\\xa2":"(TM)"}  #accented e in pokemon, \', :, the trademark symbol
				fixdictafter = {"'":"","/":""} #go after \\' so it doesn't remove it before \\' runs
				newgamename = gamename
				newfile = filename
				for badstr in fixdict:
					if (badstr in newgamename):
						newgamename = newgamename.replace(badstr,fixdict[badstr])
					if badstr in filename:
						newfile = filename.replace(badstr,fixdict[badstr])
				for badstr in fixdictafter:
					if (badstr in newgamename):
						newgamename = newgamename.replace(badstr,fixdictafter[badstr])
					if badstr in filename:
						newfile = filename.replace(badstr,fixdictafter[badstr])
	
				print(newgamename)
				if newgamename != gamename:#if the gamename is bad
					if os.path.isdir("Other/"+gamename): #test if a bad folder name exists
						os.rename("Other/"+gamename,"Other/"+newgamename)
						print("Renaming "+gamename+" folder to "+newgamename)
						gamename = newgamename
					elif os.path.isdir("Other/"+newgamename): #if the folder was already renamed
						if os.path.exists("Other/"+newgamename+'/'+filename):
							print("Assuming the song belongs in the "+newgamename+" folder!")
							gamename = newgamename
						else:
							input("Huh; a "+newgamename+" folder exists, but the BRSTM isn't in it. Something might be wrong; I'll wait while you fix it.\nPress enter to continue")

				if (newfile != filename): #If the filename needs to be replaced
					if os.path.isfile("Other/"+gamename+'/'+filename):
							os.rename("Other/"+gamename+'/'+filename,"Other/"+gamename+'/'+newfile)
							filename = newfile
							print("Renaming "+filename+" folder to "+newfile)
					elif os.path.isfile("Other/"+gamename+'/'+newfile):
						print("Huh; looks like the BRSTM is already renamed. Convenient!")
						filename = newfile
					else:
						print("No BRSTM file found for "+gamename+'/'+filename+"! Weird.")
						input("\nPress enter to continue")

				arr[i]=checkbox+"|||".join([gamename,songname,filename,songtype]) #apply changes
				continue
			if (key == 'u') and (i > 0): #undo
				i -= 1
				undoing=True
				continue
			if key == 'n': #no
				checkbox = '[n]'
				print("Any comments to add? \nb:borderline (combine this with another), d:does not fit,i:intro,o:other (type), w:WutFace, l:lyrics, t:not tense and charged enough for battle")
				key = cgetch()
				borderline = False
				if key == 'b':
					borderline = True
					print("Borderline: yes")
					key = cgetch()
				if key == 't':
					checkbox = '[n- not tense and charged enough]'
				if key == 'i':
					checkbox = '[n- intro takes too long to start up]'
				if key == 'l':
					checkbox = '[n- lyrics]'
				if key == 'w':
					checkbox = '[n- WutFace]'
				if key == 'd':
					checkbox = '[n- does not fit]'
				if key == 'o':
					reason = input("Enter reason for no:\n>")
					checkbox = '[n- '+reason+']'
				if borderline: #apply borderline
					checkbox = '[n- borderline '+checkbox[4:]
				print("Song denied because "+checkbox[4:])
			if key == 'y': #yes
				checkbox = '[#]'
			if key == 'c': #change type
				print("Types: battle, betting, result, warning, break\nr:result|w:warning|be:betting|ba:battle|br:break")
				newtype = False
				
				while newtype == False:
					typedict = {'ba':'battle','be':'betting','r':'result','w':'warning','br':'break'}
					key1 = cgetch() #this is blocking
					print(key1)
					key2 = ''
					if key1 == 'b':
						key2 = cgetch() #this is also blocking
					elif key1 == 'q':  #quit
						newtype = songtype
					newstring = key1+key2
					print(newstring)
					if newstring in typedict:	
						newtype = typedict[newstring] + '\n'
						print("Changing type to "+newtype+", to undo use 'u' to go back to this song and 'c' to change type again")
						checkbox = '[#]'
				songtype = newtype
			if (key == 'q'): #quit
				updatefile()
				stopbrstm()
				exit()


			arr[i]=checkbox+"|||".join([gamename,songname,filename,songtype])
		i += 1
finally:
	print("Quitting...")
	updatefile()
	stopbrstm()
