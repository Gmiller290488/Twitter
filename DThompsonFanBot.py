import tweepy, time
from random import randint
import pandas as pd
from pandas import DataFrame 

# twitter credentials
auth = tweepy.OAuthHandler("Dd4slek3NaGruXumIi63mcPbB", "4lT2bIeTgPfbv4vY34y5bRvex4td5Hv3B9t5tGmjYYt8aMOWq7")
auth.set_access_token("1288040332714745857-D9MuPzis6CXCaBbL0LtEQXtdXmqDVV", "c4myasCchga02C5rNC67897uhj3OAdz2GDsF2bRPoCXxP")

api = tweepy.API(auth, wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True)

target_user = "@DThompsonDev"
bot_name = "@DThompsonFanBo1"

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

    tweets_from_csv = read_tweets_from_spreadsheet()
    tweet_from_id(tweets_from_csv)

    def get_favourite_count(tweet):
        return tweet.favorite_count

    filtered_tweets = []
    filtered_tweets = [tweet for tweet in all_tweets if '@' not in tweet.full_text and tweet.favorite_count > 50 and len(tweet.full_text) < 266]
    filtered_tweets.sort(key=get_favourite_count, reverse=True)

    outtweets = [[tweet.id_str, 
                tweet.created_at, 
                tweet.favorite_count, 
                tweet.retweet_count, 
                tweet.full_text.encode("utf-8").decode("utf-8")] 
                for idx,tweet in enumerate(filtered_tweets)] 
    df = DataFrame(outtweets,columns=["id","created_at","favorite_count","retweet_count", "text"])
    df.to_csv('%s_tweets.csv' % target_user,index=False)
    df.head(3)

def restart():
    get_tweets()

def read_tweets_from_spreadsheet():
    tweets_from_csv = pd.read_csv("@DThompsonDev_tweets.csv")
    return tweets_from_csv 

def tweet_from_id(tweets_from_csv):
    tweetList = [tweet for tweet in tweets_from_csv["text"]]
    while len(tweetList) > 1:
        tweet = tweetList[0] + ' @DThompsonDev'
        print(tweet)
        # api.update_status(tweet)
        tweetList = tweetList[1:]
        print("==============================================")
        print("Next tweet will be:")
        print(tweetList[0] + ' @DThompsonDev')
        print("==============================================")
        time.sleep(3*60*60)
        
    restart() 
    
tweets_from_csv = read_tweets_from_spreadsheet()
tweet_from_id(tweets_from_csv)