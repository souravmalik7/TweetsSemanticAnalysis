from textblob import TextBlob
from tabulate import tabulate
import tweepy as tw
from copy import copy as c


# Get tweet text
def get_tweet_text(search_text, tweet_count):
    # access keys and tokens
    api_key = 'RvdLlBeMxI30Kls5W6svSKu9f'
    api_key_secret = 'U9L7qyXHtq1ldjQwp6sFpu8YxWf9fJC8pNVxMXwaDD92weEwMG'
    access_token = '1310153528225144832-YsO9K9XUkfsCm5NEdX5wUCrs5x7Oss'
    access_token_secret = 'zyqpAn0Qem0nrMYXVhxUCnNvVyeK1KxthyLWB7mfF0JQy'

    # authentication
    auth = tw.OAuthHandler(api_key, api_key_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tw.API(auth, wait_on_rate_limit=True)

    tweet_list = []
    results = api.search(q=search_text, lang="en", count=tweet_count)
    for tweet in results:
        tweet_id = tweet.id
        status = api.get_status(tweet_id, tweet_mode="extended")
        try:  # check for the Re-tweet
            tweet_list.append(status.retweeted_status.full_text)
        except AttributeError:  # Not a Re-tweet
            tweet_list.append(status.full_text)
    return tweet_list


# find the match and polarity of the tweet
def get_tweet_polarity(tweets):
    list_of_result = []
    count_of_tweets = 0
    positive_words = 0
    negative_words = 0
    positive_word_list = []
    negative_word_list = []
    for tweet in tweets:
        tweet = remove_emoji(tweet)
        positive_word_list.clear()
        negative_word_list.clear()
        count_of_tweets += 1
        tweet_words = tweet.split()
        for word in tweet_words:
            testimonial = TextBlob(word)
            if testimonial.sentiment.polarity >= 0.5:
                word = remove_special_characters(word)
                positive_word_list.append(word)
                positive_words += 1
            elif testimonial.sentiment.polarity <= -0.5:
                word = remove_special_characters(word)
                negative_word_list.append(word)
                negative_words += 1
        if len(positive_word_list) > len(negative_word_list):
            polarity = "positive"
        elif len(negative_word_list) > len(positive_word_list):
            polarity = "negative"
        else:
            polarity = "neutral"
        row = [count_of_tweets, tweet, c(positive_word_list), c(negative_word_list), polarity]
        list_of_result.append(row)
    return list_of_result


# Print the results
def print_results(list_of_result):
    table = tabulate(list_of_result, headers=['Index', 'Tweet', 'Positive Words', 'Negative Words','Polarity'],
                     tablefmt='fancy_grid')
    print(table)


# Remove special characters
def remove_special_characters(word):
    alphanumeric = ""
    for character in word:
        if character.isalnum():
            alphanumeric += character
    return alphanumeric


# Remove emoji's from the text
def remove_emoji(text):
    return text.encode('ascii', 'ignore').decode('ascii')
