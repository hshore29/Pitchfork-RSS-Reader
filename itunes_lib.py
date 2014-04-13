""" This is a class object which reads and stores the contents of your
iTunes Library.xml file, for future use. Several methods are included
which provide useful functionality (finding tracks, albums, etc.)"""

import os, plistlib

""" The iTunes library xml file contains a list of track dictionaries.
For each track, if an attribute is unset, it is omitted from the
dictionary. iTunesTrack is a class that has a default track dictionary,
and a method to process a raw track dictionary so that any unset attributes
are blank rather than absent (this is necessary to avoid key errors)"""

class iTunesTrack():
    # Default dictionary
    template = {'Bit Rate':'', 'Track Count':0, 'Genre':'', 'Skip Count':0,
                'Size':'', 'Album Rating Computed':'', 'Play Date':'',
                'Skip Date':'', 'File Folder Count':'', 'Play Date UTC':'',
                'Play Count':0, 'Disc Count':0, 'Artist':'', 'Track ID':'',
                'Comments':'', 'Date Added':'', 'Track Type':'', 'Total Time':'',
                'Location':'', 'Date Modified':'', 'Library Folder Count':'',
                'Track Number':0, 'Disc Number':0, 'Album Rating':'',
                'Rating':'', 'Name':'', 'Persistent ID':'', 'Sample Rate':'',
                'Album':'', 'Artwork Count':'', 'Grouping':'', 'Year':'',
                'Kind':'', 'Composer':'', 'Sort Album':'', 'Sort Artist':'',
                'File Type':'', 'Series':'', 'BPM':'', 'Episode':'',
                'Compilation':'', 'Sort Composer':'', 'Sort Name':'',
                'Album Artist':'', 'Release Date':'', 'Purchased':'',
                'Part Of Gapless Album':'', 'Sort Album Artist':'', 'Unplayed':'',
                'Podcast':'', 'Stop Time':'', 'Volume Adjustment':'',
                'Rating Computed':'', 'Protected':'', 'Disabled':'',
                'Start Time':'', 'Movie':'', 'Has Video':'', 'HD':'',
                'Video Height':'', 'Video Width':'', 'Explicit':''}

    # Takes raw track dict, returns dict with complete attributes
    def processTrack(self,rawTrack):
        outTrack = self.template.copy()
        for key in rawTrack:
            try:
                outTrack[key] = rawTrack[key]
            except:
                print("Missing key: " + key)
        return outTrack

""" The iTunesLib class processes a specified xml file as your iTunes library,
and stores the track structure for future reference."""

class iTunesLib():
    def __init__(self, libraryPath):
        # Load iTunes library file
        libraryFile = open(os.path.expanduser(libraryPath),'rb')
        self.libraryData = plistlib.load(libraryFile)
        libraryFile.close()
        self.tracks = dict()
        self.loadTracks()
        self.playlists = self.libraryData['Playlists']

    def getDictKeys(self):
        # Returns a list of all possible track keys
        keys = []
        for trackID, trackData in libraryData['Tracks'].items():
            for key in trackData.keys():
                if key in keys:
                    pass
                else:
                    keys.append(key)
        return keys

    def loadTracks(self):
        # Load tracks from raw data into track dictionary
        for trackID, trackData in self.libraryData['Tracks'].items():
            track = dict()
            track = iTunesTrack().processTrack(trackData)
            self.tracks[trackID] = track

    def findTrack(self, trackName):
        # Iterate through tracks, return ID if matched, otherwise 0
        for trackID, trackData in self.tracks.items():
            if trackData['Name'] == trackName:
                return trackID
        return 0

    def getTrack(self,trackID):
        # Return the track dictionary for a specified trackID
        return self.tracks[trackID]

    def getAlbumTracks(self, album, artist):
        # Iterate through tracks, return list of tracks
        trackList = []
        for trackID, trackData in self.tracks.items():
            if (trackData['Artist'].lower() == artist.lower()) and (trackData['Album'].lower() == album.lower()):
                trackList.append(trackID)
        return trackList

    def getAlbumStatus(self, track_ids):
        # Return zero for no album, 1 for partial album, 2 for complete album
        status = 0
        if len(track_ids) > 0:
            first_id = track_ids[0]
            first_track = self.getTrack(first_id)
            track_count = first_track['Track Count']
            if (len(track_ids) >= int(track_count)) and (track_count > 0):
                status = 2
            else:
                status = 1
        return status
