from collections import Counter
import pandas as pd


def main():
    posUnique = getUniqueWordsFromList("testPos.txt")
    negUnique = getUniqueWordsFromList("testNeg.txt")

    # total_word_list = posUnique.union(negUnique)

    posDict = getFreqOfWords("testPos.txt")
    negDict = getFreqOfWords("testNeg.txt")

    posDataFrame = pd.DataFrame(list(posDict.items()), columns=['Word', 'Positive Freq'])
    negDataFrame = pd.DataFrame(list(negDict.items()), columns=['Word', 'Negative Freq'])

    #Merges the two dataframes to get a joined list with both positive and negative words.

    result = pd.merge(posDataFrame, negDataFrame, on='Word', how='outer')

    #Adds a third column to the dataframe which is the overall result of the word to determine if its classed as positive or negative.
    result['Overall'] = result['Positive Freq'] - result['Negative Freq']

    print(result)


def loadDataFromFile(name):
    dataFile = open("dataFiles/test/" + name, "r")
    return dataFile;


def getUniqueWordsFromList(name):
    data = loadDataFromFile(name)
    vocab = set();

    dataRead = data.read()
    splitData = dataRead.split()

    for word in splitData:
        vocab.add(word)

    return vocab;


def getFreqOfWords(name):
    data = loadDataFromFile(name)
    dataRead = data.read()

    dictionary = dict(Counter(dataRead.split()))

    return dictionary;


main()
