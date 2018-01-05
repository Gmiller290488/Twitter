# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 20:01:32 2016

@author: Gareth Miller
"""
import tweepy, time
from random import randint
from credentials import *

# twitter credentials
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth)

## read in the text from the file
#filename = open('definitions.txt', 'r')
#tweettext = filename.readlines()
#filename.close()
#
def findLocationLastTweet():
    lastTweet = getLastTweet('cs_definitions')
    tweetwords = lastTweet.split(" ")
    txtfileline = 0
    for line in tweettext:
        txtfileline += 1
        if line == tweetwords[0]:
            print(txtfileline)
            return txtfileline 
    txtfileline = randint(0, len(tweettext))
    if txtfileline % 2 != 0:
        return txtfileline+1
    else: 
        return txtfileline 
    
def getLastTweet(screen_name):
    lastTweet = api.user_timeline(screen_name = screen_name, count=1)[0]
    return lastTweet.text

print(getLastTweet('cs_definitions'))
#print(findLocationLastTweet())

#    
#while True:
#    i = findLocationLastTweet(user)
#    if int(i) < len(tweettext):
#        api.update_status(tweettext[i])
#        i += 1
#        api.update_status(tweettext[i])
#        i -= 1
#    i += 2
#                    
#        
#            
#    time.sleep(86400)  #sleep for 24 hours   
#        
