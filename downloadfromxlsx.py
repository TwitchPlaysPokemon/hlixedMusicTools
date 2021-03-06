import sys
if sys.version_info[0] == 2:
    print("""You are using Python 2 instead of Python 3.
This program only works in Python 3.""")
    raw_input('\n\nPress enter to exit.') #use raw_input because if we're here, we're in python 2!
    exit()


print("1hlixed's automatic BRSTM downloader v3.1")
import urllib.request
import re
import os
import shutil

try:
	from openpyxl import load_workbook
	from unidecode import unidecode
except ImportError:
	input("openpyxl and unidecode are needed to use this program! Install them with 'pip3 install openpyxl unidecode'.\nPress enter to exit.")
	exit();

docfilename = "TPP Music .xlsx"

print("Reading submissions from "+docfilename)
#load the doc
doclines= []
try:
	doc = load_workbook(docfilename).active
	doclines = [line for line in doc]
	doclines= [[cell.value for cell in line] for line in doclines]
		
except FileNotFoundError as e:
	print("===ERROR===\n" + docfilename + " not found. To use this program, Use File -> Download As -> XLSX to download the music doc and save '"+docfilename + "' in the same folder as this program.")
	input("\n\nPress enter to exit.")
	exit()

#load downloaded.txt, which lets the state persist over multiple sessions
statusArr = []
try:
	with open("downloaded.txt", "r", encoding="utf-8") as f:
		statusArr = f.readlines()
		#grab range
		inputtedrange = [int(x) for x in statusArr[0].split("-")]
		dlrange = range(inputtedrange[0],inputtedrange[1])

except FileNotFoundError as e:
	linestodl = input("Enter line range to download (such as '200-300' or '1950-2300')\n:")
	inputtedrange = [int(x) for x in linestodl.split("-")]
	dlrange = range(inputtedrange[0],inputtedrange[1])
	statusArr = [linestodl + '\n'] + ["[ ]"+str(doclines[i][0])+'\n' for i in dlrange]

#sanity tests
assert dlrange.start > 2
assert dlrange.stop < len(doclines)
assert dlrange.stop > dlrange.start

gameregex = re.compile('(?<=<span id="game"><a href="/game/).*?(?=</a><br>)')
#<td><span id="name">Fighting of the Spirit (Arrange Version)</span>

nameregex = re.compile('(?<=(<span id="name">)).*?(?=</span>)')

def updatefile():
	f2 = open('downloaded.txt', 'w', encoding="utf-8")
	f2.writelines(statusArr)
	f2.close()
	print("downloaded.txt updated!")


headers = {"User-Agent":"Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11"}

def getPage(url):
	#open URL, with user agent headers

	#urllib requires an HTTP:// prefix
	if 'http' not in url:
		url = "http://" + url

	request = urllib.request.Request(url, headers=headers)
	response = urllib.request.urlopen(request)

	return response.read().decode("utf-8")

def downloadPage(url, filename):
	#download a page (or more accurately, a file) with appropriate user agent headers

	#urllib requires an HTTP:// prefix
	if 'http' not in url:
		url = "http://" + url

	foldername = os.path.dirname(filename)
	if not os.path.exists(foldername):
		os.makedirs(foldername)

	request = urllib.request.Request(url, headers=headers)
	response = urllib.request.urlopen(request)
	with open(filename, 'wb') as out_file:
		shutil.copyfileobj(response, out_file)

print("All done; time to download some BRSTMs!")
try:
	counter=0
	for i in dlrange:
		scmlink = doclines[i][0]
		if scmlink is None:
			continue

		scmlink = scmlink.replace("brawlcustommusic","smashcustommusic") #just in case

		if (("http://" not in scmlink and "https://" not in scmlink) ) and (".com" not in scmlink):
			#assume not a link
			#print("Skipping line "+str(i))
			statusArr[i-dlrange.start+1] = statusArr[i-dlrange.start+1].replace("[ ]","[-]")
			continue

		if("smashcustommusic" not in scmlink):
			print("===error===: Not a smashcustommusic link, so unable to download from line "+str(i)+":  "+scmlink + "; please do so manually.")
			statusArr[i-dlrange.start+1] = statusArr[i-dlrange.start+1].replace("[ ]","[e]")
			continue
			
		#alright, found a link. Time to download!
		if (statusArr[i-dlrange.start+1][0:3] == "[ ]"): #don't redownload if already downloaded

			if doclines[i][4] is None:
				print("===ERROR=== Line "+str(i+1)+" has no team decision! Skipping for now, but come back to this later!")
				continue
			
			#only accept songs that have team decisions of accept or change
			teamdecision = doclines[i][4].strip().lower()
			if not (('accept' in teamdecision) or ('change' in teamdecision)):
				print("Line "+str(i+1)+" had a team decision of '"+teamdecision+"', skipping...")
				statusArr[i-dlrange.start+1] = statusArr[i-dlrange.start+1].replace("[ ]","[r]")
				continue

			print("["+str(i+1)+"]")

			scmnumber = scmlink.split("/")[-1]

			#Scrape the game title from smashcustommusic
			html = getPage(scmlink)
			try:
				gametitle = re.search(gameregex, html).group().split(">")[1]
				songname = re.search(nameregex, html).group().replace("\\'","\'")

				#format to folder title standards
				gametitle = gametitle.replace(":","_").replace("\\'","'")

				#decode unicode (also handles accented es)
				gametitle = unidecode(gametitle)
				songname = unidecode(songname)

				#these characters aren't allowed in windows foldernames
				for badchar in ["*","?","<",">","|",'\\','/','.']:
					gametitle = gametitle.replace(badchar,"")
					songname = songname.replace(badchar,"")

			except Exception as e:
				print("===Error=== Unable to scrape from smashcustommusic for line "+str(i+1) + ": " + str(e))
				continue

			#Download the song!
			print("Downloading "+songname +" from "+gametitle+"...",end="")
			try:
				downloadPage("http://www.smashcustommusic.com/brstm/"+scmnumber, "downloadedsongs/"+gametitle+"/"+songname+".brstm")
			except Exception as e:
				print("===ERROR=== %s" % (e, ))
				continue
			print("Done!")

			#Mark the song as downloaded and save the progress file periodically
			statusArr[i-dlrange.start+1] = statusArr[i-dlrange.start+1].replace("[ ]","[d]")
			counter+=1
			if(counter%10==0):
				counter=0
				updatefile()
	print("\n\n\tAll songs have been downloaded to the 'downloadedsongs' folder! Note that some folder names may need fixing, possibly to match with the music library.\nAlso, please delete downloaded.txt now.")
finally:
	print("Quitting...")
	updatefile()
	input("\n\nPress enter to exit.")
