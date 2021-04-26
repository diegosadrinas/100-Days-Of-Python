import requests
from bs4 import BeautifulSoup
import spotipy
from decouple import config

# environment variables
SPOTIPY_CLIENT_ID = config("ID")
SPOTIPY_CLIENT_SECRET = config("SECRET")
SPOTIPY_REDIRECT_URI = config("URI")
SPOTIPY_AUTH_TOKEN = config("AUTH_TOKEN")


# spotify access
spotify_access = spotipy.oauth2.SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET,
                                             redirect_uri=SPOTIPY_REDIRECT_URI, scope="playlist-modify-private")
client = spotipy.client.Spotify(oauth_manager=spotify_access)
user_id = client.current_user()["id"]
sp = spotipy.Spotify(auth_manager=spotify_access)

user_input = input("Which date would you like to check the TOP 100 BILLBOARD list? (enter YYYY-MM-DD): ")
response = requests.get(url=f"https://www.billboard.com/charts/hot-100/{user_input}")
billboard_webpage = response.text
soup = BeautifulSoup(billboard_webpage, "html.parser")
ranking_number = soup.find_all(class_="chart-element__rank__number")
song_titles = soup.find_all(class_="chart-element__information__song text--truncate color--primary")
song_titles_list = [title.getText() for title in song_titles]

# list of track URIs
uri_list = []
year = user_input.split("-")[0]
for song in song_titles_list:
    results = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri_list.append(results["tracks"]["items"][0]["uri"])
    except IndexError:
        print(f"Song: {song} couldn't be find in spotify. Skipped.")

# create the playlist
playlist = client.user_playlist_create(user=user_id, name=f"Top 100 Billboard for {user_input}", public=False)

# add tracks to playlist
for song in uri_list:
    client.playlist_add_items(playlist_id=playlist["id"], items=uri_list)
