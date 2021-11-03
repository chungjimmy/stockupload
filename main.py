# this code collects data from yahoo finance and creates a csv for the stock 'Spy"
# values verified with https://www.historicalstockprice.com
import datetime
from pandas_datareader import data
import pandas as pd
from datetime import date
from summary import *
from csvdoc import *


def main():
    # example
    startDate = '1996-01-01'
    ticker = 'AMC'
    path = ''
    update(startDate, ticker)
    runAnalysis(path, startDate, ticker)


if __name__ == '__main__':
    main()
