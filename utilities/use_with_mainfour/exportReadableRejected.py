import sys
if sys.version_info[0] == 2:
		print("""You are using Python 2 instead of Python 3.
This program only works in Python 3 because as of PBR2.0 we're moving to python 3!
""")
		raw_input('\n\nPress enter to exit.') #use raw_input because if we're here, we're in python 2!
		exit()

print("1hlixed's readable metadata exporter v2.2")
filename = input("Enter the name of the downloaded file to make readable:\n>")

f = open(filename)
arr = f.readlines()
f.close()

arr2 = {}

for i in arr:
	if i[:2] != "[n":
		continue
	if "-" not in i:
		print(i + " didn't have a reason!")
		continue
	reason = i.split("-")[1].split("]")[0].strip()
	game,title,songfile,songtype = "]".join(i.split("]")[1:]).split("|||")
	if game not in arr2:
		arr2[game] = {}
	arr2[game][title] = [title,songtype.strip(),reason.strip()]

arr3=["====REJECTED SUBMISSIONS===="]
for i in arr2:
	arr3.append("==="+i+"\n")
	for j in arr2[i]:
		arr3.append(arr2[i][j][0]+" ("+arr2[i][j][1]+"): "+arr2[i][j][2]+"\n")

filename2 = input("Enter the filename to save a list of human-readable metadata to:\n(press enter to default to "+filename[0:-4]+"RejectedReadable.txt)\n>")
if filename2.strip() == "":
  filename2 = filename[0:-4]+"RejectedReadable.txt"

f = open(filename2,"w")
f.writelines(arr3)
f.close()
print("Exported readable metadata to "+filename2+"!")

input("\n\nPress enter to exit")
