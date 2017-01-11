# -*- coding: utf-8 -*-
"""
Created on Fri Sep 23 18:39:19 2016
Chris Jackson bot
@author: Gareth Miller
"""
import tweepy, time
from gettweetsbot import getLastTweet
from random import randint
from credentials import *
auth = tweepy.OAuthHandler("EDITED OUT", "EDITED OUT")
auth.set_access_token("EDITED OUT", "EDITED OUT")
api = tweepy.API(auth)


# What the bot will tweet

filename = open('jacko.txt', 'r')
tweettext = filename.readlines()
filename.close()

filename = open('names.txt', 'r')
nameList = filename.readlines()
filename.close()
    
def linenumTweets():
    return randint(0, len(tweettext)-1)



def nameChange():
    i = randint(0, len(nameList)-1)
    newName = nameList[i].upper()
    newName = list(newName)
    finalName = ""
    for char in newName:
        finalName += char + "-"
        finalName = finalName[:-1]
    return finalName
    
a = 14
while True: 
        latestTweet = getLastTweet("BeardedWelsh_CJ")
                
       # nextTweet = tweettext[a]
        
        if a == 9:
            nextTweet = tweettext[a] + nameChange()
        elif a == 12:
            nextTweet = tweettext[a] + " @mnerney86"
        elif latestTweet != tweettext[a]:
            api.update_status(tweettext[a])
            print(tweettext[a])
            print('...')
            time.sleep(7200)
            
            if a+1 == len(tweettext)-1:
                a = 0
            else:
                a += 1
            # Sleep for 2hours        
