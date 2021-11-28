import datetime as dt
import pandas as pd
import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import snscrape.modules.twitter as sntwitter
import nltk

# Download using the below method as it works in case of JUPYTER
# nltk.download('vader_lexicon')
# For downloading using Python editor, download it from http://www.nltk.org/nltk_data/ and save unzipped content at :
# Windows: C:\nltk_data\tokenizers
# OSX: /usr/local/share/nltk_data/tokenizers
# Unix: /usr/share/nltk_data/tokenizers
#


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


def _get_tweets_in_df(search_query, no_of_tweets, no_of_days):
    query = search_query

    # As long as the query is valid (not empty or equal to '#')...
    if query != '':
        if no_of_tweets != '':
            if no_of_days != '':
                # Creating list to append tweet data
                tweets_list = []
                now = dt.date.today()
                now = now.strftime('%Y-%m-%d')
                start_day = dt.date.today() - dt.timedelta(days=int(no_of_days))
                start_day = start_day.strftime('%Y-%m-%d')
                for i, tweet in enumerate(sntwitter.TwitterSearchScraper(
                        query + ' lang:en since:' + start_day + ' until:' + now + ' -filter:links -filter:replies').get_items()):
                    if i > int(no_of_tweets):
                        break
                    tweets_list.append([tweet.date, tweet.content, tweet.username])

                # Creating a dataframe from the tweets list above
                df = pd.DataFrame(tweets_list, columns=['Datetime', 'Text', 'Username'])

                # applying this function to Text column of our dataframe
                df["Text"] = df["Text"].apply(cleanTxt)
                return df
    return None


def _percentage(part,whole):
    return 100 * float(part)/float(whole)


def _set_sentiment_for_day_range(search_query, no_of_tweets, no_of_days):
    # Assigning Initial Values
    positive = 0
    negative = 0
    neutral = 0
    # Creating empty lists
    tweet_list1 = []
    neutral_list = []
    negative_list = []
    positive_list = []
    sentiment_df = _get_tweets_in_df(search_query, no_of_tweets, no_of_days)
    sentiment_df["Sentiment"] = ""
    sentiment_df['Date'] = pd.to_datetime(sentiment_df['Datetime']).dt.date
    # Iterating over the tweets in the dataframe
    # for tweet in df['Text']:
    for i, row in sentiment_df.iterrows():
        tweet = row['Text']
        tweet_list1.append(tweet)
        analyzer = SentimentIntensityAnalyzer().polarity_scores(tweet)
        neg = analyzer['neg']
        neu = analyzer['neu']
        pos = analyzer['pos']
        comp = analyzer['compound']

        if neg > pos:
            negative_list.append(tweet)  # appending the tweet that satisfies this condition
            negative += 1  # increasing the count by 1
            sentiment_df.at[i, 'Sentiment'] = 'neg'
        elif pos > neg:
            positive_list.append(tweet)  # appending the tweet that satisfies this condition
            positive += 1  # increasing the count by 1
            sentiment_df.at[i, 'Sentiment'] = 'pos'
        elif pos == neg and pos < neu:
            negative_list.append(tweet)  # appending the tweet that satisfies this condition
            negative += 1  # increasing the count by 1
            sentiment_df.at[i, 'Sentiment'] = 'neg'
        elif pos == neg and pos > neu:
            positive_list.append(tweet)  # appending the tweet that satisfies this condition
            positive += 1  # increasing the count by 1
            sentiment_df.at[i, 'Sentiment'] = 'pos'
        elif pos == neg and round(pos, 0) == round(neu, 0):
            neutral_list.append(tweet)  # appending the tweet that satisfies this condition
            neutral += 1  # increasing the count by 1
            sentiment_df.at[i, 'Sentiment'] = 'neu'
    return sentiment_df


def _get_top_sentiment(g):
    return g['Sentiment'].value_counts().idxmax()


def _get_sentiment_count(g):
    top_sentiment = _get_top_sentiment(g)
    sentiment_tuple = g['Sentiment'].value_counts()

    total_count = sentiment_tuple.sum()
    highest_count = sentiment_tuple[0]
    return top_sentiment, highest_count / total_count


def get_datewise_sentiment(search_query, no_of_tweets, no_of_days):
    sentiment_df = _set_sentiment_for_day_range(search_query, no_of_tweets, no_of_days)
    if sentiment_df.empty:
        return sentiment_df
    else:
        date_wise_sentiment = sentiment_df.groupby(['Date']).apply(_get_sentiment_count).reset_index()
        date_wise_sentiment[['Sentiment', 'Percentage']] = pd.DataFrame(date_wise_sentiment[0].tolist(),
                                                                          index=date_wise_sentiment.index)
        print(date_wise_sentiment)
        return date_wise_sentiment
