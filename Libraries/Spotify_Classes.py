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
	def __init__(self,Name,Artist,Album,ReleaseDate,Duration,ID,URI,URL):
		self.Name = Name
		self.Artist = Artist
		self.Album = Album
		self.ReleaseDate = ReleaseDate
		self.Duration = Duration
		self.ID = ID
		self.URI = URI
		self.URL = URL

class album(object):
	def __init__(self,Name,Artist,ReleaseDate,ID,URI,URL):
		self.Name = Name
		self.Artist = Artist
		self.ReleaseDate = ReleaseDate
		self.ID = ID
		self.URI = URI
		self.URL = URL