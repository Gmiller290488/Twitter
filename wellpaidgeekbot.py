import tweepy, time
from random import randint
import pandas as pd
from pandas import DataFrame 

# twitter credentials

auth = tweepy.OAuthHandler("XB6Ti8bTuX99NO5RHnRZ6RF8D", "s2G2lkSc3ULXZ7rK0Z5xHAxAvY8pUvNT6YuC1GdzA17l1c7MzU")
auth.set_access_token("1288468850779000833-j9lfidvfygjDKCmg96zfWOWI4EgM2n", "CN2pQSgoPnUeqXTf1RnWz0eRSyCNyRT4dY0kRVndB1SAG")

api = tweepy.API(auth, wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True)

target_user = "@wellpaidgeek"
bot_name = "@wellpaidgeekbot"

def get_tweets():
    tweets = api.user_timeline(screen_name=target_user, 
                            count=200,
                            include_rts = False,
                            tweet_mode = 'extended'
                            )
        
    all_tweets = []
    all_tweets.extend(tweets)
    oldest_id = tweets[-1].id

    while True:
        tweets = api.user_timeline(screen_name=target_user, 
                            count=200,
                            include_rts = False,
                            max_id = oldest_id - 1,
                            tweet_mode = 'extended'
                            )
        if len(tweets) == 0:
            break
        oldest_id = tweets[-1].id
        all_tweets.extend(tweets)
        print('N of tweets downloaded till now {}'.format(len(all_tweets)))

    def get_favourite_count(tweet):
        return tweet.favorite_count

    # filtered_tweets = [tweet for tweet in all_tweets if '@' not in tweet.full_text and tweet.favorite_count > 50 and len(tweet.full_text) < 266]
    filtered_tweets = [tweet for tweet in all_tweets if '@' not in tweet.full_text and tweet.favorite_count > 50]
    filtered_tweets.sort(key=get_favourite_count, reverse=True)

    outtweets = [[tweet.id_str, 
                tweet.created_at, 
                tweet.favorite_count, 
                tweet.retweet_count, 
                tweet.full_text.encode("utf-8").decode("utf-8")] 
                for idx,tweet in enumerate(filtered_tweets)] 
    df = DataFrame(outtweets,columns=["id","created_at","favorite_count","retweet_count", "text"])
    df.to_csv('%s_tweets_long_text.csv' % target_user,index=False)
    df.head(3)

    tweets_from_csv = read_tweets_from_spreadsheet()
    tweet_from_id(tweets_from_csv)

def restart():
    get_tweets()

def read_tweets_from_spreadsheet():
    tweets_from_csv = pd.read_csv("@wellpaidgeek_tweets_long_text.csv")
    return tweets_from_csv 

def tweet_from_id(tweets_from_csv):
    tweetList = [tweet for tweet in tweets_from_csv["text"]]
    while len(tweetList) > 1:
    
        if len(tweetList[0]) < 266:
            tweet = tweetList[0] + ' @wellpaidgeek'
            print(tweet)
            api.update_status(tweet)
        else:
            long_tweet = tweetList[0]
            long_tweet_words = long_tweet.split()

            middle = round(len(long_tweet_words)/2)
            first_half = long_tweet_words[:middle]
            second_half = long_tweet_words[middle:]
            api.update_status(' '.join(first_half) + ' [cont] @wellpaidgeek')
            api.update_status('[cont] ' + ' '.join(second_half) + ' @wellpaidgeek')
            print(' '.join(first_half) + ' [cont] @wellpaidgeek')
            print("********************************************")
            print('[cont] ' + ' '.join(second_half) + ' @wellpaidgeek')
        tweetList = tweetList[1:]
        print("==============================================")
        print("Next tweet will be:")
        print(tweetList[0] + ' @wellpaidgeek')
        print("==============================================")

        time.sleep(2*60*60)
        
    restart() 
    
# get_tweets()
tweets_from_csv = read_tweets_from_spreadsheet()
tweet_from_id(tweets_from_csv)