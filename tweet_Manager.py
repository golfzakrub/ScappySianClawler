import re
from urllib import request 
import requests
import tweepy 
import nltk
import pandas as pd
import matplotlib.pyplot as plt


from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from tweepy import OAuthHandler 
from textblob import TextBlob
from data import dataManager

###CLASS####


class TweepyManager():

    def __init__(self):
        
        self.dtM = dataManager()
        
        
        
    def connect(self):
    # Replace the xxxxx with your twitter api keys
        consumer_key= 'mhEpB8cHJhe5xt05df3LHEyeZ'
        consumer_secret= 'dKImFjd55FWX4LX3R1V2VFi292DpQLj5NRXgFklbesOJp2hb82'
        access_token= '912351283553513473-obrowBlTt2kNldW9wTPgRKonoXdYBIK'
        access_token_secret= 'NnkI5fsyxxHVogATTUNp1oJxOfAspZrDBiNrFetR4Vakt'
    
        
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


        
        return text.json().get('cleansing_text')

    def stem(self,text):
        # This function is used to stem the given sentence
        porter = PorterStemmer()
        token_words = word_tokenize(text)
        stem_sentence = []
        for word in token_words:
            stem_sentence.append(porter.stem(word))
        return " ".join(stem_sentence)

    def search_for_hashtags(self, hashtag_phrase):
        api = self.connect()
        
        keyword = hashtag_phrase

        checklang = re.compile(r'[a-zA-Z]')

        ############# ENG ################
        if checklang.match(keyword.replace("#","")):
            lang = "en"
            print("USE ENG SENTIMENT")
            tweets = api.search_tweets(
                q=f"{hashtag_phrase} -filter:retweets", 
                lang=lang,
                until='2022-03-31',
                count =1000)

            tweets_set = set()
            for tweet in tweets:
                tweets_set.add(tweet)
            tweets = list(tweets_set)
            

            users_locs = [[
                keyword,
                tweet.user.screen_name,
                # tweet.user.location if tweet.user.location != '' else 'unknown',
                tweet.created_at.replace(tzinfo=None),
                self.remove_url(self.cleanText((tweet.text))),
                tweet.retweet_count,
                self.sentiment(TextBlob(self.stem(self.cleanText((tweet.text))))),
                tweet.user.followers_count,
                f"https://twitter.com/twitter/statuses/{tweet.id}"] for tweet in tweets
                ]
                        
            tweet_text = pd.DataFrame(data=users_locs, 
                columns=['Hashtag','Username','Date','Tweet','retweet','Sentiment','Followers_count','tweet link'])
            
            fname = hashtag_phrase
            tweet_text.to_csv(f"{fname}.csv")
            filename =f"{fname}.csv"
            self.dtM.readData(filename)

            return filename

        ############# TH ################
        else:
            lang = "th"
            print("USE THAI SENTIMENT")
            tweets = api.search_tweets(
                q=f"{hashtag_phrase} -filter:retweets", 
                lang=lang,
                until='2022-03-31',
                count = 1000)

            tweets_set = set()
            for tweet in tweets:
                tweets_set.add(tweet)
            tweets = list(tweets_set)
            

            users_locs = []
            for tweet in tweets:
                try:
                    tweet_sentiment = self.THsentiment(self.THcleanText((tweet.text)))
                except:
                    continue
                locs = [
                            self.THcleanText(keyword),
                            tweet.user.screen_name,
                            # tweet.user.location if tweet.user.location != '' else 'unknown',
                            tweet.created_at.replace(tzinfo=None),
                            self.THcleanText(tweet.text),
                            tweet.retweet_count,

                            tweet_sentiment,
                            tweet.user.followers_count,
                            f"https://twitter.com/twitter/statuses/%7Btweet.id%7D"]
                users_locs.append(locs)
            print("finish")
            tweet_text = pd.DataFrame(data=users_locs, 
                columns=['Hashtag','Username','Date','Tweet','retweet','Sentiment','Followers_count','tweet link'])
            
            fname = hashtag_phrase
            tweet_text.to_csv(f"{fname}.csv")
            filename =f"{fname}.csv"
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
        
        print(cleaned_text.json()['sentiment']['polarity'])
        return cleaned_text.json()['sentiment']['polarity']

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
            

