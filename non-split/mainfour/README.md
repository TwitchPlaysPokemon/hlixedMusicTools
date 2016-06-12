# Mainfour

These programs were used before impeachment to speed up the processing of user metadata suggestions, put here in case anyone finds them useful. The workflow was:

* Use *parseEmails.py* to convert twitch emails to a suggestions.txt file

* file->replace "\n" to "\n[ ]"

* run *download.py* to automatically download every BRSTM from every brawlcustommusic URL from suggestions.txt, replacing the "[ ]" with a "[d]" to indicate progress

* use *listenToSongs.py* to go through the list and accept/reject with [#] or [n - <reason>]

* finally, run *downloadedToMetadata.py* to convert that list to a metadata_justNew.txt file, and then merge that with the newest version manually

* optionally, run utilities/exportReadableMetadata.py to make a nice list of new songs and the other one to make a list of rejected songs

getch.py is a library used by listenToSongs.py.
