# coding: utf-8
print("1hlixed's series tag inserter v1.2")

import sys
if sys.version_info[0] == 2:
		print("""You are using Python 2 instead of Python 3.
This program only works in Python 3 because as of PBR2.0 we're moving to python 3!
""")
		raw_input('\n\nPress enter to exit.') #use raw_input because if we're here, we're in python 2!
		exit()


print("This program will insert a user-prompted 'series: ' tag in each game.\n")
filename = input("Enter the filename of the metadata file to analyze (put it in the same directory as this script):\n>")
f = open(filename,"r")
arr = f.readlines()
f.close()

print("Successfully read the file!")

def updatefile():
	f2 = open(filename,'w')
	f2.writelines(arr)
	f2.close()
	print("Metadata file updated!")

def printnlog(thing):
	f = open("analysis.txt",'a')
	f.write(str(thing)+"\n")
	f.close()
	print(thing)


dataPts = [
"    title: ",
"    series: ",
"    platform: ",
"    year: ",
"    path: "]

dataPtExists = {}
dataPtI = {}

def clearDatapts():
	global dataPtExists
	for x in dataPts:
		dataPtExists[x]=False
		dataPtI[x] = None

clearDatapts()

i=0
game=""
previouslyEnteredSeries = []

seriesTag = "    series: "

try:
	while i < (len(arr)):
		for tag in dataPts:
			if arr[i].startswith(tag):
				dataPtExists[tag]=True
				dataPtI[tag] = i
		if arr[i].startswith("  - id: "): #new game
			game = arr[i].replace("  - id: ","").replace("\n","").replace("é","e")
			if game[0] == '"':
				game = game[1:-1]
		elif arr[i].startswith("    songs:"):
			for tag in dataPts:
				if not dataPtExists[tag]:
					if tag != seriesTag:
						print("Game "+game + " is missing a "+tag.strip() +" entry!")
					else:
						newSeries = input("\nPreviously entered series: "+", ".join(previouslyEnteredSeries)+"\nEnter series for "+game+": (or 'clear' to clear the previously entered series)\n>").strip()
						if newSeries == 'clear':
							previouslyEnteredSeries = []
							newSeries = input("Series data cleared. Enter series for "+game+":\n>").strip()

						if newSeries != 'sdadd':
							if newSeries not in previouslyEnteredSeries:
								previouslyEnteredSeries.append(newSeries)
							insertionPoint = dataPtI["    title: "] #place after platform
							try:
								int(insertionPoint)
							except:
								print("ERROR FOUND!" +"\n".join(arr[i-5:i+5]))
								quit()
							arr = arr[0:insertionPoint+1]+[seriesTag+newSeries+'\n']+arr[insertionPoint+1:]
							i += 1
							print("Entered "+newSeries)
						else:
							print("Skipping "+game+"; run me again to fill it out")
			clearDatapts()
					
		i += 1
except:
	if input("Aborting; \nsave entered series data to the file? (y/n):").strip().lower().startswith('y'):
		print("Saving...")
		updatefile()
	input("\n\nPress enter to exit.")
	quit()

updatefile()
input("\n\nPress enter to exit.")
