from Cocoa import *
from Foundation import NSObject
from PfkBNMModel import *
import operator, webbrowser, syslog

class PfkBNMController(NSObject):
    bnmModel = objc.IBOutlet()
    table = objc.IBOutlet()
    
    def awakeFromNib(self):
        self.selectedReview = None
        self.reviewList = self.bnmModel.getReviewList()
        self.reviewList.sort(key=operator.itemgetter('date'), reverse = True)
        self.table.reloadData()

    @objc.IBAction
    def play_(self, sender):
        if (self.selectedReview is None) or (self.selectedReview['it_status']==0):
            pass
        else:
            album = self.selectedReview['it_album']
            artist = self.selectedReview['it_artist']
            self.bnmModel.playAlbum(album,artist)

    @objc.IBAction
    def read_(self, sender):
        webbrowser.open(self.selectedReview['link'], new=1)

    @objc.IBAction
    def reload_(self, sender):
        self.bnmModel.update()
        self.reviewList = self.bnmModel.getReviewList()
        self.reviewList.sort(key=operator.itemgetter('date'), reverse = True)
        self.table.reloadData()
        
    # table view delegate methods
    def numberOfRowsInTableView_(self, tableView):
        return len(self.reviewList)

    def tableView_objectValueForTableColumn_row_(self, tableView, col, row):
        column = str(col).split(':')[2].strip()
        if column == 'date':
            return self.reviewList[row][column].strftime('%b %d, %Y')
        else:
            return self.reviewList[row][column]
            
    def tableView_shouldEditTableColumn_row_(self, tableView, col, row):
        return 0      

    def tableViewSelectionDidChange_(self, notification):
        self.selectedReview = self.reviewList[self.table.selectedRow()]
            
if __name__ == "__main__":
    from PyObjCTools import AppHelper
    AppHelper.runEventLoop()
