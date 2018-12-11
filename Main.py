import re

from nltk.corpus import stopwords
from nltk import ngrams
import time


def main():
    start = time.time()

    posDict = getCleanedWordList("trainPos.txt")[0]
    negDict = getCleanedWordList("trainNeg.txt")[0]

    total_word_list = set()
    total_word_list.update(posDict.keys(), negDict.keys())

    totalFreqDict = getFrequency(total_word_list, posDict, negDict)

    posProb = calculateProbabilityOfWord(totalFreqDict, posDict)
    negProb = calculateProbabilityOfWord(totalFreqDict, negDict)

    positiveTweetResults = getProbabilityOfTweet(posProb, negProb, "testPos.txt")
    negativeTweetResults = getProbabilityOfTweet(posProb, negProb, "testNeg.txt")

    calculateAccuracy(positiveTweetResults, negativeTweetResults, start)


def remove_stopwords(good_words):
    better_words = []
    stop_words = (set(stopwords.words('english')))
    for word in good_words:
        if word not in stop_words:
            better_words.append(word)

    return better_words


def getNgrams(better_words):
    return ngrams(better_words, 2)

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

    cleaned_words = []

    for each in dataSplit:
        cleaned_words.append(clean_string(each))

    dictionary = dict.fromkeys(set(cleaned_words), 0)

    # Calculates the frequency of each word in the dataset.
    for each in cleaned_words:
        dictionary[each] += 1

    return [dictionary]


def clean_string(string):
    string = re.sub(r"[;?<>,\"|:.`~{\}\\/@$%\[\]()^\-+&#*!_=]*", "", string)
    return string


def getProbabilityOfTweet(posProb, negProb, filename):
    data_set = loadTweetsFromFile(filename)
    posTweetCounter = 0
    negTweetCounter = 0

    for tweet in data_set:

        posWordProb = 1
        negWordProb = 1

        clean_tweet = clean_string(tweet.lower())

        for word in clean_tweet.split():
            if word in posProb:
                posWordProb = posWordProb * posProb[word]
            if word in negProb:
                negWordProb = negWordProb * negProb[word]

        if posWordProb >= negWordProb:
            posTweetCounter += 1
        else:
            negTweetCounter += 1

    return [posTweetCounter, negTweetCounter]


def getFrequency(total_word_list, posDictionary, negDictionary):
    genOccurrenceDict = dict.fromkeys(total_word_list, 0)

    for each in genOccurrenceDict.keys():
        if each in posDictionary.keys():
            genOccurrenceDict[each] += posDictionary[each]
        if each in negDictionary.keys():
            genOccurrenceDict[each] += negDictionary[each]

    return genOccurrenceDict


def calculateProbabilityOfWord(totalFreqDictionary, dictionary):  # WORKING AS INTENDED
    probabilityDictionary = dict.fromkeys(totalFreqDictionary, 0)

    for each in probabilityDictionary:
        if each in dictionary.keys():
            probabilityDictionary[each] = (dictionary[each] + 1) / (
                        totalFreqDictionary[each] + len(totalFreqDictionary))
        else:
            probabilityDictionary[each] = 1 / (totalFreqDictionary[each] + len(totalFreqDictionary))

    return probabilityDictionary


def calculateAccuracy(positiveTweetResults, negativeTweetResults, start):
    print("Time taken to complete in seconds: " + str((time.time() - start)))

    totalAVG = ((positiveTweetResults[0] + negativeTweetResults[1]) / 2) / 10

    print("\nPositive Test Data: ")
    print("\tPositive Accuracy: " + str(positiveTweetResults[0] / 10) + "%")
    print("\tNegative Accuracy: " + str(positiveTweetResults[1] / 10) + "%\n")

    print("Negative Test Data: ")
    print("\tPositive Accuracy: " + str(negativeTweetResults[0] / 10) + "%")
    print("\tNegative Accuracy: " + str(negativeTweetResults[1] / 10) + "%\n")

    print("Total Average Accuracy: " + str(totalAVG) + "%")


main()
