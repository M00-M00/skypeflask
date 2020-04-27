import pandas as pd
import yfinance as yf
import yahoofinancials as yahoo
from datetime import datetime , timedelta
from yahoo_fin import stock_info as si

today = datetime.today().strftime('%Y-%m-%d')
yesterday = (datetime.today() - timedelta(days=3)).strftime('%Y-%m-%d')




info_dict = ['sector', 'shortName', 'website', 'longBusinessSummary']

info_finance = ['regularMarketPreviousClose',
'previousClose',
'regularMarketOpen',
'twoHundredDayAverage',
'volume24Hr',
'fiftyDayAverage',
'fiftyTwoWeekHigh',
'fiftyTwoWeekLow',
'dayHigh',
'dayLow']



def get_information(ticker):
    info_keys = ['sector', 'shortName', 'website', 'longBusinessSummary']
    all_data = yf.Ticker(ticker).info
    info_dict = {x: all_data[x] for x in info_keys}
    return info_dict

def get_prices(ticker):
    tkr_figures = yf.download(ticker, start = yesterday,  end = today, progress = False)
    name = yf.Ticker(ticker).info["shortName"]
    ticker_data = {}
    ticker_data["name"] = name
    ticker_data["data"] = tkr_figures.head()
    return ticker_data

def get_figures(ticker):
    info_finance = ['shortName','regularMarketOpen',
    'regularMarketOpen',
    'twoHundredDayAverage',
    'volume24Hr',
    'fiftyDayAverage',
    'fiftyTwoWeekHigh',
    'fiftyTwoWeekLow',
    'dayHigh',
    'dayLow']
    all_data = yf.Ticker(ticker).info
    info_dict = {x: all_data[x] for x in info_finance}
    return info_dict

def live_price(ticker):
    return si.get_live_price(ticker)
