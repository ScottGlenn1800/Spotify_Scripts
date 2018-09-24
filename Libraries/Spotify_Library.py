import spotipy,os,sys
import spotipy.util as util
from optparse import OptionParser
sys.path.append("C:/CODE/Spotify_Scripts/Libraries")
from Spotify_Classes import *

def ParseArgs():
	"""Parses the Arguments the user sends on the command line.
	
	No parameters needed

	Options:
		-A Artist

	Returns the arguments
	"""
	parser = OptionParser()
	parser.add_option("-A","--Artist",dest="artist",
					 help="The name of the artist",metavar="ARTIST")
	(Arguments,args) = parser.parse_args()
	if Arguments.artist==None:
		print"ERROR! Artist not defined! See --help for more details"
		sys.exit()
	return Arguments

def CreateSpotifySession():
	""" Attempts to get a token using the username and the application credentials. 
	These Credentials are defaulted for now.

	No parameters needed.

	Returns a spotipy spotify session
	"""
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
	"""Retrieves information about Artist name that is passed to 
	the function.

	Parameters:
		- session - Spotipy spotify object created in CreateSpotifySession.
		- Artist - The name of the Artist the function should query.

	Returns an artist object
	"""
	ArtistData=None
	OUTPUT = session.search(q="artist:" + "%s"%(Artist),type="artist")
	if OUTPUT["artists"]["items"]==[]:	#if the Artist name is not on spotify, this array will return back as empty.
		print"ERROR! No results for %s found on Spotify!"%(Artist)
		#sys.exit()
	for a in OUTPUT['artists']['items']:
		if a['name'] == Artist:
			Name = a["name"]
			Genres = a["genres"] #This is a list of the Genres that the band is associated with
			Followers = a["followers"]["total"] #This is a list of the amount of followers the band has on Spotify
			ID = a['id']
			URI = a['uri']
			URL = a['external_urls']['spotify']
			ArtistData = artist(Name,Genres,Followers,ID,URI,URL)
	if ArtistData == None:
		print "Error! Results found with %s in the name but no exact matches"%(Artist)
		print'\n'
		for a in OUTPUT['artists']['items']:
			print a['name'].encode('utf8')
			print a['genres']
		#sys.exit()
	else:
		return ArtistData
	
def GetAlbumData(session,Album,Artist):
	"""Retrieves information about Album name that is passed to 
	the function.

	Parameters:
		- session - Spotipy spotify object created in CreateSpotifySession.
		- Album - The name of the Album the function should query
		- Artist - The artist object on the artist that created the album,
				   passed from GetArtistData

	Returns album object
	"""
	OUTPUT = session.search(q="album:" + "%s"%(Album),type="album")
	if OUTPUT["albums"]["items"]==[]:	#if the Tracks name is not on spotify, this array will return back as empty.
		print"ERROR! Album not found on Spotify!"
		#sys.exit()
	for a in OUTPUT['albums']['items']:
		if a['name'] == Album:
			if a['artists'][0]['name'] == Artist.Name:
				print"Album %s found for Artist %s"%(Album,Artist.Name)
				Name = a["name"]
				Artist = a["artists"][0]["name"]
				ReleaseDate = a["release_date"]
				ID = a['id']
				URI = a['uri']
				URL = a['external_urls']['spotify']
				Album = album(Name,Artist,ReleaseDate,ID,URI,URL)
				return Album
	print"Error! Album %s not found"%(Album)

def GetTrackData(session,Track,Artist):
	"""Retrieves information about a Track name that is passed
	to the function.

	Parameters:
		- session - Spotipy spotify object created in CreateSpotifySession.
		- Track - The name of the Track the function should query
		- Artist - The artist object of the artist that created the Track,
				   passed from GetArtistData

	Returns track object
	"""
	OUTPUT = session.search(q="track:" + "%s"%(Track),type="track",limit=50)
	if OUTPUT["tracks"]["items"]==[]:	#if the Tracks name is not on spotify, this array will return back as empty.
		print"ERROR! Track name not found on Spotify!"
		#sys.exit()
	for t in OUTPUT['tracks']['items']:
		if t['name'] == Track:
			if t['artists'][0]['name'] == Artist.Name:
				print"Track %s found for Artist %s"%(Track,Artist.Name)
				Album = t["album"]['name']
				ReleaseDate = t["album"]['release_date']
				Artist = t["album"]['artists'][0]['name']
				Name = t['name']
				Duration = t['duration_ms']
				ID = t['id']
				URI = t['uri']
				URL = t['external_urls']['spotify']
				Track = track(Name,Artist,Album,ReleaseDate,Duration,ID,URI,URL)
				return Track
	print"ERROR! Track %s by %s not found"%(Track,Artist.Name)

def GetTopTracks(session,Artist):
	"""Gets the top 10 tracks of the artist passed.passed back an array of Track objects.

	Parameters
		- session - Spotipy spotify object created in CreateSpotifySession.
		- Artist - The artist object of the artist that created the Track,
				   passed from GetArtistData

	Returns list of Track objects.
	"""
	OUTPUT = session.artist_top_tracks(Artist.ID)
	TopTracks = []
	for t in OUTPUT['tracks']:
		Track = GetTrackData(session,t['name'],Artist)
		TopTracks.append(Track)
	return TopTracks

def GetRelatedArtists(session,Artist):
	"""Gets the 10 most related artists to teh artist that is passed to the function.
	Parameters
		- session - Spotipy spotify object created in CreateSpotifySession.
		- Artist - The artist object of the artist that created the Track,
				   passed from GetArtistData

	Returns list of Artist objects.
	"""
	OUTPUT = session.artist_related_artists(Artist.ID)
	RelatedArtists = []
	for a in OUTPUT['artists']:
		Artist = GetArtistData(session,a['name'])
		RelatedArtists.append(Artist)
	return RelatedArtists

def GetArtistAlbums(session,Artist):
	"""
	"""
	OUTPUT = session.artist_albums(Artist.ID)
	Albums = []
	for a in OUTPUT['items']:
		Skip = False
		Album = GetAlbumData(session,a['name'],Artist)
		if Album==None:
			continue
		for a in Albums:
			if a.ID == Album.ID:
				print"Skipping Duplicate Album: %s"%(Album.Name)
				Skip = True
		if Album==None or Skip==True:
			continue
		Albums.append(Album)
	return Albums

def GetAlbumTracks(session,Album,Artist):
	"""
	"""
	OUTPUT = session.album_tracks(Album.ID)
	Tracks = []
	for t in OUTPUT['items']:
		Track = GetTrackData(session,t['name'],Artist)
		if Track == None:
			continue
		Tracks.append(Track)
	return Tracks

def GetArtistTracks(session,Artist):
	All_Tracks = []
	Albums = GetArtistAlbums(session,Artist)
	for album in Albums:
		Tracks = GetAlbumTracks(session,album,Artist)
		for t in Tracks:
			All_Tracks.append(t)
	return All_Tracks


def main(): #This is for debugging the Library
	Arguments = ParseArgs()
	session = CreateSpotifySession()
	Artist = GetArtistData(session,Arguments.artist)
	print Artist.Name
	print Artist.Genres
	print Artist.Followers







#main()