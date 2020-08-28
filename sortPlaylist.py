import spotipy
import spotipy.util as util
import spotipy.client as client
from spotipy.oauth2 import SpotifyClientCredentials
from pprint import pprint

username = "" # Enter username
client_secret = "" # Enter Spotify API Client secret
client_id = "" # Enter Spotify API Client ID
redirect_uri = "http://localhost:8888/callback/"

class SpotifySort():
    def __init__(self):
        # Get an API token from Spotify
        token = util.prompt_for_user_token(username, "playlist-modify-private", client_id, client_secret, redirect_uri)

        client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
        self.sp = spotipy.Spotify(auth=token, client_credentials_manager=client_credentials_manager)

    def SortPlaylistFromTo(self, sourceId, targetID):
        playlistData = []

        index = 0
        while True:
            # Get the tracks, the Spotify API has a limit on 100 songs that you can get in one API call
            tracks = self.sp.user_playlist_tracks(playlist_id=sourceId, limit=100, offset=index)
            if (len(tracks['items']) == 0):
                break

            for track in list(tracks['items']):
                if (track['track'] == None): #Filter anything that isn't a track, like a podcast
                    continue

                trackName = track['track']['name']
                trackID = track['track']['id']

                mainArtistID = track['track']['artists'][0]['id']
                mainArtist = track['track']['artists'][0]['name']

                artist = self.sp.artist(mainArtistID)
                artistGenres = artist['genres']
                if (len(artistGenres) == 0):
                    playlistData.append([trackName, mainArtist, trackID, ""])
                else:
                    playlistData.append([trackName, mainArtist, trackID, artistGenres[0]])

            index += 100
            
        sortedPlaylist = sorted(playlistData, key=lambda sl: (sl[3], sl[2], sl[1]))

        genresFLow = []

        for item in sortedPlaylist:
            if (item[3] not in genresFLow):
                genresFLow.append(item[3])
        
        # Print the genres in which the playlist in sorted in
        pprint(genresFLow)

        sortedPlaylistTrackIDsOnly = [item[2] for item in sortedPlaylist]
        
        # Loop the length of the playlist and send 100 songs to the new playlist. The Spotify API has a limit of 100 songs that you can add in one API call
        for i in range(0, int(len(sortedPlaylistTrackIDsOnly) / 100) + 1):
            self.sp.user_playlist_add_tracks(user=username, playlist_id=targetID, tracks=sortedPlaylistTrackIDsOnly[i * 100:i * 100 + 100])

if __name__ == "__main__":
    spotifySort = SpotifySort()
    spotifySort.SortPlaylistFromTo('''The playlist to sort''', '''The (empty) playlist to put the songs into''')
