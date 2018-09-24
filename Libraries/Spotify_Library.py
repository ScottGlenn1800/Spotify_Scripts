#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

def GetTrackFeatures(session,TrackID):
	Features = session.audio_features([TrackID])
	#Index Mapping of Features output (Descriptions Taken from: https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/)

	#0: track_href: A link to the Web API endpoint providing full details of the track.
	#1: analysis_url: An HTTP URL to access the full audio analysis of this track. An access token is required to access this data.
	#2: energy:	Energy is a measure from 0.0 to 1.0 and represents a perceptual measure of intensity and activity. Typically, energetic tracks feel fast, 
	#   loud, and noisy. For example, death metal has high energy, while a Bach prelude scores low on the scale. Perceptual features contributing to this 
	#   attribute include dynamic range, perceived loudness, timbre, onset rate, and general entropy.
	#3: liveness:	Detects the presence of an audience in the recording. Higher liveness values represent an increased probability that the track was 
	#   performed live. A value above 0.8 provides strong likelihood that the track is live.
	#4: tempo: 	The overall estimated tempo of a track in beats per minute (BPM). In musical terminology, tempo is the speed or pace of a given piece 
	#   and derives directly from the average beat duration.
	#5: speechniess: Speechiness detects the presence of spoken words in a track. The more exclusively speech-like the recording (e.g. talk show, 
	#   audio book, poetry), the closer to 1.0 the attribute value. Values above 0.66 describe tracks that are probably made entirely of spoken words. 
	#   Values between 0.33 and 0.66 describe tracks that may contain both music and speech, either in sections or layered, including such cases as rap 
	#   music. Values below 0.33 most likely represent music and other non-speech-like tracks.
	#6: uri: The Spotify URI for the track.
	#7: acoustiness: A confidence measure from 0.0 to 1.0 of whether the track is acoustic. 1.0 represents high confidence the track is acoustic.
	#8: instrumentalness: Predicts whether a track contains no vocals. “Ooh” and “aah” sounds are treated as instrumental in this context. Rap or spoken 
	#   word tracks are clearly “vocal”. The closer the instrumentalness value is to 1.0, the greater likelihood the track contains no vocal content. 
	#   Values above 0.5 are intended to represent instrumental tracks, but confidence is higher as the value approaches 1.0.
	#9: time_signature: An estimated overall time signature of a track. The time signature (meter) is a notational convention to specify how many beats 
	#   are in each bar (or measure).
	#10:danceability: Danceability describes how suitable a track is for dancing based on a combination of musical elements including tempo, rhythm 
	#   stability, beat strength, and overall regularity. A value of 0.0 is least danceable and 1.0 is most danceable.
	#11:key: The key the track is in. Integers map to pitches using standard Pitch Class notation . E.g. 0 = C, 1 = C♯/D♭, 2 = D, and so on.
	#12:duration_ms: The duration of the track in milliseconds.
	#13:loudness: The overall loudness of a track in decibels (dB). Loudness values are averaged across the entire track and are useful for comparing 
	#   relative loudness of tracks. Loudness is the quality of a sound that is the primary psychological correlate of physical strength (amplitude). 
	#   Values typical range between -60 and 0 db.
	#14:valence: A measure from 0.0 to 1.0 describing the musical positiveness conveyed by a track. Tracks with high valence sound more positive (e.g. happy, 
	#   cheerful, euphoric), while tracks with low valence sound more negative (e.g. sad, depressed, angry).
	#15:type: The object type: “audio_features”
	#16:id: The Spotify ID for the track.
	#17:mode: Mode indicates the modality (major or minor) of a track, the type of scale from which its melodic content is derived. Major is represented by 
	#   1 and minor is 0.
	print Features[0]
	features = {}
	features['Energy'] = Features[0]['energy']
	features['Liveness'] = Features[0]['liveness']
	features['Tempo'] = Features[0]['tempo']
	features['Speechiness'] = Features[0]['speechiness']
	features['Acousticness'] = Features[0]['acousticness']
	features['Instrumentalness'] = Features[0]['instrumentalness']
	features['TimeSignature'] = Features[0]['time_signature']
	features['Danceability'] = Features[0]['danceability']
	features['Key'] = Features[0]['key']
	features['Loudness'] = Features[0]['loudness']
	features['Valence'] = Features[0]['valence']
	features['Mode'] = Features[0]['mode']
	return features

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
				Features = GetTrackFeatures(session,ID)
				Track = track(Name,Artist,Album,ReleaseDate,Duration,ID,URI,URL,
					          Features['Energy'],Features['Liveness'],Features['Tempo'],
					          Features['Speechiness'],Features['Acousticness'],Features['Instrumentalness'],
					          Features['TimeSignature'],Features['Danceability'],Features['Key'],
					          Features['Loudness'],Features['Valence'],Features['Mode'])
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