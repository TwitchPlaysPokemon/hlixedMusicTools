import sys
if sys.version_info[0] == 2:
		print("""You are using Python 2 instead of Python 3.
This program only works in Python 3 because 1hlixed hasn't gotten around to porting it to python 2.7. I recommend pestering 1hlixed repeatedly.
""")
		raw_input('\n\nPress enter to exit.') #use raw_input because if we're here, we're in python 2!
		exit()



listenedfile = 'listeningdownloaded.txt'

print("1hlixed's "+listenedfile+" duplicate remover v1.0")
print("\nthis program is intended to work with download.py and listenToSong.py and will remove any duplicate entries for songs, keeping the first one.")
print("Note that this doesn't scan for songs already in the metadata file, or rejected in previous submissions; copy the listeningdownloaded.txt to the top of the new "+listenedfile+" file to do that.")
input("\nPress enter to begin.")

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
	f2.writelines(newarr)
	f2.close()
	print("Metadata files updated!")

gamearr = []
songarr = []

newarr = []
caught=0
for i in arr:
	try:
		gamename,songname,filename,songtype = i[3:].split("|||")
	except:
		print("Error getting data; here's the offending line:\n"+i)
		input("Press enter to exit")
	dup = False
	if (gamename in gamearr):
		for index in [x for x in range(len(songarr)) if songarr[x] == songname]:
			if gamearr[index] == gamename:
				print("Duplicate of "+gamename+" - "+songname)
				dup=True
				caught += 1
	gamearr.append(gamename)
	songarr.append(songname)
	if not dup:
		newarr.append(i)

if input("Found "+str(caught)+" duplicates. Remove? (y/n)\n>").strip().lower()=='y':
	updatefile()
