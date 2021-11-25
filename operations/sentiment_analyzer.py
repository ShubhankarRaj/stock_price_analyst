import datetime as dt
import numpy as np
import pandas as pd
import snscrape.modules.twitter as sntwitter
import re


def cleanTxt(text):
    """
    Function to clean the tweets
    :param text:
    :return:
    """
    text = re.sub('@[A-Za-z0–9]+', '', text) #Removing @mentions
    text = re.sub('#', '', text) # Removing '#' hash tag
    text = re.sub('RT[\s]+', '', text) # Removing RT
    text = re.sub('https?:\/\/\S+', '', text) # Removing hyperlink
    return text


def get_tweets(search_query, no_of_tweets, no_of_days):
    query = search_query

    # As long as the query is valid (not empty or equal to '#')...
    if query != '':
        noOfTweet = input("Enter the number of tweets you want to Analyze: ")
        if noOfTweet != '':
            noOfDays = input("Enter the number of days you want to Scrape Twitter for: ")
            if noOfDays != '':
                # Creating list to append tweet data
                tweets_list = []
                now = dt.date.today()
                now = now.strftime('%Y-%m-%d')
                start_day = dt.date.today() - dt.timedelta(days=int(noOfDays))
                start_day = start_day.strftime('%Y-%m-%d')
                for i, tweet in enumerate(sntwitter.TwitterSearchScraper(
                        query + ' lang:en since:' + start_day + ' until:' + now + ' -filter:links -filter:replies').get_items()):
                    if i > int(noOfTweet):
                        break
                    tweets_list.append([tweet.date, tweet.content, tweet.username])

                # Creating a dataframe from the tweets list above
                df = pd.DataFrame(tweets_list, columns=['Datetime', 'Text', 'Username'])

                # applying this function to Text column of our dataframe
                df["Text"] = df["Text"].apply(cleanTxt)
                return df
    return None


