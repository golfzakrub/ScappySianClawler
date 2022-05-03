from PyQt5 import QtCore
from tweet_Manager import TweepyManager


class TweetThread_Search(QtCore.QThread):
    finished = QtCore.pyqtSignal()
    def __init__(self,hashtag_phrase,datetime):
        QtCore.QThread.__init__(self)
        self.hashtag_phrase,self.datetime = hashtag_phrase,datetime
        self.tw_search = TweepyManager()
    
    def run(self):
        self.tw_search.search_for_hashtags(self.hashtag_phrase,self.datetime)
        self.finished.emit()