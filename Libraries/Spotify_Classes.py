#Spotify Classes
class artist(object):
	def __init__(self,Name,Genres,Followers):
		self.Name = Name
		self.Genres = Genres
		self.Followers = Followers

class track(object):
	def __init__(self,Name,Artist,Album,ReleaseDate,Duration):
		self.Name = Name
		self.Artist = Artist
		self.Album = Album
		self.ReleaseDate = ReleaseDate
		self.Duration = Duration

class album(object):
	def __init__(self,Name,Artist,ReleaseDate):
		self.Name = Name
		self.Artist = Artist
		self.ReleaseDate = ReleaseDate