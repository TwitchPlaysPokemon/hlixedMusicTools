#py3
#In email client, click the emails from twitch saying "hey here's a new message", right click -> save as them into the /emails directory. This'll go through and append them to each other.

import os
bigstring = ""

directory = "emails"

for filename in os.listdir(directory):
	f =  open(directory+'/'+filename)
	string = f.read()
	f.close()
	
	print(string)

	name = string
	name = name.split('Subject: ')[1]
	name = name.split(" has sent you a message on Twitch")[0]

	if(len(name.split(' class="follower-name"'))>1):
		continue

    
	string = string.replace('=\n','').split('padding:20px;font-size:14px;line-height:1.5" >')[1]
	string = string.split("</div>\n          </div>\n        </td>\n      </tr>\n    </table>\n  </td>\n</tr>\n<!-- Email Content -->")[0]
	#replace HTML

	string = string.replace("<br>","\n").replace("\n\n\n","")
	bigstring += "\n\n\n#####submissions by "+name+":\n"
	bigstring += string


print(bigstring)

bigfilename = "parsedEmails.txt"
f = open(bigfilename,'w')
f.write(bigstring)
f.close()
