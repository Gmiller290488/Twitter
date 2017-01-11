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
auth = tweepy.OAuthHandler("4Uu7Ewc3u76cowtx3xfmyts8v", "urKWZ7LcjAl5D2828xO9uQ6Pywcym7g0QNXwlipAVyiK4ake8L")
auth.set_access_token("790632355484622848-E2mQvr5ODFC0K4XofS8s7EJDUSguIcy", "LjJiec4rEZIuqqpbQeAl3Yk57PtVNf2hWiXbd989azuOo")
api = tweepy.API(auth)
user = ["@ctingcter ", "@runwithalice "]

#twilio variables
myTwilioNumber = "+441865922379"
myPhoneNumber = "+447739988398"
accountSID = "AC93948e9cd1e5c5a432026ae15c15e65d"
authToken = "246a9c92c1033b40c8eadad78535b210"
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
        
