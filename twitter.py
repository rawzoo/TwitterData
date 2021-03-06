import re 
import tweepy 
from tweepy import OAuthHandler 
from textblob import TextBlob 


class TwitterClient(object): 
    def __init__(self): 
        consumer_key = 'XXXXXXXXXXXXXXXXXXXXXXXX'
        consumer_secret = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXX'
        access_token = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXX'
        access_token_secret = 'XXXXXXXXXXXXXXXXXXXXXXXXX'

        # attempt authentication 
        try: 
            # create OAuthHandler object 
            self.auth = OAuthHandler(consumer_key, consumer_secret) 
            # set access token and secret 
            self.auth.set_access_token(access_token, access_token_secret) 
            # create tweepy API object to fetch tweets 
            self.api = tweepy.API(self.auth) 
        except: 
                print("Error: Authentication Failed") 

    def clean_tweet(self, tweet): 
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split()) 

    def get_tweet_sentiment(self, tweet): 
        # create TextBlob object of passed tweet text 
        analysis = TextBlob(self.clean_tweet(tweet)) 
        # set sentiment 
        if analysis.sentiment.polarity > 0: 
            return 'positive'
        elif analysis.sentiment.polarity == 0: 
            return 'neutral'
        else: 
            return 'negative'

    def get_tweets(self, query, count = 10): 
        # empty list to store parsed tweets 
        tweets = [] 
        try:
            fetched_tweets = self.api.search(q = query, count = count) 
            for tweet in fetched_tweets: 
                parsed_tweet = {}  
                parsed_tweet['text'] = tweet.text  
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text) 
 
                if tweet.retweet_count > 0: 
                    if parsed_tweet not in tweets: 
                        tweets.append(parsed_tweet) 
                else: 
                    tweets.append(parsed_tweet) 

            return tweets 

        except tweepy.TweepError as e: 
            print("Error : " + str(e)) 

def main(): 
    api = TwitterClient() 
    tweets = api.get_tweets(query = 'Donald Trump', count = 200) 
 
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive'] 
    print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets))) 
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative'] 
    print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets))) 
    print("Neutral tweets percentage: {} % \ ".format(100*len(tweets - ntweets - ptweets)/len(tweets))) 

    # printing first 5 positive tweets 
    print("\n\nPositive tweets:") 
    for tweet in ptweets[:10]: 
        print(tweet['text']) 

    # printing first 5 negative tweets 
    print("\n\nNegative tweets:") 
    for tweet in ntweets[:10]: 
        print(tweet['text']) 

if __name__ == "__main__": 
    # calling main function 
    main()

