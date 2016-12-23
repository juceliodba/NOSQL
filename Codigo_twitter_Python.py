
# coding: utf-8

# In[26]:

from twython import Twython
from datetime import datetime
from pymongo import MongoClient
import json

import tweepy


import time
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import os

start_time = time.time() #grabs the system time
keyword_list = ['twitter'] #track list


# In[4]:

APP_KEY = ""
APP_SECRET = ""
OAUTH_TOKEN = ""
OAUTH_TOKEN_SECRET = ""


# In[5]:

tw = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)


# In[18]:

result = tw.search(q="brasil",count=1,lang="pt")


# In[ ]:




# In[79]:

from pymongo import MongoClient
import json
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import datetime


# Auth Variables

consumer_key = ""
consumer_key_secret = ""
access_token = ""
access_token_secret = ""



# MongoDB connection info

connection = MongoClient('localhost', 27017)
db = connection.TwitterStream
db.tweets.ensure_index("id", unique=True, dropDups=True)
collection = db.tweets

# Key words to be tracked, (hashtags)

keyword_list = [
'Renan', 'Temer', 'Política', 'Odebrecht', 'corrupção','STF','Lula','Dilma','PT','PMDB','PSDB',
               'Moro','Cunha','Kalil','FHC','Fernado Henrique Cardoso','Manifestação','PEC','Crise','Politicos','Delação',
    'Delatado','Corrupto','Corrupção','partido','partidos','janot','delação','governo','depoimento','votação','eleição','eleições',
    'câmara','milhoões','previdencia','reforma','lava-jato','petrobras','vazamento','escandalo',
               'Juca','PF','Senado','Presidencia','Caixa dois','Caixa 2','Propina','impeachment','Gilmar Mendes',
'#foratemer','golpista','#golpista','crise','jaburo','renúncia','eleição direta','delações','datafolha',
'citado','parlamentares','delator','oposição']


class StdOutListener(StreamListener):
    def on_data(self, data):

        # Load the Tweet into the variable "t"
        t = json.loads(data)

        # Pull important data from the tweet to store in the database.
        tweet_id = t['id_str']  # The Tweet ID from Twitter in string format
        text = t['text']  # The entire body of the Tweet
        hashtags = t['entities']['hashtags']  # Any hashtags used in the Tweet
        time_stamp = t['created_at']  # The timestamp of when the Tweet was created
        language = t['lang']  # The language of the Tweet

        # Convert the timestamp string given by Twitter to a date object called "created"
        created = datetime.datetime.strptime(time_stamp, '%a %b %d %H:%M:%S +0000 %Y')

        # Load all of the extracted Tweet data into the variable "tweet" that will be stored into the database
        tweet = {'id': tweet_id, 'text': text, 'hashtags': hashtags, 'language': language, 'created': created}

        # Save the refined Tweet data to MongoDB
        collection.insert_one(tweet)

        #print(tweet_id + "\n")
        return True
       
         
           
    # Prints the reason for an error to your console
    def on_error(self, status):
          
        print(status)

l = StdOutListener(api=tweepy.API(wait_on_rate_limit=True))
auth = OAuthHandler(consumer_key, consumer_key_secret)
auth.set_access_token(access_token, access_token_secret)

stream = Stream(auth, listener=l)
stream.filter(track=keyword_list)


# In[ ]:



