from collections import Counter
import pandas as pd


def main():
    posUnique = getUniqueWordsFromList("trainPos.txt")
    negUnique = getUniqueWordsFromList("trainNeg.txt")

    # total_word_list = posUnique.union(negUnique)

    posDict = getFreqOfWords("trainPos.txt")
    negDict = getFreqOfWords("trainNeg.txt")

    posDataFrame = pd.DataFrame(list(posDict.items()), columns=['Word', 'Positive Freq'])
    negDataFrame = pd.DataFrame(list(negDict.items()), columns=['Word', 'Negative Freq'])

    #Merges the two dataframes to get a joined list with both positive and negative words.

    result = pd.merge(posDataFrame, negDataFrame, on='Word', how='outer')

    #Replaces the nulls with 0
    result = result.fillna(0)

    #Adds a third column to the dataframe which is the overall result of the word to determine if its classed as positive or negative.
    result['Overall'] = result['Positive Freq'] + result['Negative Freq']



    result = calculateProbabilityOfWord(result)
    print(result)


def loadTestDataFromFile(name):
    dataFile = open("dataFiles/test/" + name, "r")
    return dataFile;

def loadTrainingDataFromFile(name):
    dataFile = open("dataFiles/train/" + name, "r")
    return dataFile;



def getUniqueWordsFromList(name):
    data = loadTrainingDataFromFile(name)
    vocab = set();

    dataRead = data.read()
    splitData = dataRead.split()

    for word in splitData:
        vocab.add(word)

    return vocab;

# Returns a dictionary with the individual words + Frequency at which they occur within the dataset
def getFreqOfWords(name):
    data = loadTrainingDataFromFile(name)
    dataRead = data.read()

    dictionary = dict(Counter(dataRead.split()))

    return dictionary;

def calculateProbabilityOfWord(result):
    result['PosProb'] = result['Positive Freq'] / result['Overall']
    result['NegProb'] = result['Negative Freq'] / result['Overall']

    return result

def detProbOfTweet(result):
    negTestSet = loadTestDataFromFile("testNeg")
    posTestSet = loadTestDataFromFile("testPos")

    negLines = negTestSet.readlines()
    posLines = posTestSet.readLines()



main()