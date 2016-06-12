import sys
if sys.version_info[0] == 2:
		print("""You are using Python 2 instead of Python 3.
This program only works in Python 3 because as of PBR2.0 we're moving to python 3!
""")
		raw_input('\n\nPress enter to exit.') #use raw_input because if we're here, we're in python 2!
		exit()

f = open(input("Metadata filename to analyze:\n>"),"r")
arr = f.readlines()
f.close()

total=0
total_warning=0
total_bet=0
total_break=0
total_leader=0
total_result=0
total_battle=0

def contains(a,b):
  return a.lower().find(b.lower()) != -1

for i in arr:
  total+=1
  if contains(i,"warning"):
    total_warning+=1
  elif contains(i,"betting"):
    total_bet+=1
  elif contains(i,"battle"):
    total_battle+=1
  elif contains(i,"break"):
    total_break+=1
  elif contains(i,"leaderboard"):
    total_leader+=1
  elif contains(i,"result"):
    total_result+=1
  else:
    total-=1

print(str(total) + " total tracks that have metadata in this file.")
print(str(total_bet) + " betting tracks.")
print(str(total_warning) + " warning tracks.")
print(str(total_battle) + " battle tracks.")
print(str(total_break) + " break tracks.")
print(str(total_result) + " result tracks.")
print(str(total_leader) + " leaderboard tracks.")
