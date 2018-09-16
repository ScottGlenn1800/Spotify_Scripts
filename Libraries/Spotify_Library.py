import spotipy,os,sys
import spotipy.util as util
from optparse import OptionParser
sys.path.append("C:/CODE/Spotify_Scripts/Libraries")
from Spotify_Classes import *

def ParseArgs():
	parser = OptionParser()
	parser.add_option("-A","--Artist",dest="artist",
					 help="The name of the artist",metavar="ARTIST")
	(Arguments,args) = parser.parse_args()
	if Arguments.artist==None:
		print"ERROR! Artist not defined! See --help for more details"
		sys.exit()
	return Arguments

def CreateSpotifySession():
	username = "12186403842"
	#These are the Spotify App credentials for Music_Recommender App registered on Spotify
	SPOTIFY_CLIENT_ID = "68ee9cc4856c4bbd877fa851b8ea4905"
	SPOTIFY_CLIENT_SECRET = "03089f17b7ac4de0b32391052d3d6789"
	SPOTIFY_REDIRECT_URL = "http://localhost:8888/callback"
	try:
		token = util.prompt_for_user_token(username,client_id=SPOTIFY_CLIENT_ID,client_secret=SPOTIFY_CLIENT_SECRET,redirect_uri=SPOTIFY_REDIRECT_URL)
	except AttributeError:
		os.remove(".cache-%s"%(username)) #removing the existing username from cache in case its lingering
		token = util.prompt_for_user_token(username,client_id=SPOTIFY_CLIENT_ID,client_secret=SPOTIFY_CLIENT_SECRET,redirect_uri=SPOTIFY_REDIRECT_URL)
	return spotipy.Spotify(auth=token)

def GetArtistData(session,Artist):
	OUTPUT = session.search(q="artist:" + "%s"%(Artist),type="artist")
	if OUTPUT["artists"]["items"]==[]:	#if the Artist name is not on spotify, this array will return back as empty.
		print"ERROR! Artist not found on Spotify!"
		sys.exit()
	Name = OUTPUT["artists"]["items"][0]["name"]
	Genres = OUTPUT["artists"]["items"][0]["genres"] #This is a list of the Genres that the band is associated with
	Followers = OUTPUT["artists"]["items"][0]["followers"]["total"] #This is a list of the amount of followers the band has on Spotify
	Artist = artist(Name,Genres,Followers)
	return Artist
	
def GetTrackData(session,Track):
	OUTPUT = session.search(q="track:" + "%s"%(Track),type="track")
	if OUTPUT["tracks"]["items"]==[]:	#if the Tracks name is not on spotify, this array will return back as empty.
		print"ERROR! Track name not found on Spotify!"
		sys.exit()
	Album = OUTPUT["tracks"]["items"][0]["album"]['name']
	ReleaseDate = OUTPUT["tracks"]["items"][0]["album"]['release_date']
	Artist = OUTPUT["tracks"]["items"][0]["album"]['artists'][0]['name']
	Name = OUTPUT["tracks"]["items"][0]['name']
	Duration = OUTPUT["tracks"]["items"][0]['duration_ms']
	return track(Name,Artist,Album,ReleaseDate,Duration)


def main(): #This is for debugging the Library
	Arguments = ParseArgs()
	session = CreateSpotifySession()
	Artist = GetArtistData(session,Arguments.artist)
	print Artist.Name
	print Artist.Genres
	print Artist.Followers







#main()