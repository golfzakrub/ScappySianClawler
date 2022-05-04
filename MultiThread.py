from PyQt5 import QtCore
from tweet_Manager import TweepyManager
from crawler1 import Crawler
from webkey import KEY_MANAGER

class TweetThread_Search(QtCore.QThread):
    finished = QtCore.pyqtSignal()
    def __init__(self,hashtag_phrase,datetime):
        QtCore.QThread.__init__(self)
        self.hashtag_phrase,self.datetime = hashtag_phrase,datetime
        self.tw_search = TweepyManager()
    
    def run(self):
        self.tw_search.search_for_hashtags(self.hashtag_phrase,self.datetime)
        self.finished.emit()
    
class WebThread_Search(QtCore.QThread):
    finished = QtCore.pyqtSignal()
    def __init__(self):
        QtCore.QThread.__init__(self)
        self.wcr_search = Crawler()
    
    def run(self):
        self.wcr_search.start_crawler()
        self.finished.emit()    

class Web_scan_word(QtCore.QThread):
    finished = QtCore.pyqtSignal()
    def __init__(self,keyword):
        QtCore.QThread.__init__(self)
        self.keyword = keyword
        self.wk_search = KEY_MANAGER()
    
    def run(self):
        self.wk_search.start_scan(self.keyword)
        self.finished.emit()    
    
