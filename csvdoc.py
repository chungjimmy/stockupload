import datetime
from pandas_datareader import data
import pandas as pd
from datetime import date

path = ''


# creates a csv for spy data from yahoo finance
def create_csv(start_date, ticker):
    global path
    end_date = date.today()
    Spy = data.DataReader(ticker, 'yahoo', start_date, end_date)
    Spy.to_csv(path)


# edit the csv by creating weekday as a number for easier usage in spreadsheet, % column
def weekday_as_num():
    csv_input = pd.read_csv(path)
    split_string = csv_input['Date']
    split_values = []
    for a in split_string:
        split_valuesList = a.split(' ')
        split_valuesStr = ''.join(split_valuesList)
        split_valuesInt = pd.Timestamp(split_valuesStr).day_of_week
        split_values.append(split_valuesInt)
    csv_input['WeekdayNum'] = split_values
    csv_input.to_csv(path, index=False)


# add weekday column for user visibility
def weekday_column():
    csv_input = pd.read_csv(path)
    split_string = csv_input['Date']
    split_values = []
    for a in split_string:
        split_valuesList = a.split(' ')
        split_valuesStr = ''.join(split_valuesList)
        split_valuesStr = pd.Timestamp(split_valuesStr).day_name()
        split_values.append(split_valuesStr)
    csv_input['Weekday'] = split_values
    csv_input.to_csv(path, index=False)


# convert week to out of year for quarterly analysis
def week_of_the_year():
    csv_input = pd.read_csv(path)
    split_string = csv_input['Date']
    split_values = []
    for a in split_string:
        split_valuesList = a.split(' ')
        split_valuesStr = ''.join(split_valuesList)
        split_valuesInt = pd.Timestamp(split_valuesStr).weekofyear
        split_values.append(split_valuesInt)
    csv_input['Week of year'] = split_values
    csv_input.to_csv(path, index=False)


# add year for easier queries
def year():
    csv_input = pd.read_csv(path)
    split_string = csv_input['Date']
    split_values = []
    for a in split_string:
        split_valuesList = a.split(' ')
        split_valuesStr = ''.join(split_valuesList)
        split_valuesInt = pd.Timestamp(split_valuesStr).year
        split_values.append(split_valuesInt)
    csv_input['Year'] = split_values
    csv_input.to_csv(path, index=False)


# calculates percentage changed based on the price of spy at the time Spy opens and closes
def percentage():
    csv_input = pd.read_csv(path)
    csv_input['Percentage'] = (csv_input['Close'] - csv_input['Open']) / csv_input['Open']
    csv_input['Percentage'] = csv_input['Percentage'] * 100
    csv_input.to_csv(path, index=False)


def percentage_low():
    csv_input = pd.read_csv(path)
    csv_input['Percentage_Low'] = (csv_input['Low'] - csv_input['Open']) / csv_input['Open']
    csv_input['Percentage_Low'] = csv_input['Percentage_Low'] * 100
    csv_input.to_csv(path, index=False)


def percentage_high():
    csv_input = pd.read_csv(path)
    csv_input['Percentage_High'] = (csv_input['High'] - csv_input['Open']) / csv_input['Open']
    csv_input['Percentage_High'] = csv_input['Percentage_High'] * 100
    csv_input.to_csv(path, index=False)


def trade_range():
    csv_input = pd.read_csv(path)
    csv_input['trade_range'] = (csv_input['Percentage_High'] - csv_input['Percentage_Low'])
    csv_input.to_csv(path, index=False)


# calls other functions to create csv, add all columns as default
def update(start_date, ticker):
    global path
    path = 'C:/Users/Alienwear/Desktop/Stock Data/' + ticker + '_' + start_date + '.csv'
    create_csv(start_date, ticker)
    weekday_as_num()
    weekday_column()
    week_of_the_year()
    year()
    percentage()
    percentage_low()
    percentage_high()
    trade_range()
    print('done with ticker: ' + ticker + ', starting at ' + start_date)
