"""
	Guilherme Batalheiro
	08/06/2021
	Spotify-Youtube-PlayList
	IMPORTED LIBS:
		googleapiclient
        spotipy
"""

from secrets import *
import re
import datetime

import spotipy
from spotipy.oauth2 import SpotifyOAuth

from googleapiclient.discovery import build

youtube = build('youtube', 'v3', developerKey = API_KEY)

spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id = CLIENT_ID,
                                                client_secret = CLIENT_SECRET,
                                                redirect_uri = REDIRECT_URI,
                                                scope = "user-library-read playlist-modify-public playlist-modify-private"))

notFound = []

currentUser = spotify.current_user()

while(True):
    now = datetime.datetime.now()
    currentTimeStr = now.strftime("[%m-%d-%Y %H:%M:%S]")

    # Get the playlist from the YouTube API and save the song titles.
    try:
        playlistYouTube =  youtube.playlistItems().list(part = "snippet", playlistId = PLAYLIST_ID, maxResults = 500)
        tracksNamePlayListYouTube = [ re.sub("[\(\[].*?[\)\]]|Ft. .*|ft. .*", "", musicItem["snippet"]["title"]) for musicItem in playlistYouTube.execute()["items"]]
    except Exception:
        print("Failed to get the playlist from the YouTube API and save the song titles")


    # Gets the playlists from the Spotify API.
    try:
        playlistsSpotify = spotify.current_user_playlists(limit = 50, offset = 0)["items"]
    except Exception:
        print("Failed to gets the playlists from the Spotify API")


    # Check if the YouTube playlist already exists if it doesn't make one.
    try:
        found = 0
        for playlistSpotify in playlistsSpotify:
            if(playlistSpotify["name"] == PLAYLIST_NAME):
                playListSpotifyYouTubeId = playlistSpotify["id"]
                found = 1
                break

        if(not found):
            spotify.user_playlist_create(currentUser["id"], "YouTube")

            playlistsSpotify = spotify.current_user_playlists(limit = 50, offset = 0)["items"]

            for playlistSpotify in playlistsSpotify:
                if(playlistSpotify["name"] == "YouTube"):
                    playListSpotifyYouTubeId = playlistSpotify["id"]
            print(currentTimeStr + " Created YouTube playlist!")
    except Exception:
        print("Failed to check if the YouTube playlist already exists if it doesn't make one")

    # Save the IDs of the songs in the Spotify playlist "YouTube."
    try:
        tracksPlayListSpotify = spotify.user_playlist_tracks(user = currentUser, playlist_id = playListSpotifyYouTubeId, fields = "items", limit=100, offset=0, market=None)
        tracksPlayListSpotifyIds = [ track["track"]["id"] for track in tracksPlayListSpotify["items"]]
    except Exception:
        print("Failed to save the IDs of the songs in the Spotify playlist YouTube.")

    # Look through the YouTube playlist for new songs and add them to the Spotify playlist.
    for trackName in tracksNamePlayListYouTube:
        trackItem = spotify.search(trackName, limit = 1, type = "track", market = None)
        if(not trackItem["tracks"]["items"]):
            if(trackName not in notFound):
                print(currentTimeStr + " Not found track: " + trackName)
                notFound.append(trackName)
        elif(trackItem["tracks"]["items"][0]["id"] not in tracksPlayListSpotifyIds):
            try:
                spotify.user_playlist_add_tracks(user = currentUser, playlist_id = playListSpotifyYouTubeId, tracks = [trackItem["tracks"]["items"][0]["id"]])
            except Exception:
                print("Failed to add song to Spotify")
            
            print(currentTimeStr + " Added track: " + trackName)
