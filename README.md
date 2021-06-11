# Spotify-YouTube-PlayList
A small Python script that detects if you add a new song to a certain YouTube playlist and, if it exists, adds it to a specific Spotify playlist.

## Installation
1) Install All Dependencies.    
`pip install -r requirements.txt`
2) Collect the youtube playlist id that's in the URL and add it to the secret.py.    
Example:     
`https://m.youtube.com/playlist?list=PLMC9KNkIncKtPzgY-5rmhvj7fax8fdxoj`.   
PLAYLIST_ID = "PLMC9KNkIncKtPzgY-5rmhvj7fax8fdxoj"
3) Get a Google API key explained [here](https://www.google.com/url?sa=t&source=web&rct=j&url=https://developers.google.com/youtube/v3/getting-started&ved=2ahUKEwjluLW-sY7xAhW2AWMBHU-JCS0QFjAAegQIEBAC&usg=AOvVaw3ueucBVp-4rmSh_si8y-vP&cshid=1623373487113) and add it to the secret.py.
4) Create a simple server-side application [here](https://developer.spotify.com/documentation/web-api/quick-start/) and get the Spotify client id and the client secret and add it to the secret.py.    

Note: You can change the Spotify playlist name ("YouTube" by default) and the redirect URL ("htt<span>p://localhost/" by default).

## Usage
```
python spotify-youtube-playlist.py
```
If it is the first time running the script, log into your Spotify account in the new browser window that popped up.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)

