import tweepy, time
from random import randint
import pandas as pd
from pandas import DataFrame 

# twitter credentials
auth = tweepy.OAuthHandler("", "")
auth.set_access_token("", "")

api = tweepy.API(auth, wait_on_rate_limit=True,
    wait_on_rate_limit_notify=True)

target_user = "@DThompsonDev"
bot_name = "@DThompsonFanBo1"
time_to_sleep = 60*60 #1 hour

def get_last_bot_tweet():
    return api.user_timeline(screen_name=bot_name, 
                            count=1,
                            include_rts = False,
                            tweet_mode = 'extended'
                            )
def get_user_tweets():
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
    return all_tweets

def filter_tweets(tweets):
        return [tweet for tweet in tweets if '@' not in tweet.full_text and 'giveaway' not in tweet.full_text and tweet.favorite_count > 50]
    
def sort_tweets(tweets):
        return tweets.sort(key=get_favourite_count, reverse=True)

def get_favourite_count(tweet):
        return tweet.favorite_count

def put_tweets_into_csv(tweets):

    outtweets = [[tweet.id_str, 
                tweet.created_at, 
                tweet.favorite_count, 
                tweet.retweet_count, 
                tweet.full_text.encode("utf-8").decode("utf-8")] 
                for idx,tweet in enumerate(tweets)] 
    df = DataFrame(outtweets,columns=["id","created_at","favorite_count","retweet_count", "text"])
    df.to_csv('%s_tweets.csv' % target_user,index=False)
    df.head(3)

def restart():
    # sort_tweets(filter_tweets(get_user_tweets()))
    tweet_from_list(format_tweets(read_tweets_from_spreadsheet()))
    
def read_tweets_from_spreadsheet():
    tweets_from_csv = pd.read_csv('%s_tweets.csv' % target_user)
    return tweets_from_csv 

def format_tweets(tweets_list):
    return [str(tweet).replace('-&lt;', '<').replace('-&le;', '<=').replace('-&gt;', '>').replace('-&ge;', '>=').replace('&amp;', '&') for tweet in tweets_list["text"]]

def split_long_tweet(long_tweet):
    long_tweet_words = long_tweet.split()
    middle = round(len(long_tweet_words)/2)
    return (long_tweet_words[:middle], long_tweet_words[middle:])

def tweet_from_list(tweets_list):
    while len(tweets_list) > 1:
        
        if len(tweets_list[0]) < 266:
            tweet = tweets_list[0] + ' %s' % target_user
            print(tweet)
            api.update_status(tweet)
        else:
            tweet = tweets_list[0]
            print(tweet)
            api.update_status(tweet)
            last_tweet_set = get_last_bot_tweet()
            api.update_status(bot_name + ' %s' % target_user, last_tweet_set[0].id_str)



        # else:
        #     first_tweet, second_tweet = split_long_tweet(tweets_list[0])
        #     # api.update_status(' '.join(first_tweet) + ' [cont] %s' % target_user)
        #     # api.update_status('[cont] ' + ' '.join(second_tweet) + ' %s' % target_user)
        #     print(' '.join(first_tweet) + ' [cont] %s' % target_user)
        #     print("********************************************")
        #     print('[cont] ' + ' '.join(second_tweet) + ' ')
        tweets_list = tweets_list[1:]
        print("==============================================")
        print("Next tweet will be:")
        print(tweets_list[0] + ' %s' % target_user)
        print("==============================================")
        
        time.sleep(time_to_sleep)

    restart() 
    
restart()
