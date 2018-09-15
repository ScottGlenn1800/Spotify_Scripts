import spotipy,os
import spotipy.util as util


username = "12186403842"
SPOTIFY_CLIENT_ID = "68ee9cc4856c4bbd877fa851b8ea4905"
SPOTIFY_CLIENT_SECRET = "03089f17b7ac4de0b32391052d3d6789"
SPOTIFY_REDIRECT_URL = "http://localhost:8888/callback"
try:
	token = util.prompt_for_user_token(username,client_id=SPOTIFY_CLIENT_ID,client_secret=SPOTIFY_CLIENT_SECRET,redirect_uri=SPOTIFY_REDIRECT_URL)
except AttributeError:
	os.remove(".cache-12186403842")
	token = util.prompt_for_user_token(username,client_id=SPOTIFY_CLIENT_ID,client_secret=SPOTIFY_CLIENT_SECRET,redirect_uri=SPOTIFY_REDIRECT_URL)

spotify = spotipy.Spotify(auth=token)
results = spotify.search(q="artist:" + "Dayshell",type="artist")
print results