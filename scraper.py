import yfinance as yf
import pandas as pd
from bs4 import BeautifulSoup
import requests


def get_stock_data(ticker, period='1y'):
    """Get stock data using Yahoo Finance"""
    try:
        stock = yf.Ticker(ticker)
        hist = stock.history(period=period)
        return hist
    except Exception as e:
        print(f"Error getting stock data: {e}")
        return pd.DataFrame()


def scrape_financial_news(ticker):
    """Get formatted news with sources and dates"""
    try:
        news = yf.Ticker(ticker).news
        formatted_news = []

        for item in news[:5]:  # Get top 5 news items
            date = pd.to_datetime(item['providerPublishTime'], unit='s').strftime('%b %d, %Y')
            formatted_news.append({
                'title': item['title'],
                'publisher': item['publisher'],
                'date': date,
                'link': item['link']
            })
        return formatted_news
    except Exception as e:
        print(f"News scraping error: {e}")
        return []