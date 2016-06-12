import string

print("1hlixed's path fixer v1.0")

name = raw_input("Metadata file name>")
f=None
try:
  f = open(name)
except:
  print("Invalid file name!")
  raw_input("\n\nPress enter to exit.")
  quit()
arr = f.readlines()
f.close()
def updateFile():
  f = open(name+".fixed","w")
  f.writelines(arr)
  f.close()

  print("\n\nA copy of "+name+" has been saved to "+name+".fixed with these changes made.\nYou'll need to rename the folders yourself, though.")
  raw_input("\n\nPress enter to exit.")


for i in range(len(arr)):
  line = arr[i]
  if line.startswith("    path: "):
    prefix = "    path: "
    currName = line.replace("    path: ","").strip()
    if currName != currName.replace(":","_"):
      arr[i] = prefix + currName.replace(":","_") + "\n"
      print(currName+" changed to "+currName.replace(":","_"))
  if line.startswith("        path: "):
    prefix = "        path: "
    currName = line.replace(prefix,"").strip()
    if currName != currName.replace(":","_"):
      arr[i] = prefix + currName.replace(":","_") + "\n"
      print(currName+" changed to "+currName.replace(":","_"))
updateFile()
