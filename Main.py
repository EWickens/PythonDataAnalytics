import re

from nltk.corpus import stopwords
from nltk import ngrams


def main():
    posDict = getCleanedWordList("trainPos.txt")[0]
    posNgrams = getCleanedWordList("trainPos.txt")[1]
    negDict = getCleanedWordList("trainNeg.txt")[0]
    negNgrams = getCleanedWordList("trainNeg.txt")[1]

    total_word_list = set()
    total_word_list.update(posDict.keys(), negDict.keys())

    totalFreqDict = getFrequency(total_word_list, posDict, negDict)

    posProb = calculateProbabilityOfWord(totalFreqDict, posDict)
    negProb = calculateProbabilityOfWord(totalFreqDict, negDict)

    positiveTweetResults = getProbabilityOfTweet(posProb, negProb, "testPos.txt")
    negativeTweetResults = getProbabilityOfTweet(posProb, negProb, "testNeg.txt")

    print(positiveTweetResults[0])
    print(positiveTweetResults[1])

    print(negativeTweetResults[0])
    print(negativeTweetResults[1])





# Processes the words and outputs a cleaned list
def cleanWords(word_list):
    good_words = re.compile("[^A-Za-z0-9]+")
    good_words = list(filter(lambda bad_word: not good_words.search(bad_word), word_list))
    better_words = remove_stopwords(good_words)
    return better_words


def remove_stopwords(good_words):
    better_words = []
    stop_words = (set(stopwords.words('english')))
    for word in good_words:
        if word not in stop_words:
            better_words.append(word)

    return better_words

def getNgrams(better_words):
    return ngrams(better_words, 2)

# def check_tweet_for_ngrams(tweets, ngrams):
#     occurence = 0
#     for each in tweets:
#         if ngrams in each:
#

def loadTestDataFromFile(name):
    dataFile = open("dataFiles/test/" + name, "r")
    return dataFile


def loadTrainingDataFromFile(name):
    dataFile = open("dataFiles/train/" + name, "r")
    return dataFile


def loadTweetsFromFile(name):
    dataFile = loadTestDataFromFile(name)

    testData = dataFile.read().splitlines()

    return testData


# Returns a dictionary with the individual words + Frequency at which they occur within the dataset
def getCleanedWordList(name):
    data = loadTrainingDataFromFile(name)

    # Makes each word lowercase
    dataRead = data.read().lower()

    dataSplit = dataRead.split()

    cleaned_words = cleanWords(dataSplit)

    ngrams = getNgrams(cleaned_words)

    dictionary = dict.fromkeys(set(cleaned_words), 0)

    # Calculates the frequency of each word in the dataset.
    for each in cleaned_words:
        dictionary[each] += 1

    return [dictionary,ngrams]


def clean_string(string):
    string = re.sub(r"[;?<>,\"|:.`~{\}\\/@$%\[\]()^\-+&#*!_=]*", "", string)
    return string


def getProbabilityOfTweet(posProb, negProb, filename):
    data_set = loadTweetsFromFile(filename)
    posTweetCounter = 0
    negTweetCounter = 0

    posWordProb = 0
    negWordProb = 0

    for tweet in data_set:
        clean_tweet = clean_string(tweet.lower())

        for word in clean_tweet.split():
            if word in posProb.keys():
                posWordProb += posProb[word]
            if word in negProb.keys():
                negWordProb += negProb[word]

        if posWordProb > negWordProb:
            posTweetCounter += 1
        else:
            negTweetCounter += 1

    return [posTweetCounter, negTweetCounter]


# def getProbabilityOfTweet(posProb, negProb):
#     tweets = loadTweetsFromFile("testPos.txt")
#     # negTweetProbLines = loadTweetsFromFile("testNeg.txt")
#     print(len(tweets))
#     posTweetCounter = 0
#     negTweetCounter = 0
#
#     posClassDictionary = dict.fromkeys(tweets, 1)
#     negClassDictionary = dict.fromkeys(tweets, 1)
#
#     for line in tweets:  # For each tweet
#
#         for word in line:  # For each word
#             word = clean_string(word.lower())  # Cleans tweet to compare it with cleaned words.
#             if word in posProb.keys():  # if word is in the positive dictionary
#                 posClassDictionary[line] = posClassDictionary[line] * posProb[word]  # multiply the value of the tweet by the value of the word
#                 # print(posClassDictionary[line])
#             if word in negProb.keys():  # if word is in the positive dictionary
#                 negClassDictionary[line] = negClassDictionary[line] * negProb[word]  # multiply the value of the tweet by the value of the word
#                 # print(negClassDictionary[line])
#
#         # print(negClassDictionary[line])
#         if posClassDictionary[line] > negClassDictionary[line]:
#             posTweetCounter += 1
#         else:
#             negTweetCounter += 1
#
#     print(posTweetCounter)
#     print(negTweetCounter)


# def getSingleTweetProb(line, posProb, negProb, posClassDictionary, negClassDictionary):
#     posTweetCounter = 0
#     negTweetCounter = 0
#
#     for word in line:  # For each word
#         word = clean_string(word.lower())  # Cleans tweet to compare it with cleaned words.
#         if word in posProb.keys():  # if word is in the positive dictionary
#             posClassDictionary[line] = posClassDictionary[line] * posProb[word]  # multiply the value of the tweet by the value of the word
#             # print(posClassDictionary[line])
#         if word in negProb.keys():  # if word is in the positive dictionary
#             negClassDictionary[line] = negClassDictionary[line] * negProb[word]  # multiply the value of the tweet by the value of the word
#             # print(negClassDictionary[line])
#
#     # print(negClassDictionary[line])
#     if posClassDictionary[line] > negClassDictionary[line]:
#         posTweetCounter += 1
#     else:
#         negTweetCounter += 1
#
#     return [posTweetCounter, negTweetCounter]


def getFrequency(total_word_list, posDictionary, negDictionary):
    genOccurenceDict = dict.fromkeys(total_word_list, 0)

    for word in genOccurenceDict.keys():
        if word in posDictionary.keys():
            genOccurenceDict[word] += posDictionary[word]
        if word in negDictionary.keys():
            genOccurenceDict[word] += negDictionary[word]

    return genOccurenceDict


def calculateProbabilityOfWord(totalFreqDictionary, dictionary):  # WORKING AS INTENDED
    probabilityDictionary = dict.fromkeys(totalFreqDictionary, 0)

    for each in probabilityDictionary:
        if each in dictionary.keys():
            probabilityDictionary[each] = dictionary[each] / totalFreqDictionary[each]

    return probabilityDictionary


main()
