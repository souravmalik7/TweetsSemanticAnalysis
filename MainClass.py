from FunctionsClass import *


# Main script
def tweet_polarity():
    tweets = get_tweet_text("#fitness", 100)
    list_of_result = get_tweet_polarity(tweets)
    print_results(list_of_result)


if __name__ == '__main__':
    tweet_polarity()
