""" This module contains two applescript blocks - one to build a playlist
in iTunes containing one album from one artist, and a second to play that
playlist. These are passed to the terminal by the "playAlbum" function,
which also specifies the playlist, album, and artist names"""

import os

# OSA Script template to make iTunes build a playlist
create_playlist = """osascript<<END
tell application "iTunes"
    if (exists playlist "%s") then
        delete playlist "%s"
    end if
    set name of (make new playlist) to "%s"
    set theseTracks to every track of playlist "Library" whose album is "%s"
    repeat with thisTrack in theseTracks
        if artist of thisTrack is "%s" then
            duplicate thisTrack to playlist "%s"
        end if
    end repeat
end tell
END"""

# OSA Script template to make iTunes play a playlist
play = """osascript<<END
tell application "iTunes"
play playlist "%s"
end tell
END"""

def playAlbum(playlist,album,artist):
    os.system(create_playlist % (playlist, playlist, playlist, album, artist, playlist))
    os.system(play % playlist)
