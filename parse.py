#Dirty program to autogenerate list of added songs from a control+A on the github website for a commit
#To use, first select the changelog page, and save it into a file named changelog.txt. Then run this! It'll output to newsongs.txt, and all that's left to do is add a line at the top saying "Songs added on <date>".

import collections
with open("changelog.txt") as f:
	lines = f.readlines()

print(lines[0])

added = collections.OrderedDict()

gamename = ""
songname = ""
songtype = "betting"

i=0
while i < len(lines):
	line = lines[i]
	if "/metadata.yaml" in line:
		gamename = " ".join(line.split("/metadata.yaml")[0].split(" ")[1:])
		gamename = gamename.replace("_",":")
	if line.startswith("+  - id:"):
		#collect song title and type from the next 4 lines
		for j in range(1,4):
			songline = lines[i+j]
			if songline.startswith("+  - id:"):
				print("The song on line "+str(i)+" seems to be missing a tag? Aborting...")
				exit()
			if songline.startswith("+    type: "):
				songtype = songline.replace("+    type: ","").strip()
			if songline.startswith("+    title: "):
				songname = songline.replace("+    title: ","").strip()[1:-1]

		if songtype not in added:
			added[songtype] = []
		added[songtype].append(songname + " from " + gamename)
	i += 1
#print the results, while also outputting to a file
outputFilename = "newsongs.txt"
toPrint = []

def printnlog(string):
	print(string)
	toPrint.append(string + '\n')

for category in added:
	printnlog("\n==For "+category+":")
	for song in added[category]:
		printnlog(song)

#output to a file as well as printing
with open(outputFilename, 'w') as f:
	f.writelines(toPrint)
input("\n\nThe above has also been outputted to "+outputFilename+" for easy copypasting! \nPress enter to exit.")
