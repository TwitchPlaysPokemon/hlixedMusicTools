This repo contains a collection of music tools to speed up and help with managing TPP metadata. 

###downloadfromxlsx.py

Downloads brstms from smashcustommusic links in a certain range in the music doc. Quite helpful!

# Note: Any program in the non-split folder has not been updated to deal with the new per-game file format. They might still be useful in particular cases, though.
Also, programs with italicized names have not been updated to deal with the "series: " tag either, and may malfunction or break. Try not to use them.

# non-split/Utilities

###analyzeFile.py
Gives a summary of the number of songs of each type in a metadata file. Mostly for curiousity, and to give information about the size of various updates.

###createMetadata.py
A program to help Revo's music-pack-making process. Takes a specific folder configuration and generates a metadata file from it, with user-specified IDs.

###exportReadableMetadata.py
Takes a metadata file and makes a human-readable list of songs in it, sorted by game.

###*fixthings.py*
A program to automatically fix things wrong with metadata files. Mistakes caught include putting "results" instead of "result", song IDs over 50 characters, mismatched quotes, shared song IDs, and more.

###getch.py
A library; don't mind it.

###insertSeries.py
Inserts a user-provided "series:" tag in games without it.

###outputJustResult.py
Outputs just songs of type result (and any other, if you input something different) to analysis.txt.

###*pathBeforeSongs.py*
If there are any games that don't have the 'path:' before the 'songs:' tag, it'll fix it.

###renameFromFileMetadata.py
Some .minigsf songs pulled from various sites are named "song 1", "song 2" and the like, but contain the correct titles in the music file's metadata. This renames the files accordingly.

###splitFile.py
When musicCat is done, use this. Takes a monolithic metadata file and autogenerates the per-folder metadata files for each game, creating and placing them in the appropriate folders.

###verifyAllSongs.py
Very useful. Checker for metadata files to ensure that everything is valid. This ensures that no songs are missing a type, and that every song has a BRSTM file (but only if there's an other/ folder), among other things. If pyYaml is installed, it also runs the file through it and notes any errors. Outputs any errors to analysis.txt

This folder also contains a few old metadata files for testing these programs on.

## Utilities/use_with_mainfour

Utilities to help with the mainfour programs.

###exportReadableRejected.py
Reads from the listeningdownloaded.txt file created by listenToSongs.py and makes a human-readable list of songs that were rejected by that program.

###removeDuplicatesListening.py
Removes duplicate submissions in listeningdownloaded.txt, in case two different people both submitted the same brawlcustommusic URL. Does not scan through a metadata file, though.

## non-split/Utilities/old

Old utilities that are not supported but are here because why not.

##fixids.py

Ensures all song IDs are valid. Kind of outdated, and downloadedToMetadata.py should only generate valid song IDs, but this program exists if you want to use it.

##addMetadata.py

Super old program to add metadata manually for a file. I think this was the first metadata program I made, actually; No error-checking whatsoever, and I think this was made before the "year:" tag was added anyways. Use downloadedToMetadata.py instead. I'm just putting it here in case it's helpful, but seriously, don't use it.

##fixfoldernames.py

Replaces colons in folder names with underscores. If you use downloadedToMetadata.py it does this anyways, so you shouldn't need this at all.
