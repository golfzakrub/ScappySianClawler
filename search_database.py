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
import glob


class search_database():
    def __init__(self):
        self.dtM = dataManager()
    
    def tweet_search_no_date(self,keyword):
        all_files = glob.glob(f"{keyword}/*.csv")
        df = pd.concat((pd.read_csv(f,encoding = 'utf-8',index_col=0) for f in all_files))
        return df