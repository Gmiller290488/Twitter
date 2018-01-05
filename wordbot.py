# -*- coding: utf-8 -*-
"""
Created on Mon Oct 24 20:01:32 2016

@author: Gareth Miller
"""
import tweepy, time
from twilio.rest import TwilioRestClient
from gettweetsbot import getLastTweet
from random import randint
from credentials import *



# twitter credentials
auth = tweepy.OAuthHandler("EDITED OUT", "EDITED OUT")
auth.set_access_token("EDITED OUT", "EDITED OUT")
api = tweepy.API(auth)
user = ["@ctingcter ", "@runwithalice "]

#twilio variables
myTwilioNumber = "EDITED OUT"
myPhoneNumber = "EDITED OUT"
accountSID = "EDITED OUT"
authToken = "EDITED OUT"
twilioCli = TwilioRestClient(accountSID, authToken)



# read in the text from the file
filename = open('definitions.txt', 'r')
tweettext = filename.readlines()
filename.close()




def textWord():
    message = twilioCli.messages.create(body=tweettext[i], from_=myTwilioNumber, to=myPhoneNumber)

def findLocationLastTweet(name):
    lastTweet = getLastTweet('WorddefinitionG')
    words = lastTweet.split(" ")
    i = 0
    for line in tweettext:
        i += 1
        if line == words[1]:
            print(i)
            return i
    i = randint(0, len(tweettext))
    if i % 2 != 0:
        return i+1
    else: 
        return i 
    
findLocationLastTweet(user)
    
while True:
    i = findLocationLastTweet(user)
    for name in user:        
        if int(i) < len(tweettext):
            if name == "@ctingcter ":
                textWord()
            currentTweet = name + tweettext[i]
            print(currentTweet)
            api.update_status(currentTweet)
            i += 1
            if name == "@ctingcter ":
                textWord()
            currentTweet = name + tweettext[i]
            print(currentTweet)
            api.update_status(currentTweet)
            i -= 1
    i += 2
                    
        
            
    time.sleep(86400)  #sleep for 24 hours   
        
