#Spotify Classes
class artist(object):
	def __init__(self,Name,Genres,Followers,ID,URI,URL):
		self.Name = Name
		self.Genres = Genres
		self.Followers = Followers
		self.ID = ID
		self.URI = URI
		self.URL = URL

class track(object):
	def __init__(self,Name,Artist,Album,ReleaseDate,Duration,
				 ID,URI,URL,Energy,Liveness,Tempo,Speechiness,
				 Acousticness,Instrumentalness,TimeSignature,
				 Danceability,Key,Loudness,Valence,Mode):
		self.Name = Name
		self.Artist = Artist
		self.Album = Album
		self.ReleaseDate = ReleaseDate
		self.Duration = Duration
		self.ID = ID
		self.URI = URI
		self.URL = URL
		self.Energy = Energy
		self.Liveness = Liveness
		self.Tempo = Tempo
		self.Speechiness = Speechiness
		self.Acousticness = Acousticness
		self.Instrumentalness = Instrumentalness
		self.TimeSignature = TimeSignature
		self.Danceability = Danceability
		self.Key = Key
		self.Loudness = Loudness
		self.Valence = Valence
		self.Mode = Mode

class album(object):
	def __init__(self,Name,Artist,ReleaseDate,ID,URI,URL):
		self.Name = Name
		self.Artist = Artist
		self.ReleaseDate = ReleaseDate
		self.ID = ID
		self.URI = URI
		self.URL = URL