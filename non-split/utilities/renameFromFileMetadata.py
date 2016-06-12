import os

import sys
if sys.version_info[0] == 2:
		print("""You are using Python 2 instead of Python 3.
This program only works in Python 3 because as of PBR2.0 we're moving to python 3!
""")
		raw_input('\n\nPress enter to exit.') #use raw_input because if we're here, we're in python 2!
		exit()

print("Silly-titled file renamer v2") 


def process(filename):
	f = open(filename,'rb')
	arr = f.readlines()
	f.close()
	title = None

	for i in range(1,len(arr)):
		thestr = str(arr[i])[2:-1] #chop off bytestring representation
		thestr = thestr.replace("\\n","")
		metatype = thestr.split("=")[0]
		if metatype == "title":
			title = thestr.split("=")[1]

	if title != None:

		badchrs = "\/:*?\"<>|"
		for i in title:
			if i in badchrs:
				input("The title is "+title+", but it has the invalid character "+i+" in it; not renaming. \nPress enter when ready.")
				return

		filenamearr = filename.split(".")
		extension = filenamearr[-1]

		dirname = os.path.dirname(filename)
		if dirname == None:
			dirname = ''
		print("Renaming "+ filename + " to "+ title+'.'+extension+"...")
		os.rename(filename,dirname+os.sep+title+'.'+extension)
		print("Done! file is now at "+ dirname+os.sep+title+'.'+extension+"\n")
	
		title=None
	else:
		print("\nNo title found in "+filename+"; not renaming.\n")

filename = input("Enter filename to rename, or a directory to scan (filenames contain dots for the extension):\n>").strip()
if filename == '':
	print("Quitting...")
	quit()
elif (filename[0] in ['"',"'"]) and (filename[-1] in ['"',"'"]):
	filename = filename[1:-1]

#scan
if '.' in filename:
	process(filename)
else:
	dirname = filename
	os.listdir(dirname)
	filetype = input("Enter an extension to scan for, starting with a dot: (or press enter to scan everything in the "+filename+" folder\n>").strip()
	filesToScan = os.listdir(dirname)
	if filetype != "":
		filesToScan = [fname for fname in filesToScan if fname.split(".")[-1]== filetype.replace(".","")]
	for filename in filesToScan:
		process(dirname+os.sep+filename)


input("\n\nPress enter to exit.")
