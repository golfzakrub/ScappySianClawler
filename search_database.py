from fileinput import filename
from msilib.schema import CreateFolder
import re
from urllib import request 
import requests
import tweepy 
import nltk
import pandas as pd
# import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv
from tweepy import OAuthHandler 
from textblob import TextBlob
from data import dataManager
import datetime 
from datetime import date, timedelta
import glob


class search_database():
    def __init__(self):
        self.dtM = dataManager()
    
    def tweet_search_no_date(self,keyword):
        all_files = glob.glob(f"{keyword}/*.csv")
        df = pd.concat((pd.read_csv(f,encoding = 'utf-8',index_col=0) for f in all_files))
        return df

    def tweet_search_with_date(self,keyword,date1,date2):
        
        date1 = date1
        date2 = date2
        date1_n = date1.split('-')
        date2_n = date2.split('-')

        date_list = []
        start_date = date(int(date1_n[0]),int(date1_n[1]),int(date1_n[2]))
        end_date = date(int(date2_n[0]),int(date2_n[1]),int(date2_n[2]))    # perhaps date.now()

        delta = end_date - start_date   # returns timedelta
        datetime
        for i in range(delta.days + 1):
            day = start_date + timedelta(days=i)
            # print(r"#Liverpool//Liverpool_{day}.csv")
            files = f"{keyword}\\{keyword}_{day}.csv"
            date_list.append(files)
        
        all_files = glob.glob(f"{keyword}/*.csv")

        interseclist = self.intersection(date_list,all_files)

        df = pd.concat((pd.read_csv(f,encoding = 'utf-8',index_col=0) for f in interseclist))

                

        
        return df


    def Web_search_no_date(self,keyword):
        all_files = glob.glob(f"data_csv/{keyword}/*.csv")
        df = pd.concat((pd.read_csv(f,encoding = 'utf-8',index_col=0) for f in all_files))
        return df

    def intersection(self,lst1, lst2):
        lst3 = [value for value in lst1 if value in lst2]
        return lst3           