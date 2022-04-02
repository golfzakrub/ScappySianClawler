
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtCore import  QSortFilterProxyModel

import pandas as pd
from pandasModel import pandasModel 

class dataManager():


    def getFile(self):

        self.filename = QFileDialog.getOpenFileName(filter = "Excel or CSV(*.csv ,*.xls ,*.xlsx ,*.xlsm)")[0]
        if self.filename == "" :
            print("please select file")
        else:
            return self.filename

    def readData(self,filename):
        self.all_data = pd.read_csv(filename,encoding = 'utf-8',index_col=0).dropna()

        print("read file finished")
        return self.all_data

