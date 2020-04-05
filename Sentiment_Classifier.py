import pathlib

def strip_punctuation(string):
    '''
        removes random characters from a string

        :param:
            string (string): string to be cleaned up

        :return:
            stripped_word (string): string with random character and punctuation removed
    '''

    punctuation_chars = ["'", '"', ",", ".", "!", ":", ";", '#', '@']
    stripped_string = string

    # remove any random characters from string
    for char in stripped_string:
        if char in punctuation_chars:
            stripped_string = stripped_string.replace(char, "")

    return stripped_string


def get_pos(sentence):
    '''
        compares each word to a list of 'positive' words

        :param:
            sentence (string): sentence from a twitter message

        :return:
            positive_count (int): number of positive words
    '''
    positive_count = 0

    # lists of words with positive connotation
    positive_words = []
    with open("positive_words.txt") as pos_f:
        for lin in pos_f:

            if lin[0] != ';' and lin[0] != '\n':
                positive_words.append(lin.strip())


    for word in sentence.split():
        # remove random chars and capitalization
        if strip_punctuation(word).lower() in positive_words:
            # count number of positive words
            positive_count += 1

    return positive_count


def get_neg(sentence):
    '''
        compares each word to a list of 'negative' words

        :param:
            sentence (string): sentence from a twitter message

        :return:
            negative_count (int): number of negative words
    '''
    negative_count = 0

    # lists of negative words to use
    negative_words = []
    with open("negative_words.txt") as pos_f:
        for lin in pos_f:

            if lin[0] != ';' and lin[0] != '\n':
                negative_words.append(lin.strip())

    for word in sentence.split():
        # remove random chars and capitalization
        if strip_punctuation(word).lower() in negative_words:
            # count number of negative words
            negative_count += 1

    return negative_count


def sentiment_classifier(tweets):
    tweet_meta_data = []

    for tweet in tweets:
        tweet_meta_data.append("{retweets}, {replies}, {positive}, {negative}, {net}\n".
                               format(retweets=tweet[1],
                                      replies=tweet[2],
                                      positive=get_pos(tweet[0]),
                                      negative=get_neg(tweet[0]),
                                      net=get_pos(tweet[0]) - get_neg(tweet[0])))

    return tweet_meta_data


# pull twitter data from file
with open(pathlib.Path.cwd() / "project_twitter_data.csv") as twitter_file:
    file_lines = twitter_file.readlines()
    tweets = []

    for line in file_lines[1:]:
        tweets.append(line.strip().split(","))

    print(tweets)


# write twitter meta data into csv file
with open(pathlib.Path.cwd() / "resulting_data.csv", "w") as csv_file:
    twitter_meta_data = sentiment_classifier(tweets)

    # write header line
    csv_file.write("Number of Retweets, Number of Replies, Positive Score, Negative Score, Net Score\n")

    # write twitter meta data
    for line in twitter_meta_data:
        csv_file.write(line)
        print(line)
