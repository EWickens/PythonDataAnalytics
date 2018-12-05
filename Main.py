import re
import pandas as pd


def main():
    posDict = getCleanedWordList("trainPos.txt")
    negDict = getCleanedWordList("trainNeg.txt")

    total_word_list = set()
    total_word_list.update(posDict.keys(), negDict.keys())

    totalFreqDict = getFrequency(total_word_list, posDict, negDict)

    posProb = calculateProbabilityOfWord(totalFreqDict, posDict)
    negProb = calculateProbabilityOfWord(totalFreqDict, negDict)

# Processes the words and outputs a cleaned list
def cleanWords(word_list):
    good_words = re.compile("[^A-Za-z0-9]+")
    return list(filter(lambda bad_word: not good_words.search(bad_word), word_list))


def loadTestDataFromFile(name):
    dataFile = open("dataFiles/test/" + name, "r")
    return dataFile;


def loadTrainingDataFromFile(name):
    dataFile = open("dataFiles/train/" + name, "r")
    return dataFile;

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

    dictionary = dict.fromkeys(set(cleaned_words), 0)

    # Calculates the frequency of each word in the dataset.
    for each in cleaned_words:
        dictionary[each] += 1

    return dictionary


def getProbabilityOfTweet(negProb, posProb):
    posTweetLines = loadTweetsFromFile("testPos")
    negTweetLines = loadTweetsFromFile("testNeg")

    posTweetCounter = 0
    negTweetCounter = 0

    posClassDictionary = dict.fromkeys(posTweetLines)
    negClassDictionary = dict.fromkeys(negTweetLines)

    for line in negTweetLines: # For each tweet
        cleaned_tweet = cleanWords(line.split()) # Cleans tweet to compare it with cleaned words.

        for word in cleaned_tweet: # For each word

            if word in posProb.keys(): # if word is in the positive dictionary
                posTweetLines[line] *= posProb[word] # multiply the value of the tweet by the value of the word
            if word in negProb.keys():# if word is in the positive dictionary
                negTweetLines[line] *= negProb[word] # multiply the value of the tweet by the value of the word

    if posTweetLines[line] >= negTweetLines[line]:
        posTweetCounter += 1
    else:
        negTweetCounter += 1

def getFrequency(total_word_list, posDictionary, negDictionary):
    genOccurenceDict = dict.fromkeys(total_word_list, 0)

    for each in genOccurenceDict.keys():
        if each in posDictionary.keys():
            genOccurenceDict[each] += posDictionary[each]
        if each in negDictionary.keys():
            genOccurenceDict[each] += negDictionary[each]

    return genOccurenceDict


def calculateProbabilityOfWord(totalFreqDictionary, dictionary):
    probabilityDictionary = dict.fromkeys(totalFreqDictionary, 0)

    for each in probabilityDictionary:
        if each in dictionary.keys():
            probabilityDictionary[each] = dictionary[each] / totalFreqDictionary[each]

    return probabilityDictionary


main()
