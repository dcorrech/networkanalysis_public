# Scrape tweets with tweaking new method: https://www.geeksforgeeks.org/extraction-of-tweets-using-tweepy/

import tweepy
import csv
import json

# load Twitter API credentials

consumer_key = 'xxxxxxxxxxxxxxxxxxx'
consumer_secret = 'xxxxxxxxxxxxxxxxxxx'
access_token = 'xxxxxxxxxxxxxxxxxxx'
access_secret = 'xxxxxxxxxxxxxxxxxxx'

# Function to extract tweets 
def get_tweets(username): 
          
    # Authorization to consumer key and consumer secret 
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
  
    # Access to user's access key and access secret 
    auth.set_access_token(access_token, access_secret) 
  
    # Calling api 
    api = tweepy.API(auth) 
  
    tweets = api.user_timeline(username) 
  
    # create array of tweet information: username,  
    # tweet id, date/time, text 
    tweets_for_csv = [[tweet.id_str, tweet.created_at,
    tweet.text.encode('utf-8')] for tweet in tweets] # CSV file created  

    # writing to the csv file

    with open(username + '_tweets.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'created_at', 'text'])
        writer.writerows(tweets_for_csv)
  
        
    
# Driver code 
if __name__ == '__main__': 
    mp_handles = []
    with open('mp_twitter.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            mp_handles.append(row[0])
  
    # Run get_tweets for all MPs
    for handle in mp_handles:
        print('Scraping ' + handle)
        get_tweets(handle)
        print('Finished ' + handle)
    print('Done scraping tweets')