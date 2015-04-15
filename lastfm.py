import pylast

# You have to have your own unique two values for API_KEY and API_SECRET
# Obtain yours from http://www.last.fm/api/account for Last.fm
API_KEY = "dcbf56084b47ffbd3cc6755724cb12fa"
API_SECRET = "a970660ef47453134192fa6a9fa6da31"

# In order to perform a write operation you need to authenticate yourself
username = "your_user_name"
password_hash = pylast.md5("your_password")

network = pylast.LastFMNetwork(api_key = API_KEY, api_secret = API_SECRET)

album = network.get_album("Nightwish", "Once")
if album:
	print album
	print album.get_cover_image(2)
