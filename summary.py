import datetime
from pandas_datareader import data
import pandas as pd
from datetime import date

lowDates = []
lowPer = []
lowClose = []
posLow = []
highDates = []
highPer = []
highClose = []
posHigh = []
path = ''
setPercentage = 3.4
filePath = ''


# define global var, values = percentage moved in a day, pos = position in list, Dates = date of low or high movements
def filterByYear(setYear):
    global lowPer, highPer, posLow, posHigh, lowDates, highDates, highClose, lowClose
    originalHigh = len(posHigh)
    originalLow = len(posLow)
    csv_input = pd.read_csv(path)
    countLow = countHigh = 0
    yearList = csv_input['Year']
    dateList = csv_input['Date']
    for x in posLow:
        if yearList[x] < setYear:
            countLow += 1
    for x in posHigh:
        if yearList[x] < setYear:
            countHigh += 1
    if countLow != 0:
        posLow = posLow[countLow:]
        lowPer = lowPer[countLow:]
        lowDates = lowDates[countLow:]
        lowClose = lowClose[countLow:]
    if countHigh != 0:
        posHigh = posHigh[countHigh:]
        highPer = highPer[countHigh:]
        highDates = highDates[countHigh:]
        highClose = highClose[countHigh:]
    f = open(filePath, "a")
    f.write("Filter year set to " + str(setYear) + ". Data starts from " + str(setYear) + "\n")
    f.write(
        str(len(posLow)) + " dates. Deleted " + str(originalLow - len(posLow)) + " dates from days with big drops\n")
    f.write(
        str(len(posHigh)) + " dates. Deleted " + str(originalHigh - len(posHigh)) + " dates from days with big gains\n")
    f.close()


def filterByPercentage(x):
    global setPercentage
    setPercentage = x


def createFile(startDate, ticker):
    global filePath
    # create file to write analysis, write in set values so you can write multiple times with different filters
    posofchar = path.rfind('/')
    filePath = path[0:posofchar]
    filePath += "/" + ticker + "_" + startDate[0:4] + "_Summary.txt"
    f = open(filePath, "w")
    f.close()


def setValue():
    global lowPer, highPer, posLow, posHigh, lowDates, highDates, highClose, lowClose
    lowPer.clear()
    highPer.clear()
    posLow.clear()
    posHigh.clear()
    lowDates.clear()
    highDates.clear()
    highClose.clear()
    lowClose.clear()
    csv_input = pd.read_csv(path)
    percentageList = csv_input['Percentage']
    dateList = csv_input['Date']
    closeList = csv_input['Close']
    split_values = []
    counter = 0

    for a in percentageList:
        if float(a) < -setPercentage:
            lowPer.append(float(a))
            posLow.append(counter)
            lowClose.append(closeList[counter])
        elif float(a) > setPercentage:
            highPer.append(float(a))
            posHigh.append(counter)
            highClose.append(closeList[counter])
        counter += 1
    dateList = csv_input['Date']
    for x in posLow:
        lowDates.append(dateList[x])
    for x in posHigh:
        highDates.append(dateList[x])

    # for x in posLow:
    # print(dateList[x])
    # print(len(posLow))
    # print()
    # print(highDates)
    # print(highClose)


def afterHigh():
    # initialzie var
    dayAfter = []
    csv_input = pd.read_csv(path)
    close = csv_input['Close']
    nextClose = []
    percentageChange = goesDown = goesUp = equal = 0
    f = open(filePath, "a")
    f.write("\nData for days where stocks closes above " + str(setPercentage) + "%\n")
    f.write("Data contains " + str(len(highClose)) + " entries\n")
    # go through high days, get next days close and add it to nextClose
    for x in posHigh:
        if (x+1) != len(posHigh):
            nextClose.append(close[x + 1])
        else:
            nextClose.append(close[x])

    # print days with high movement up, close value and the next days close value
    # for x in range(len(nextClose)):
    # print(str(highDates[x]) + '          ' + str(highClose[x]) + '     ' + str(nextClose[x]))

    # go through each high, and count how many times it goes up and goes down the next day, calculate % based on closing
    for x in range(len(nextClose)):
        difference = (highClose[x] - nextClose[x]) / highClose[x]
        percentageChange = percentageChange + (-1 * difference)
        if highClose[x] > nextClose[x]:
            goesDown += 1
        elif highClose[x] == nextClose[x]:
            equal += 1
        else:
            goesUp += 1
    # write data to the file
    f.write("CLoses positively next day: " + str(round(goesUp * 100 / (goesUp + goesDown + equal), 2)) + "%\n")
    f.write("closed at exactly the same price next day: " + str(equal) + "\n")
    f.write("went down next day: " + str(goesDown) + "\n")
    f.write("went up next day: " + str(goesUp) + "\n")
    # adds up total percentage moved then divided by length, so on average it moves x%
    f.write("average percentage: " + str(percentageChange / (len(nextClose)) * 100) + "%\n\n")
    f.close()


# find days with big drop, find out close for next day, p2 find out when it meets high again
def afterLow():
    dayAfter = []
    csv_input = pd.read_csv(path)
    close = csv_input['Close']
    nextClose = []
    percentageChange = goesDown = goesUp = equal = 0

    f = open(filePath, "a")
    f.write("Data for days after it drops " + str(setPercentage) + "%\n")
    print(len(close))
    lastDay = len(close)
    print(posLow)
    for x in posLow:
        if (x + 1) == lastDay:
            #nextClose.append(close[x])
        else:
            nextClose.append(close[x + 1])

    for x in range(len(nextClose)):
        difference = (lowClose[x] - nextClose[x]) / lowClose[x]
        percentageChange = percentageChange + (-1 * difference)
        if lowClose[x] > nextClose[x]:
            goesDown += 1
        elif lowClose[x] == nextClose[x]:
            equal += 1
        else:
            goesUp += 1

    f.write("CLoses postively next day: " + str(round(goesUp * 100 / (goesUp + goesDown + equal), 2)) + "%\n")
    f.write("closed at exactly the same price next day: " + str(equal) + "\n")
    f.write("went down next day: " + str(goesDown) + "\n")
    f.write("went up next day: " + str(goesUp) + "\n")
    # adds up total percentage moved then divided by length, so on average it moves x%
    f.write("average percentage: " + str(percentageChange / (len(nextClose)) * 100) + "%\n")

    lowHigh = csv_input['High']
    lowHighValue = []
    nextHigh = []
    for x in posLow:
        lowHighValue.append(lowHigh[x])
    for x in posLow:
        daysAfter = 0
        lowDateHigh = lowHigh[x]
        y = 0
        while lowDateHigh > y:
            daysAfter += 1
            y = lowHigh[x + daysAfter]
        nextHigh.append(daysAfter)
        sum = 0
    for x in nextHigh:
        sum += x
    f.write(
        "average trading days it takes to reach high of day drop again: " + str(round(sum / len(nextHigh), 2)) + "\n")
    f.write("trading days it takes to reach same high: \n")
    for x in nextHigh:
        f.write(str(x) + ", ")
    f.write("\n")
    count = 0
    for x in nextHigh:
        if x < 6:
            count += 1
    f.write("Times where it has gone up within 5 days: " + str(count) + " out of " + str(len(nextHigh)) + "\n")
    f.write("-----------------------------------------------------------\n\n")
    f.close()


def runAnalysis(pathMain, startDate, ticker):
    setYear = [0, 2000, 2008, 2010, 2015, 2020]
    setPercentage = [2.4, 3.4]
    global path
    path = pathMain
    createFile(startDate, ticker)
    for x in setYear:
        for y in setPercentage:
            filterByPercentage(y)
            setValue()
            filterByYear(x)
            afterHigh()
            afterLow()
