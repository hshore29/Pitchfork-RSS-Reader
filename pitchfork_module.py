""" This is a module to parse the Pitchfork Best New Albums RSS feed, and
store the contents of that feed in a dictionary object which can be saved
locally as a plist file. It contains three methods and a class:
    -pfkLib is a class that stores / writes the review list
    -getBestAlbums returns the last n reviews from the RSS feed
    -getScore uses BeautifulSoup to find the score on the actual review page
    -scoreClass is used by BeautifulSoup to find the score's <div>"""

import feedparser, urllib, os, plistlib
from time import mktime
from datetime import datetime
from bs4 import BeautifulSoup
from itunes_lib import iTunesLib

def scoreClass(tag):
    if tag.has_attr('class'):
        return tag['class'][0].split(' ')[0] == 'score'
    else:
        return False

def getScore(url):
    review_page=urllib.request.urlopen(url)
    soup=BeautifulSoup(review_page.read())
    span=str(soup.findAll(scoreClass)[0])
    return float(BeautifulSoup(span).text.strip() or 0)

def getBestAlbums(num):
    feed=feedparser.parse('feed://pitchfork.com/rss/reviews/best/albums/')
    length=len(feed['entries'])
    albums = dict()

    if num > length:
        num=length
    
    for x in range(0,num):
        review=feed['entries'][x]
        album=dict()
        score=getScore(review['link'])
        review_id = review['id'].split('/')[-2].split('-')[0]
        # Build album dict, append to albums
        album['link'] = review['link']
        album['date'] = datetime.fromtimestamp(mktime(review['published_parsed']))
        album['artist'] = review['title'].split(':')[0]
        album['album'] = review['title'].split(':')[1].strip()
        album['summary'] = review['summary']
        album['score'] = score
        album['it_status'] = 0
        album['it_artist'] = ''
        album['it_album'] = ''
        album['it_plays'] = 0
        albums[review_id] = album
    
    return albums

class pfkLib:
    def __init__(self, filename):
        # Load Pitchfork BNM library file if it exists
        self.filepath = os.path.join(os.path.split(os.path.expanduser(__file__))[0],filename)
        self.libraryData = dict()
        self.lib_exists = False
        if os.path.isfile(self.filepath):
            self.lib_exists = True
            libraryFile = open(self.filepath,'rb')
            self.libraryData = plistlib.load(libraryFile)
            libraryFile.close()

    def updateRSS(self):
        # Set number of records to pull
        if self.lib_exists:
            num = 5
        else:
            num = 100
            
        # Read RSS Feed, update Library Data
        feed_contents = getBestAlbums(num)
        id_list = self.libraryData.keys()
        for reviewID, review in feed_contents.items():
            if reviewID not in id_list:
                self.libraryData[reviewID] = review
        
        # Write updated data to BNM library file, creating one if necessary
        self.writeToPlist()
        
    def updateIT(self, it_library):
        # Update iTunes Data for each review
        for reviewID, review in self.libraryData.items():
            it_track_ids = it_library.getAlbumTracks(review['album'],review['artist'])
            # Set iTunes status (0 = missing, 1 = incomplete, 2 = complete)
            review['it_status'] = it_library.getAlbumStatus(it_track_ids)
            # If we have any tracks, set the iTunes album and artist names
            if review['it_status'] > 0:
                first_track = it_library.getTrack(it_track_ids[0])
                review['it_artist'] = first_track['Artist']
                review['it_album'] = first_track['Album']
                # Get the minimum play count from the album
                review['it_plays'] = int(first_track['Play Count'] or 0)
                for track_id in it_track_ids:
                    plays = int(it_library.getTrack(track_id)['Play Count'] or 0)
                    if plays < review['it_plays']:
                        review['it_plays'] = plays                       
                                    
        # Write updated data to BNM library file, creating one if necessary
        self.writeToPlist()
        
    def getKeys(self):
        return self.libraryData.keys()

    def getReviews(self):
        return self.libraryData

    def getReview(self, reviewID):
        return self.libraryData[reviewID]

    def getiTunesAlbumArtist(self,review_id):
        album = self.libraryData[review_id]['it_album']
        artist = self.libraryData[review_id]['it_artist']
        return [album, artist]

    def writeToPlist(self):
        if self.lib_exists:
            libraryFile = open(self.filepath, 'rb+')
        else:
            libraryFile = open(self.filepath, 'wb')
        plistlib.dump(self.libraryData, libraryFile)
        libraryFile.close()
