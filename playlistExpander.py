import spotipy
import spotipy.util as util
from tqdm import tqdm

SPOTIFY_USERNAME = "oxa11ce"
SPOTIFY_SCOPE = "playlist-read-private playlist-modify-private playlist-modify-public"

token = util.prompt_for_user_token(SPOTIFY_USERNAME, SPOTIFY_SCOPE)
sp = spotipy.Spotify(token)


def main():
    origPlaylist = input("Enter playlist URI: ")
    #origPlaylist = "spotify:playlist:2GGTebqmfqLkURZpUdtLy4"
    playlistName = sp.user_playlist(user=None,
                                    playlist_id=origPlaylist,
                                    fields="name")["name"]
    origTracks = tracksInPlaylist(SPOTIFY_USERNAME, origPlaylist)
    albums = albumsOfTracks(origTracks)
    newTracks = tracksOfAlbums(albums)

    newPl = sp.user_playlist_create(SPOTIFY_USERNAME,
                                    playlistName + " - expanded")['uri']

    for i in tqdm(range(0, len(newTracks), 100)):
        sp.user_playlist_add_tracks(SPOTIFY_USERNAME, newPl,
                                    newTracks[i:i + 100])


def albumsOfTracks(tracks):
    return list(
        dict.fromkeys([track['track']['album']['uri'] for track in tracks]))


def tracksOfAlbums(albums):
    tracks = []
    for cAlbum in tqdm(albums):
        for track in sp.album(cAlbum)['tracks']['items']:
            tracks.append(track['uri'])
    return tracks


def tracksInPlaylist(user, playlist):
    #spotify only gives 100 at a time, thanks ackleyrc
    batch = sp.user_playlist_tracks(user, playlist)
    tracks = batch['items']
    while batch['next']:
        batch = sp.next(batch)
        tracks.extend(batch['items'])
    return tracks


if __name__ == "__main__":
    main()
