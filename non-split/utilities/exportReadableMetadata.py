import sys
if sys.version_info[0] == 2:
		print("""You are using Python 2 instead of Python 3.
This program only works in Python 3 because as of PBR2.0 we're moving to python 3!
""")
		raw_input('\n\nPress enter to exit.') #use raw_input because if we're here, we're in python 2!
		exit()

print("1hlixed's readable metadata exporter v2.1")
filename = input("Enter the name of the metadata file to make readable:\n>")

f = open(filename,"r")
arr = f.readlines()
f.close()
arr2=[]
for i in arr:
  if i.startswith("        title: "):
    arr2.append(i.replace("        title: ",""))
  if i.startswith("    title: "):
    arr2.append(i.replace("    title: ","==="))

filename2 = input("Enter the filename to save a list of human-readable metadata to:\n(press enter to default to "+filename[0:-4]+"Readable.txt)\n>")
if filename2.strip() == "":
  filename2 = filename[0:-4]+"Readable.txt"

f = open(filename2,"w")
f.writelines(arr2)
f.close()
print("Exported readable metadata to "+filename2+"!")

input("\n\nPress enter to exit")
