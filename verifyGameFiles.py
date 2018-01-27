#Edit these to point to the metadata repo and the music-file repo, respectively. Don't put slashes at the ends!
metadata_library_path = "" 
musicfiles_library_path = ""

print("1hlixed's metadata file verifier v4.2")

#standard modules
import re
import os
import sys
import logging
from collections import namedtuple

#pip3 dependencies
import yaml

if sys.version_info[0] == 2:
		print("""You are using Python 2 instead of Python 3.\nThis program only works in Python 3.""")
		raw_input('\n\nPress enter to exit.') #use raw_input because if we're here, we're in python 2!
		exit()

if metadata_library_path == "" or musicfiles_library_path == "":
	print("To use this program, please open up this up in a text editor and specify the locations of your metadata and music file repository folders in the strings at the top.")
	input('\n\nPress enter to exit.') 
	exit()


Song = namedtuple("Song", ("id", "title", "path", "types", "game", "fullpath", "ends", "tags"))
Game = namedtuple("Game", ("id", "title", "platform", "year", "series","is_fanwork"))


#Tests:
#	song missing a required tag
#	game missing a required tag
#	song type in valid_song_types
#	duplicate game ID
#	duplicate song id
#	song ids are lowercase
#	song ids are <50 chars
#	if brstmcheckoption is enabled, and not os.path.isfile(gamepath+"/"+songpath)
#	ensure game has a songs tag
#	check that a game isn't indented like a song and a song isn't indented like a game
#	end-of-line comments should have spaces before them
log = logging.getLogger("verifier")

songlist = {}
valid_song_types = ['betting', 'battle', 'result', 'warning', 'break']

def import_metadata(metafilename):
	"""Import metadata given a metadata filename. Assumed to be one game per metadata file."""
	with open(metafilename, encoding="utf-8") as metafile:
		try:
			gamedata = yaml.load(metafile)
		except UnicodeDecodeError:
			print(metafilename + " is not UTF-8!")
	path = os.path.dirname(metafilename)
	newsongs = {}

	songs = gamedata.pop("songs")

	#the series and is_fanwork tags are optional
	if 'series' not in gamedata:
		gamedata['series'] = None
	if 'is_fanwork' not in gamedata:
		gamedata['is_fanwork'] = None

	#Create the game info, which will cause an error if not all required tags are present
	game = Game(**gamedata)

	#before proceeding, test to ensure that is_fanwork is a boolean
	if game.is_fanwork is not None:
		if type(game.is_fanwork) != bool:
			log.error("Gameid {} has an 'is_fanwork' tag that is {} instead of a boolean value (true/false).",
						  game.id, game.is_fanwork)
	#now, test each song in the game
	for song in songs:
		song["fullpath"] = os.path.join(path, song["path"])
		song["game"] = game

		# convert single type to a stored list
		if "type" in song:
			song["types"] = [song.pop("type")]

		#if no ends provided, say so explicitly
		if "ends" not in song:
			song["ends"] = None
		if "tags" not in song:
			song["tags"] = None
		#convert single end time to list
		elif (type(song["ends"]) == int) or (type(song["ends"]) == float):
			song["ends"] = [song["ends"]]

		#create the song
		#Any missing tags will cause an error here
		newsong = Song(**song)

		#Now, test for duplicates
		#is the current song ID present in a different game?
		if newsong.id in songlist:
			log.error("Songid conflict! %s exists twice, once in %s and once in %s!",
						  newsong.id, songlist[newsong.id].game.title, game.title)
		#is the current song ID present twice in THIS game?
		if newsong.id in newsongs:
			log.error("Songid conflict! %s exists twice in the same game, %s.",
						  newsong.id, game.id)

		#Ensure the song has a BRSTM file
		actual_songfile_path = newsong.fullpath.replace(metadata_library_path, musicfiles_library_path)
		if not os.path.isfile(actual_songfile_path):
			log.error("Songid %s doesn't have a BRSTM file at %s!",
					   newsong.id, actual_songfile_path)

		#if an ends tag is present but it's a small number, complain since the user probably entered in minutes and not seconds
		if newsong.ends != None:
			if type(20) is not list:
				newsong.ends = [newsong.ends]
			for endtime in newsong.ends:
				if endtime < 10:
					log.warn("Songid {} has an end of {}, which seems fishy (end times are in seconds, not minutes; Did you mean to put {}?)".format(newsong.id, endtime, int(endtime*60)))

		#ensure the song is a valid type
		for thetype in newsong.types:
			if thetype not in valid_song_types:
				log.error("Songid %s has an invalid type %s!",
					   newsong.id, thetype)

		#add to song list!
		songlist[newsong.id] = newsong


#begin
for root, _, files in os.walk(metadata_library_path):
	for filename in files:
		if filename.endswith(".yaml"):
			metafilename = os.path.join(root, filename)
			import_metadata(metafilename)
if len(songlist) == 0:
	log.warn("No metadata found! (Current music library location: {} )".format(metadata_library_path))

input("\n\nPress enter to exit.")
