#Old program to autogenerate list of added songs from a control+A on the github website for a commit



with open("changelog.txt") as f:
	lines = f.readlines()

print(lines[0])

added = {}

gamename = ""
songname = ""
songtype = "betting"

for line in lines:
	if "/metadata.yaml" in line:
		gamename = " ".join(line.split("/metadata.yaml")[0].split(" ")[1:])
		gamename = gamename.replace("_",":")
	if line[0] == "+":

		if "+    type: " in line:
			songtype = line.replace("+    type: ","").strip()
			if songtype not in added:
				added[songtype] = []
			added[songtype].append(songname + " from " + gamename)
		if "+    title: " in line:
			songname = line.replace("+    title: ","").strip()[1:-1]


print(added)

for category in added:
	print("\n==For "+category+":")
	for song in added[category]:
		print(song)
