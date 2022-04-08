import os #tools to interact with local files
import sys
import petl
import configparser
import requests
import datetime
import json
import decimal



#get data from config file using method called configparser()
config = configparser.ConfigParser()
#Error and exeption handling
try:
    config.read('config.ini')
except Exception as e:
    print('Cant read this file:' + str(e))
    sys.exit() #gets rid of error message


# read settings from configuration file
startDate = config['CONFIG']['startDate']
url = config['CONFIG']['url']



# request data from URL API, bank data
try:
    Bank_api_Response = requests.get(url+startDate)
except Exception as e:
    print('could not make request:' + str(e))
    sys.exit()
#print(Bank_api_Response.text)

# initialize list of lists for data storage
Bank_dates_bucket = []
bank_rates_bucket = []
# check response status and process BOC JSON object
if (Bank_api_Response.status_code == 200):
    BOCRaw = json.loads(Bank_api_Response.text)

    # extract observation data into column arrays
    for row in BOCRaw['observations']:
        Bank_dates_bucket.append(datetime.datetime.strptime(row['d'],'%Y-%m-%d')) #forces data type to be time (takes string and turns into date)
        bank_rates_bucket.append(decimal.Decimal(row['FXUSDCAD']['v'])) #'FXUSDCAD' 'v' and 'd' are keys, this row goes two levels deep
   #print ( bank_rates_bucket) these are the exchange rates
    #print(Bank_dates_bucket)

    # create petl table from column arrays and rename the columns
    exchangeRates = petl.fromcolumns([Bank_dates_bucket, bank_rates_bucket],header=['date','rate'])
    #print(exchangeRates)
    
    
    # load expense document and this is second table
    try:
        expenses = petl.io.xlsx.fromxlsx('Expenses.xlsx',sheet='Github')
    except Exception as e:
        print('could not open expenses.xlsx:' + str(e))
        sys.exit()
    #print(expenses)
    
    # join tables using outer, has every value from both sets of data
    expenses = petl.outerjoin(exchangeRates,expenses,key='date')
 # we dont have an exchange for every day so we use filldown
    # fill down missing values
    expenses = petl.filldown(expenses,'rate') #looks for nulls 
    print(expenses)
"""""
    # remove dates with no expenses, se;ect statement identifies table and condition for that table
    expenses = petl.select(expenses,lambda rec: rec.USD != None)

    # add CDN column, what is this
    expenses = petl.addfield(expenses,'CAD', lambda rec: decimal.Decimal(rec.USD) * rec.rate)
    print(expenses) #combined two previous tables
   
   
"""