#this code collects data from yahoo finance and creates a csv for the stock 'Spy"
#values verified with https://www.historicalstockprice.com
import datetime
from pandas_datareader import data
import pandas as pd
from datetime import date

#creates a csv for spy data from yahoo finance
def create_csv(start_date, ticker):
    end_date = date.today()
    Spy = data.DataReader(ticker, 'yahoo', start_date, end_date)
    path = 'C:' + ticker + '_' + start_date + '.csv'
    Spy.to_csv(path)
    return path

#edit the csv by creating weekday as a number for easier usage in spreadsheet, % column
def weekday_as_num(path):
    csv_input = pd.read_csv(path)
    split_string = csv_input['Date']
    split_values = []
    for a in split_string:
        split_valuesList = a.split(' ')
        split_valuesStr =''.join(split_valuesList)
        split_valuesInt = pd.Timestamp(split_valuesStr).day_of_week
        split_values.append(split_valuesInt)
    csv_input['WeekdayNum'] = split_values
    csv_input.to_csv(path, index = False)

#add weekday column for user visibility
def weekday_column(path):
    csv_input = pd.read_csv(path)
    split_string = csv_input['Date']
    split_values = []
    for a in split_string:
        split_valuesList = a.split(' ')
        split_valuesStr =''.join(split_valuesList)
        split_valuesStr = pd.Timestamp(split_valuesStr).day_name()
        split_values.append(split_valuesStr)
    csv_input['Weekday'] = split_values
    csv_input.to_csv(path, index = False)

#convert week to out of year for quarterly analysis
def week_of_the_year(path):
    csv_input = pd.read_csv(path)
    split_string = csv_input['Date']
    split_values = []
    for a in split_string:
        split_valuesList = a.split(' ')
        split_valuesStr =''.join(split_valuesList)
        split_valuesInt = pd.Timestamp(split_valuesStr).weekofyear
        split_values.append(split_valuesInt)
    csv_input['Week of year'] = split_values
    csv_input.to_csv(path, index = False)

#add year for easier queries
def year(path):
    csv_input = pd.read_csv(path)
    split_string = csv_input['Date']
    split_values = []
    for a in split_string:
        split_valuesList = a.split(' ')
        split_valuesStr =''.join(split_valuesList)
        split_valuesInt = pd.Timestamp(split_valuesStr).year
        split_values.append(split_valuesInt)
    csv_input['Year'] = split_values
    csv_input.to_csv(path, index = False)

#calculates percentage changed based on the price of spy at the time Spy opens and closes
def percentage(path):
    csv_input = pd.read_csv(path)
    csv_input['Percentage'] = (csv_input['Close'] - csv_input['Open'])/csv_input['Open']
    csv_input['Percentage'] = csv_input['Percentage'] * 100
    csv_input.to_csv(path, index = False)

#calls other functions to create csv, add all columns as default
def update(start_date, ticker):
    path = create_csv(start_date, ticker)
    weekday_as_num(path)
    weekday_column(path)
    week_of_the_year(path)
    year(path)
    percentage(path)
    print('done with ticker: ' + ticker + ', starting at ' + start_date)

def main():
    #example
    start_date = '1994-01-01'
    ticker = 'SPY'
    update(start_date, ticker)


if __name__ == '__main__':
    main()