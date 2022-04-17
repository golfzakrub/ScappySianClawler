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
            'Apikey': "Oh2wndIoRybtDhRSJVN5u2HugwQSFhkk",
            }
        text = requests.request("GET", url, headers=headers, params=params)


        print(text.json().get('cleansing_text'))
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
        api = self.connect()
        
        keyword = hashtag_phrase

        checklang = re.compile(r'[a-zA-Z]')
        
        datetime_N = datetime.split('-')
        start_date = date(int(datetime_N[0]),int(datetime_N[1]),int(datetime_N[2]))
        until_date = start_date + timedelta(1)
        yesterday_date = start_date - timedelta(1)
        print(datetime_N)
        ############# ENG ################
        self.CreateFolder(f"{hashtag_phrase}")
        if checklang.match(keyword.replace("#","")):
            lang = "en"
            print("USE ENG SENTIMENT")
            tweets = tweepy.Cursor(api.search_tweets,
                q=f"{hashtag_phrase} -filter:retweets", 
                lang=lang,
                until=f"{until_date}",
                result_type = 'recent').items(50)

            tweets_set = set()        
            for tweet in tweets:
                tweets_set.add(tweet)
 
            tweets = list(tweets_set)
            

            users_locs = []
            try:
                keyword_lower = keyword.lower()
                keyword_list = keyword_lower.replace("#","")
                
            except:
                pass
            
            count = 0
            for tweet in tweets:
                if tweet.created_at.replace(tzinfo=None).date() > yesterday_date:
                    print(keyword_list)
                    now_text = self.remove_url(self.cleanText((tweet.text))).split(" ")
                    print(now_text)
                    count = now_text.count(f"{keyword_list}")
                    print(count)            
                    locs = [
                        keyword,
                        tweet.user.screen_name,
                        # tweet.user.location if tweet.user.location != '' else 'unknown',
                        tweet.created_at.replace(tzinfo=None),
                        self.remove_url(self.cleanText((tweet.text))),
                        tweet.retweet_count,
                        len(TextBlob(self.stem(self.remove_url(self.cleanText((tweet.text))))).split(" ")),
                        count,
                        self.sentiment(TextBlob(self.stem(self.cleanText((tweet.text))))),
                        tweet.user.followers_count,
                        f"https://twitter.com/twitter/statuses/{tweet.id}"]
                    users_locs.append(locs)
                                
            tweet_text = pd.DataFrame(data=users_locs, 
                columns=['Hashtag','Username','Date','Tweet','retweet','Word_count','Key_word_count','Sentiment','Followers_count','tweet link'])
            
            fname = hashtag_phrase

            open(f"./{fname}/{fname}_{datetime}.csv","w")
            tweet_text.to_csv(f"./{fname}/{fname}_{datetime}.csv")
            filename=f"./{fname}/{fname}_{datetime}.csv"
            self.dtM.readData(filename)
            return filename

        ############# TH ################
        else:
            lang = "th"
            print("USE THAI SENTIMENT")
            tweets = tweepy.Cursor(api.search_tweets,
                q=f"{hashtag_phrase} -filter:retweets", 
                lang=lang,
                until=f"{until_date}",
                result_type = 'recent').items(20)

            tweets_set = set()
            for tweet in tweets:
                tweets_set.add(tweet)
            tweets = list(tweets_set)
            

            users_locs = []
            count = 0
            for tweet in tweets:
                try:
                    tweet_sentiment = self.THsentiment(self.THcleanText((tweet.text)))
                except:
                    continue
                if tweet.created_at.replace(tzinfo=None).date() > yesterday_date:
                    # now_text = self.THKeyword(self.THcleanText((tweet.text)))
                
                    # count = now_text.count(keyword_list)
                    locs = [
                                self.THcleanText(keyword),
                                tweet.user.screen_name,
                                # tweet.user.location if tweet.user.location != '' else 'unknown',
                                tweet.created_at.replace(tzinfo=None),
                                self.THcleanText(tweet.text),
                                tweet.retweet_count,
                                self.THstopword(self.THcleanText((tweet.text))),
                                count,
                                tweet_sentiment,
                                tweet.user.followers_count,
                                f"https://twitter.com/twitter/statuses/%7Btweet.id%7D"]
                    users_locs.append(locs)
            print("finish")
            tweet_text = pd.DataFrame(data=users_locs, 
                columns=['Hashtag','Username','Date','Tweet','retweet','Word_count','Key_word_count','Sentiment','Followers_count','tweet link'])
            
            fname = hashtag_phrase
            

            
            open(f"./{fname}/{fname}_{datetime}.csv","w")
            tweet_text.to_csv(f"./{fname}/{fname}_{datetime}.csv")
            filename=f"./{fname}/{fname}_{datetime}.csv"
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
            'Apikey': "Oh2wndIoRybtDhRSJVN5u2HugwQSFhkk"
            }
        
        cleaned_text = requests.get(url, headers=headers, params=params)
        
        
        return cleaned_text.json()['sentiment']['polarity']


    def THstopword(self,cleaned_text):
        
        
        url = "https://api.aiforthai.in.th/tpos"
        
        params = {'text':f"{cleaned_text}"}
        
        headers = {
            'Apikey': "Oh2wndIoRybtDhRSJVN5u2HugwQSFhkk",
            }
        
        cleaned_text= requests.get(url, headers=headers, params=params)
        
        return len(cleaned_text.json()['words'])

    def THKeyword(self,cleaned_text):
        
        
        url = "https://api.aiforthai.in.th/tpos"
        
        params = {'text':f"{cleaned_text}"}
        
        headers = {
            'Apikey': "Oh2wndIoRybtDhRSJVN5u2HugwQSFhkk",
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

    def CreateFolder(self,filename):
        
        if not os.path.exists(f"./{filename}"):                    
            os.mkdir(f"./{filename}")  
            print("CreteFolder Successed")


    def Keyword_count_eng(self,cleaned_text):
        pass