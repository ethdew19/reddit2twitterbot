import praw
import requests
import os
import re
from os import environ
from tweepy import *

access_token = environ.get('access_token')
access_token_secret = environ.get('secret_access')
consumer_key = environ.get('consumer_key')
consumer_secret = environ.get('consumer_secret')

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = API(auth)


secret = environ.get('secret')
client_id = environ.get('client_id')
user_agent = "Top Post Finder 1.0 by /u/xEquator"

reddit = praw.Reddit(client_id=client_id, client_secret=secret, user_agent=user_agent)

def get_last_tweet():
    timeline = api.user_timeline(tweet_mode ="extended")
    text = timeline[0].full_text
    cleantext = re.sub(r"http\S+", "", text)
    return cleantext

def get_top_post(subreddit):
    last_tweet = get_last_tweet()
    for submission in reddit.subreddit(subreddit).hot(limit=4):
        if not submission.stickied and submission.url.endswith(('jpg', 'jpeg', 'png')) and submission.title + " #gaming " != last_tweet:
            returnurl = submission.url
            returnmessage = submission.title
            return returnurl , returnmessage



def download_and_post(url,message):
    filename = 'temp.jpg'
    request = requests.get(url, stream=True)
    if request.status_code == 200:
        with open(filename, 'wb') as image:
            for chunk in request:
                image.write(chunk)

        api.update_with_media(filename, status=message)
        os.remove(filename)
    else:
        print("Unable to download image")

url,message = get_top_post('programmerhumor')
download_and_post(url,message)

