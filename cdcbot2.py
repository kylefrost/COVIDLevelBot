import tweepy
import json
import requests
import logging
import time

import credentials
from cdcdata import CDCData

consumer_key = credentials.API_key
consumer_secret_key = credentials.API_secret_key
access_token = credentials.access_token
access_token_secret = credentials.access_token_secret

auth = tweepy.OAuthHandler(consumer_key, consumer_secret_key)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

cdcdata = CDCData()

# For adding logs in application
logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)
logger.setLevel(logging.INFO)

def get_data(tweet):
    try:
        tw = tweet.full_text.split(' ', 1)[-1]
        county_state = ""

        if ',' in tw:
            county_state = [x.strip() for x in tw.split(',')]
            if len(county_state) != 2:
                return 1, 0
        else:
            return 2, 0
        
        current_status = cdcdata.get_current_status(county_state[0], county_state[1])

        current_version = cdcdata.get_current_version()

        return current_status, current_version
    except:
        return 3, 0


def get_last_tweet(file):
    f = open(file, 'r')
    lastId = int(f.read().strip())
    f.close()
    return lastId

def put_last_tweet(file, Id):
    f = open(file, 'w')
    f.write(str(Id))
    f.close()
    logger.info("Updated the file with the latest tweet Id")
    return

def respondToTweet(file=credentials.file):
    last_id = get_last_tweet(file)
    mentions = api.mentions_timeline(last_id, tweet_mode='extended')
    if len(mentions) == 0:
        return

    new_id = 0
    logger.info("Someone mentioned me...")

    for mention in reversed(mentions):
        if not mention.full_text.startswith('@COVIDLevelBot'):
            pass
        logger.info(str(mention.id) + '-' + mention.full_text)
        new_id = mention.id
        response = ""

        status, version = get_data(mention)

        if status == 1:
            response = "Sorry, that tweet looks invalid. Please check that the format is \"County, State\" (without quotes) and try again."
        elif status == 2:
            reponse = "Please separate the County and State with a comma like this: County, State."
        elif status == 3:
            response = "Sorry, an unknown error occured. Please check that your tweet format is \"County, State\" (without quotes) and try again."
        else:
            response = "The COVID-19 Community Level for your County is " + status + ", last updated " + version + "."

        logger.info("Responding to {}".format(mention.id))
        try:
            logger.info("Liking and replying to tweet")

            api.create_favorite(mention.id)
            api.update_status('@' + mention.user.screen_name + " " + response, mention.id)
        except:
            logger.info("Already replied to {}".format(mention.id))

    put_last_tweet(file, new_id)

if __name__=="__main__":
    while True:
        respondToTweet()
        time.sleep(30)
