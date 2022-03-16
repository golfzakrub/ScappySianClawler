

import os
import tweepy as tw
import pandas as pd
import re


# In[ ]:


consumer_key= 'mhEpB8cHJhe5xt05df3LHEyeZ'
consumer_secret= 'dKImFjd55FWX4LX3R1V2VFi292DpQLj5NRXgFklbesOJp2hb82'
access_token= '912351283553513473-obrowBlTt2kNldW9wTPgRKonoXdYBIK'
access_token_secret= 'NnkI5fsyxxHVogATTUNp1oJxOfAspZrDBiNrFetR4Vakt'


# In[ ]:


auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)


# In[ ]:


# Post a tweet from Python
#api.update_status("Tweeting from #Python")


# In[ ]:


# Define the search term and the date_since date as variables
search_words = "#คิวเท"
date_since = "2022-03-01"


# In[ ]:


# Collect tweets
tweets = tw.Cursor(api.search_tweets,
              q=search_words,
              lang="th",
              since_id = '2022-03-15').items(5)
tweets


# In[ ]:


# Iterate and print tweets
for tweet in tweets:
    print(tweet.text)


# In[ ]:


# Collect a list of tweets
[tweet.text for tweet in tweets]


# In[ ]:


new_search = search_words + " -filter:retweets"
new_search


# In[ ]:


# Collect tweets
tweets = tw.Cursor(api.search_tweets,
              q=search_words,
              lang="th",
              since_id=date_since).items(5)

# Collect a list of tweets
[tweet.text for tweet in tweets]


# In[ ]:


tweets = tw.Cursor(api.search_tweets, 
                           q=new_search,
                           lang="th",
                           since_id=date_since).items(10)

users_locs = [[tweet.user.screen_name, tweet.user.location] for tweet in tweets]
users_locs


# In[ ]:


tweet_text = pd.DataFrame(data=users_locs, 
                    columns=['user', "location"])
tweet_text


# In[ ]:


new_search = "#PTT -filter:retweets"

tweets = tw.Cursor(api.search_tweets,
                   q=new_search,
                   lang="th",
                   since_id='date_since').items(100)

all_tweets = [tweet.text for tweet in tweets]
all_tweets[:10]


# In[ ]:


def remove_url(txt):
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


# In[ ]:


def remove_url_th(txt):
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


# In[ ]:


all_tweets_no_urls = [remove_url_th(tweet) for tweet in all_tweets]
all_tweets_no_urls[:20]


# In[ ]:


from pythainlp import word_tokenize

text = "ทดสอบการตัดตำภาษาไทย"
text = all_tweets_no_urls[0]
proc = word_tokenize(text, engine='newmm')
print(proc)


# In[ ]:


from textblob import TextBlob 
#text = "looked terrible on paper and sadly is terrible in its execution not even being so bad it is fun."
text = "It's all great fun, full of sly humour, snappy action and dapper dressing."
analysis = TextBlob(text)
sentiment = analysis.sentiment.polarity
print(sentiment)


# In[ ]:





# In[ ]:


from pythainlp.corpus import thai_stopwords

words = thai_stopwords()
print(words)


# In[ ]:




