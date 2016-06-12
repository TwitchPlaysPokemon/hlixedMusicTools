import sys
if sys.version_info[0] == 2:
		print("""You are using Python 2 instead of Python 3.
This program only works in Python 3 because as of PBR2.0 we're moving to python 3!
""")
		raw_input('\n\nPress enter to exit.') #use raw_input because if we're here, we're in python 2!
		exit()

print("1hlixed's metadata file path-before-songs-inator v1.0")
print("Ensures the path: part comes right before the songs: part of a metadata file")

metafilename = input("Enter a metadata filename\n>")
f2 = open(metafilename)
arr = f2.readlines()
f2.close()

for i in range(len(arr)):
	if arr[i].startswith("    songs: "):
		if not arr[i-1].startswith("    path: "):
			for j in range(5):
				if arr[i-j-2].startswith("    path: "):
					#swap arr[i-j] and arr[i]
					print("Found "+arr[i-1]+"in place of path!")
					#swap lines
					tmp = arr[i-1]
					arr[i-1] = arr[i-j-2]
					arr[i-j-2] = tmp
					break
		



f = open(metafilename,'w')
f.writelines(arr)
f.close()

input("Done! \n\nPress enter to exit.")
