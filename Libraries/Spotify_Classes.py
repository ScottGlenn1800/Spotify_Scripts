#Spotify Classes
class artist(object):
	def __init__(self,Name,Genres,Followers):
		self.Name = Name
		self.Genres = Genres
		self.Followers = Followers

class track(object):
	def _init_(self,Name,Artist,Album,ReleaseDate,Duration):
		self.Name = Name
		self.Artist = Artist
		self.Album = Album
		self.ReleaseDate = ReleaseDate
		self.Duration = Duration