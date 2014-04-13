from Foundation import NSObject
from itunes_lib import *
from itunes_controller import playAlbum
from pitchfork_module import pfkLib

class PfkBNMModel(NSObject):

    def init(self):
        # Read the pitchfork plist
        self.pitchforkLibrary = pfkLib("bnm.plist")
        return self

    def update(self):
        # Update the pitchfork review list
        self.pitchforkLibrary.updateRSS()
        # Read the user's iTunes library and update the it_status of each review
        self.itunesLibrary = iTunesLib("~/Music/iTunes/iTunes Music Library.xml")
        self.pitchforkLibrary.updateIT(self.itunesLibrary)
    
    def playAlbum(self, album, artist):
        # Tell iTunes to play the specified album/artist
        playAlbum("temp_playlist",album,artist)

    def getReviews(self):
        # Return a dictionary object with all of the reviews
        return self.pitchforkLibrary.getReviews()

    def getReviewList(self):
        # Return a list object with all of the reviews
        reviews = self.getReviews()
        reviewList = []
        for reviewID, review in reviews.items():
            reviewList.append(review)
        return reviewList

    def getReview(self, reviewID):
        # Return a given review
        return self.pitchforkLibrary.getReview(reviewID)
