from fileinput import filename
from msilib.schema import CreateFolder
import re
from traceback import print_tb
from urllib import request
from numpy import result_type 
import requests
import tweepy 
import nltk
import pandas as pd
# import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from tweepy import OAuthHandler 
from textblob import TextBlob
from data import dataManager
import datetime 
from datetime import date, timedelta
import emoji 
from pythainlp.util import normalize
from pythainlp.tokenize import word_tokenize
from pythainlp.corpus import thai_stopwords
from collections import Counter
import time

###CLASS####


class TweepyManager():

    def __init__(self):
        
        self.dtM = dataManager()

        
        
    def connect(self):
    # Replace the xxxxx with your twitter api 
        load_dotenv()
        
        consumer_key= os.getenv('consumer_key')
        consumer_secret= os.getenv('consumer_secret')
        access_token= os.getenv('access_token')
        access_token_secret= os.getenv('access_token_secret')
    
        
        try:
            auth = OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)
            api = tweepy.API(auth)
            return api
        except:
            print("Error")
            exit(1)

    def cleanText(self,text):
        text =text.lower()
        text =re.sub(r'@[A-Za-z0-9]+','',text) #remove @mentions
        text =re.sub(r'#','',text) #remove the '#' symbol
        text =re.sub(r'RT[\s]+','',text)    #Remove RT
        text =re.sub(r'https?:\/\/\S+','',text) #Remove the hyper link
        # text = re.sub(r'[^\w\s]', '', text) #set to chr

        return text


    def THcleanText(self,text):
        url = "https://api.aiforthai.in.th/textcleansing"
        params = {'text':f"{text}"}

        headers = {
            'Apikey': "LZscuA9AIoUvt4OH5fFzpaB5dwy4aOD7",
            }
        text = requests.request("GET", url, headers=headers, params=params)



        return text.json().get('cleansing_text')

    def stem(self,text):
        # This function is used to stem the given sentence
        porter = PorterStemmer()
        token_words = word_tokenize(text)
        stem_sentence = []
        for word in token_words:
            stem_sentence.append(porter.stem(word))
        return " ".join(stem_sentence)

    def search_for_hashtags(self, hashtag_phrase,datetime):
        time.sleep(5)
        api = self.connect()
        
        keyword = hashtag_phrase

        checklang = re.compile(r'[a-zA-Z]')
        
        datetime_N = datetime.split('-')
        start_date = date(int(datetime_N[0]),int(datetime_N[1]),int(datetime_N[2]))
        until_date = start_date + timedelta(1)
        yesterday_date = start_date - timedelta(1)
        print(datetime_N)
        ############# ENG ################
        self.CreateMainFolder()
        self.CreateSubFolder(f"{hashtag_phrase}")
        
        
        if checklang.match(keyword.replace("#","")):            
            lang = "en"
            hashtag_pattern = re.compile(r"#[a-zA-Z']+")
            print("USE ENG SENTIMENT")
            tweets = tweepy.Cursor(api.search_tweets,
                q=f"{hashtag_phrase} -filter:retweets", 
                lang=lang,
                tweet_mode="extended",
                until=f"{until_date}",
                result_type = 'recent').items(700)

            
            users_locs = []
            try:
                keyword_lower = keyword.lower()
                keyword_list = keyword_lower.replace("#","")
                
            except:
                pass
            
            count = 0
            for tweet in tweets:
                if tweet.created_at.replace(tzinfo=None).date() > yesterday_date:
                    Relatehashtag = re.findall(hashtag_pattern, tweet.full_text)
                    now_text = self.remove_url(self.cleanText((tweet.full_text))).split(" ")
                    count = now_text.count(f"{keyword_list}")           
                    locs = [
                        keyword,
                        tweet.user.screen_name,
                        # tweet.user.location if tweet.user.location != '' else 'unknown',
                        tweet.created_at.replace(tzinfo=None),
                        self.remove_url(self.cleanText((tweet.full_text))),
                        tweet.retweet_count,
                        len(TextBlob(self.stem(self.remove_url(self.cleanText((tweet.full_text))))).split(" ")),                        
                        count,
                        tweet.favorite_count,
                        self.sentiment(TextBlob(self.stem(self.cleanText((tweet.full_text))))),
                        Relatehashtag,
                        tweet.user.followers_count,
                        f"https://twitter.com/twitter/statuses/{tweet.id}"]
                    users_locs.append(locs)
                                
            tweet_text = pd.DataFrame(data=users_locs, 
                columns=['Hashtag','Username','Date','Tweet','retweet','Word_count','Key_word_count','Favorite','Sentiment','RelateHashtag','Followers_count','tweet link'])
            
            fname = hashtag_phrase

            open(f"./data_tweepy/{fname}/{fname}_{datetime}.csv","w")
            tweet_text.to_csv(f"./data_tweepy/{fname}/{fname}_{datetime}.csv")
            filename=f"./data_tweepy/{fname}/{fname}_{datetime}.csv"
            self.dtM.readData(filename)
            return filename

        ############# TH ################
        else:
            lang = "th"
            hashtag_pattern = re.compile(r"#[\u0E00-\u0E7Fa-zA-Z']+")
            print("USE THAI SENTIMENT")
            tweets = tweepy.Cursor(api.search_tweets,
                q=f"{hashtag_phrase} -filter:retweets", 
                lang=lang,
                tweet_mode="extended",
                until=f"{until_date}",
                result_type = 'recent').items(500)
            

            users_locs = []
            keyword= keyword.replace("#","")
            #diff from eng keyword this use keyword with #

            count = 0
            for tweet in tweets:
                try:
                    tweet_sentiment = self.THsentiment(normalize(self.remove_url_th(tweet.full_text)))
                    if tweet_sentiment =="":
                        tweet_sentiment ="neutral"

                except:
                    continue
                if tweet_sentiment =="":
                    tweet_sentiment ="neutral"
                if tweet.created_at.replace(tzinfo=None).date() > yesterday_date:

                    Relatehashtag = re.findall(hashtag_pattern, tweet.full_text)
                    now_text = normalize(self.remove_url_th(tweet.full_text))
                    count = now_text.count(f"{keyword}")           
                    locs = [
                        f"#{keyword}",
                        tweet.user.screen_name,
                        # tweet.user.location if tweet.user.location != '' else 'unknown',
                        tweet.created_at.replace(tzinfo=None),
                        normalize(self.remove_url_th(tweet.full_text)),
                        tweet.retweet_count,
                        len(self.THStopword_new(self.remove_url_th(tweet.full_text))),
                        count,
                        tweet.favorite_count,
                        tweet_sentiment,
                        Relatehashtag,
                        tweet.user.followers_count,
                        f"https://twitter.com/twitter/statuses/{tweet.id}"]
                    users_locs.append(locs)
            print("finish")
            tweet_text = pd.DataFrame(data=users_locs, 
                columns=['Hashtag','Username','Date','Tweet','retweet','Word_count','Key_word_count','Favorite','Sentiment','RelateHashtag','Followers_count','tweet link'])
            
            fname = hashtag_phrase
            

            
            open(f"./data_tweepy/{fname}/{fname}_{datetime}.csv","w")
            tweet_text.to_csv(f"./data_tweepy/{fname}/{fname}_{datetime}.csv")
            filename=f"./data_tweepy/{fname}/{fname}_{datetime}.csv"
            self.dtM.readData(filename)

            return filename
        

    # def save_to_excel(self, tweets):
    #     tweets.to_excel("./data/tweets.xlsx", engine="openpyxl", index=False)
            

    def sentiment(self,cleaned_text):
        # Returns the sentiment based on the polarity of the input TextBlob object
        if cleaned_text.sentiment.polarity > 0:
            return 'positive'
        elif cleaned_text.sentiment.polarity < 0:
            return 'negative'
        else:
            return 'neutral'

    def THsentiment(self,cleaned_text):

        url = "https://api.aiforthai.in.th/ssense"
        
        params = {'text':f"{cleaned_text}"}
        
        headers = {
            'Apikey': "LZscuA9AIoUvt4OH5fFzpaB5dwy4aOD7"
            }
        
        cleaned_text = requests.get(url, headers=headers, params=params)
        
        
        return cleaned_text.json()['sentiment']['polarity']


    def THstopword(self,cleaned_text):
        
        
        url = "https://api.aiforthai.in.th/tpos"
        
        params = {'text':f"{cleaned_text}"}
        
        headers = {
            'Apikey': "LZscuA9AIoUvt4OH5fFzpaB5dwy4aOD7",
            }
        
        cleaned_text= requests.get(url, headers=headers, params=params)
        
        return len(cleaned_text.json()['words'])

    def THKeyword(self,cleaned_text):
        
        
        url = "https://api.aiforthai.in.th/tpos"
        
        params = {'text':f"{cleaned_text}"}
        
        headers = {
            'Apikey': "LZscuA9AIoUvt4OH5fFzpaB5dwy4aOD7",
            }
        
        cleaned_text= requests.get(url, headers=headers, params=params)
        # print(cleaned_text.json()['words'])
        
        return cleaned_text.json()['words']


    def remove_url(self,txt):
        """Replace URLs found in a text string with nothing 
        (i.e. it will remove the URL from the string).
        Parameters
        ----------
        txt : string
            A text string that you want to parse and remove urls.
        Returns
        -------
        The same txt string with url's removed.
        """

        return " ".join(re.sub("([^0-9A-Za-z \t])|(\w+:\/\/\S+)", "", txt).split())

    def remove_url_th(self,txt):
        """Replace URLs found in a text string with nothing 
        (i.e. it will remove the URL from the string).
        Parameters
        ----------
        txt : string
            A text string that you want to parse and remove urls.
        Returns
        -------
        The same txt string with url's removed.
        """

        return " ".join(re.sub("([^\u0E00-\u0E7Fa-zA-Z' ]|^'|'$|''|(\w+:\/\/\S+))", "", txt).split())
            
    def remove_emoji(self,text):
        return ''.join([c for c in text if c not in emoji.UNICODE_EMOJI])


    def THStopword_new(self,text):
        text = f"{text}"
        list_word = word_tokenize(text)
        


        stopwords = list(thai_stopwords())
        list_word_not_stopwords = [i for i in list_word if i not in stopwords]
        

        return list_word_not_stopwords

    def trending(self):
        api = self.connect()

        # WOEID of Bangkok
        woeid = 1225448

        # fetching the trends
        trends = api.get_place_trends(id = woeid)

        # printing the information
        # print("The top trends for the location are :")
        user_loc = []
        for value in trends:
            for trend in value['trends']:
                user_loc.append(trend['name'])

        tweet_text = pd.DataFrame(data=user_loc, 
            columns=['Top Trend'])
            
        
        tweet_text.to_csv('trending.csv')
        filename ='trending.csv'
        self.dtM.readData(filename)

        return filename

    def CreateMainFolder(self):
        if not os.path.exists(f"./data_tweepy"):                    
            os.mkdir(f"./data_tweepy")
            print("CreteMainFolder Successed")        

    def CreateSubFolder(self,filename):
        if not os.path.exists(f"./data_tweepy/{filename}"):                    
            os.mkdir(f"./data_tweepy/{filename}")
            print("CreteSubFolder Successed")



    def RelateHashtag(self,filename):
        # filename = './data_tweepy/#Liverpool/#Liverpool_2022-05-03.csv'
        df = pd.read_csv(filename,encoding = 'utf-8').dropna()
        count_word = Counter()

        for list in df["RelateHashtag"]:
                    count_word += Counter(eval(list))

        count_word_list =[]
        for item in count_word.most_common():
            locs = [item[0],item[1]]
            count_word_list.append(locs)
        df = pd.DataFrame(data=count_word_list,columns=['Hashtag','count'])

        return df


