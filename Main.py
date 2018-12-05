import re
import pandas as pd


def main():
    posDict = getCleanedWordList("trainPos.txt")
    negDict = getCleanedWordList("trainNeg.txt")

    total_word_list = set()
    total_word_list.update(posDict.keys(), negDict.keys())

    totalFreqDict = getFrequency(total_word_list, posDict, negDict)

    print(posDict)


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


def calculateProbabilityOfWord(result):
    result['PosProb'] = result['Positive Freq'] / result['Overall']
    result['NegProb'] = result['Negative Freq'] / result['Overall']

    return result


def getFrequency(total_word_list, posDictionary, negDictionary):
    genOccurenceDict = dict.fromkeys(total_word_list, 0)

    for each in genOccurenceDict.keys():
        if each in posDictionary.keys():
            genOccurenceDict[each] += posDictionary[each]
        if each in negDictionary.keys():
            genOccurenceDict[each] += negDictionary[each]

    return genOccurenceDict


def detProbOfTweet():
    negTestSet = loadTestDataFromFile("testNeg")
    posTestSet = loadTestDataFromFile("testPos")

    negLines = negTestSet.readlines()
    posLines = posTestSet.readLines()


main()
