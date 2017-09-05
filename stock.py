#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  7 00:52:53 2017

@author: huyle
"""
#final IT780
#This program will: 
#yahoo api from chartapi.finance.yahoo.com/instrument/1.0/'whatever'/xxx
#https://chartapi.finance.yahoo.com/instrument/1.0/GOOG/chartdata;type=quote;range=1d/csv

# found one that works to replace the old yahoo chartapi: https://www.google.com/finance/historical?q=%27,symbol,%27&startdate=%27,startDateStr,%27&enddate=%27,endDateStr,%27&output=csv
# found from: https://github.com/creeveshft/matlabfunctions/blob/master/GetHistoricGoogle.m

import sys
import urllib.request, urllib.error, urllib.parse
import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import matplotlib.dates as mdates
#from matplotlib.finance import candlestick_ohlc
#import matplotlib


try:
    number = int(input('Enter Number of Stocks you need: '))
except Exception as e:
    print('Please enter a number!!!, error', str(e))
    sys.exit("Try Again! I told you to input NUMBER OF STOCKS, like how many?")

stocksToPull = []
for i in range(number):
    stock = input('Enter sticker of stock '+ str(i+1) + ': ')
    stocksToPull.append(stock)

#stocksToPull = ['AAPL', 'GOOG','GE', 'EBAY', 'AMZN', 'FB', 'TSLA']

def pullData(stock, year):
    try:
        fileLine = stock+'.txt'
        url = 'http://chartapi.finance.yahoo.com/instrument/1.0/'+stock+'/chartdata;type=quote;range='+year+'y/csv'
        sourceCode = urllib.request.urlopen(url).read().decode()
        splitSource = sourceCode.split('\n')
        for line in splitSource:
            splitline = line.split(',')
            if len(splitline) == 6:
                if 'values' not in line:
                    saveFile = open(fileLine,'a')
                    lineToWrite = line+'\n'
                    saveFile.write(lineToWrite)
        print('Pulled', stock)
        print('loading ...')
        time.sleep(2)
    except Exception as e:
        print('main loop', str(e))
        
        


# GRAPH DATA FROM STOCK TXT

def graphData(stock):
    try:
        stockFile = stock+'.txt'
        date, closep, highp, lowp, openp, volume = np.loadtxt(stockFile,delimiter=',', unpack=True, converters={ 0: bytespdate2num('%Y%m%d')})
        
        fig = plt.figure()
        fig.set_size_inches(15,8)
        ax1 = plt.subplot(2,1,1)
        ax1.plot(date, openp)
        ax1.plot(date, highp)
        ax1.plot(date, lowp)
        ax1.plot(date, closep)
        plt.ylabel('Stock Price')
        ax1.grid(True)
        
        ax2 = plt.subplot(2,1,2, sharex=ax1)
        ax2.bar(date, volume)
        plt.ylabel('Volume')
        ax2.grid(True)
        
        ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
        ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        
        for label in ax1.xaxis.get_ticklabels():
            label.set_rotation(0)
        for label in ax2.xaxis.get_ticklabels():
            label.set_rotation(45)
            
# ------- plot decoration --------- #
        plt.subplots_adjust(left=.10, bottom=.19, right=.93, top=.95, wspace=.07)
        plt.xlabel('Date')
        plt.suptitle('History of '+stock+' Stock Price')
        plt.show()

# ------- delete the current content in order to graph the second time for the same stock
#        deleteContent(stockFile)
    except Exception as e:
        print('dang, ',str(e))
        
            
# ------- plot decoration --------- #
        plt.subplots_adjust(left=.10, bottom=.19, right=.93, top=.95, wspace=.07)
        plt.xlabel('Date')
        plt.suptitle('History of '+stock+' Stock Price')
        plt.show()

# ------- delete the current content in order to graph the second time for the same stock
        deleteContent(stockFile)
    except Exception as e:
        print('dang, ',str(e))
        
#def getEarningIncome(stock):
#    try:
#        revenue = urllib.request.urlopen('https://www.quandl.com/api/v3/datasets/SEC/'+stock+'_SALESREVENUENET_Q.csv?api_key=HyHKNKzLur3xUu1A1g6C').read()
#        print(revenue)
#    except Exception as e:
#        print('error: ', str(e))
# Delete Content
def deleteContent(fName):
    with open(fName, "w"):
        pass
# Converting str
        
def bytespdate2num(fmt, encoding='utf-8'):
    strconverter = mdates.strpdate2num(fmt)
    def bytesconverter(b):
        s = b.decode(encoding)
        return strconverter(s)
    return bytesconverter
#################////////////////////// - MAIN - //////////////////////##############
for i in stocksToPull:
    day = input('Enter Number of Years for historical data of '+i +": ")
    pullData(i, day)
#    getEarningIncome(i)
    graphData(i)
