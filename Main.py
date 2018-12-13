# Eoin Wickens
# Student Number: R00151204
# Email: eoin.wickens@mycit.ie

import re  # Regex Import
from nltk.corpus import stopwords  # Stopwords list import
from nltk import ngrams  # ngrams import
import time  # Time library import
import matplotlib.pyplot as matplotlib  # MatPotLib Graphing import


def main():
    print("Unprocessed Data\n")
    # Runs the program without the words being cleaned
    preProcessedAVG = calculateProbabilityToggle(False)

    print("\n\nProcessed Data\n")
    # Runs the program with the words being cleaned
    postProcessedAVG = calculateProbabilityToggle(True)

    # Displays a graph of the pre and post processed reports
    displayGraph(preProcessedAVG, postProcessedAVG)


# This function runs the program with or without postprocessing based on the boolean passed in.
def calculateProbabilityToggle(clean):
    start_time = time.time()  # Takes the time at the beginning of the function

    # Gets the training datasets and only cleans the words if the boolean is True
    posDict = getCleanedWordList("trainPos.txt", clean)
    negDict = getCleanedWordList("trainNeg.txt", clean)

    # Initializes a set
    total_word_list = set()
    # Gets the words of both the positive and negative dictionary and creates a set of all the words combined.
    total_word_list.update(posDict.keys(), negDict.keys())

    # Gets the total frequency of each of the words in both tables
    totalFreqDict = getFrequency(total_word_list, posDict, negDict)

    # Calculates the probability of the positive words in the dictionary
    posProb = calculateProbabilityOfWord(totalFreqDict, posDict)
    # Calculates the probability of the negative words in the dictionary
    negProb = calculateProbabilityOfWord(totalFreqDict, negDict)

    # Calculates the probability of all the tweets in the
    positiveTweetResults = getProbabilityOfTweet(posProb, negProb, "testPos.txt", clean)
    negativeTweetResults = getProbabilityOfTweet(posProb, negProb, "testNeg.txt", clean)

    # Calculates the total average between the positive accuracy of the positive file and the negative accuracy of
    # the negative file
    totalAVG = calculateAccuracy(positiveTweetResults, negativeTweetResults)

    # Calculates the time taken from the start of the function to the end of the function to complete.
    time_taken = (time.time() - start_time)

    print("Time taken to complete in seconds: " + str(time_taken))

    # Returns the total average for the graphing function.
    return totalAVG


# This function receives the cleaned list and proceeds to check it against the stop word list
# If the words in the list are not in the new list, add the word to the better_words list

def remove_stopwords(good_words):
    better_words = []
    stop_words = (set(stopwords.words('english')))  # Creates a set of all the stop words to check against

    for word in good_words:
        if word not in stop_words:
            better_words.append(word)

    return better_words  # Returns the cleaned words


# This function is implemented but not used due to accuracy already being over 75%
def getNgrams(better_words):
    return ngrams(better_words, 2)


# Loads the test data from the file
def loadTestDataFromFile(name):
    dataFile = open("dataFiles/test/" + name, "r")
    return dataFile


# Loads the training data from the file
def loadTrainingDataFromFile(name):
    dataFile = open("dataFiles/train/" + name, "r")
    return dataFile


# loads the tweets from the file
def loadTweetsFromFile(name):
    dataFile = loadTestDataFromFile(name)

    # Splits the file on the line to separate out each tweet.
    testData = dataFile.read().splitlines()

    return testData


# Returns a dictionary with the individual words + Frequency at which they occur within the dataset
def getCleanedWordList(name, clean):
    data = loadTrainingDataFromFile(name)

    # Makes each word lowercase
    dataRead = data.read().lower()

    # Gets each word on its own
    dataSplit = dataRead.split()

    cleaned_words = []

    if clean:  # If the clean variable is set to true, then start preprocessing

        for each in dataSplit:
            cleaned_words.append(clean_string(each))  # Adds each cleaned word to the cleaned_word list

        # Removes stop words
        better_words = remove_stopwords(cleaned_words)

        # Generates a dictionary from the set of the cleaned words
        dictionary = dict.fromkeys(set(better_words), 0)

        # Calculates the frequency of each word in the dataset.
        for each in better_words:
            dictionary[each] += 1

    else:  # Dont clean the words
        dictionary = dict.fromkeys(set(dataSplit), 0)
        for each in dataSplit:
            dictionary[each] += 1

    return dictionary


# This function removes any of the specified strings from the string
def clean_string(string):
    string = re.sub(r"[;?<>,\"|:.`~{\}\\/@$%\[\]()^\-+&#*!_=]*", "", string)
    return string


# This function works out if a tweet has an overall positive or negative probability
def getProbabilityOfTweet(posProb, negProb, filename, clean):
    data_set = loadTweetsFromFile(filename)
    posTweetCounter = 0
    negTweetCounter = 0

    for tweet in data_set:
        # Sets the probability of each word as 1 initially to not multiply by 0
        posWordProb = 1
        negWordProb = 1

        if clean:  # If the clean boolean is true, clean each tweet
            clean_tweet = clean_string(tweet.lower())
        else:  # Dont clean the tweet
            clean_tweet = tweet.lower()

        for word in clean_tweet.split():
            if word in posProb:
                posWordProb *= posProb[word]  # Multiply the probability of each word together
            if word in negProb:
                negWordProb *= negProb[word]

        # If the positive probability of the tweet is greater or equal to the negative probability
        if posWordProb >= negWordProb:
            posTweetCounter += 1  # Increment the counter by 1
        else:
            negTweetCounter += 1

    return [posTweetCounter, negTweetCounter]


# Calculates the overall frequency of each word
def getFrequency(total_word_list, posDictionary, negDictionary):
    genOccurrenceDict = dict.fromkeys(total_word_list, 0)

    print("Total Words: " + str(len(total_word_list)))
    # For each word in the dictionary of every word
    for each in genOccurrenceDict.keys():
        if each in posDictionary.keys():
            genOccurrenceDict[each] += posDictionary[
                each]  # Adds the occurrence of each word into the general dictionary
        if each in negDictionary.keys():
            genOccurrenceDict[each] += negDictionary[each]

    return genOccurrenceDict


# Calculates the probability of each word - this is a generic function and works for both positive and negative
# dictionaries
def calculateProbabilityOfWord(totalFreqDictionary, dictionary):
    # Generates an empty dictionary with all of the words
    probabilityDictionary = dict.fromkeys(totalFreqDictionary, 0)

    for each in probabilityDictionary:
        if each in dictionary.keys():
            probabilityDictionary[each] = (dictionary[each] + 1) / (  # Increments each occurence value the dictionary
                #  by one to remove any 0 occurences
                    totalFreqDictionary[each] + len(totalFreqDictionary))  # Divides each value in the dictionary by
            # the total occurence of the word added to the length of all words in the dictionary
        else:  # If the word isn't in the dictionary
            probabilityDictionary[each] = 1 / (totalFreqDictionary[each] + len(totalFreqDictionary))  # 1 is divided
            # by the total occurence of the word added to the length of all words in the dictionary

    return probabilityDictionary  # Return the probability dictionary


# Takes the pos and neg tweet results in, and calculates the probability of each word Since each tweet file is 1000
# tweets, I divide each of the results by 1000, and multiply it by 100 to get the percentage accuracy

def calculateAccuracy(positiveTweetResults, negativeTweetResults):
    total_length_tweets = positiveTweetResults[0] + positiveTweetResults[1]  # Gets the total number of tweets in the file

    # Calculates the average of the positive results from the positive dataset and the negative accuracy of the
    # negative dataset
    totalAVG = (((positiveTweetResults[0] + negativeTweetResults[1]) / 2) / total_length_tweets) * 100

    # Prints out the accuracy data
    print("\nPositive Test Data: ")
    print("\tPositive Accuracy: " + str((positiveTweetResults[0] / total_length_tweets) * 100) + "%")
    print("\tNegative Accuracy: " + str((positiveTweetResults[1] / total_length_tweets) * 100) + "%\n")

    print("Negative Test Data: ")
    print("\tPositive Accuracy: " + str((negativeTweetResults[0] / total_length_tweets) * 100) + "%")
    print("\tNegative Accuracy: " + str((negativeTweetResults[1] / total_length_tweets) * 100) + "%\n")

    print("Total Average Accuracy: " + str(totalAVG) + "%")

    # Returns the total average
    return totalAVG


# Uses matplotlib to display a graph of processed and preprocessed data
def displayGraph(unprocessedAccuracy, preprocessedAccuracy):
    y_axis = [0, 100]  # Sets the range of the y axis to 0 - 100

    types = ("UnprocessedAccuracy", "PreProcessed Accuracy")  # Sets the bar titles

    # Sets the plot values as the total avg of both the processed and unprocessed data
    plot_values = [unprocessedAccuracy, preprocessedAccuracy]

    # Creates the bar chart
    matplotlib.bar(y_axis, plot_values, align='center', alpha=1)

    # Sets the ticks to be y axis and types
    matplotlib.xticks(y_axis, types)

    matplotlib.ylabel("Accuracy")  # Labels Y axis
    matplotlib.xlabel("Data")  # Labels X axis

    matplotlib.title("Accuracy of Pre vs Post Processing Data")  # Sets the title of the bar chart

    matplotlib.show()  # Displays the bar chart


main()
