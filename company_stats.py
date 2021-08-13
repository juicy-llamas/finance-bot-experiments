#!/usr/bin/python3
import yfinance as yf
import pandas as pd
import requests
import bs4 as bs
from proxy_inteface import p_sesh

'''
stock lists:

http://batstrading.com/market_data/listed_symbols/
http://www.nasdaq.com/screening/company-list.aspx
ftp://ftp.nasdaqtrader.com/SymbolDirectory/nasdaqlisted.txt
https://stockanalysis.com/stocks/
'''

def get_tickers ():
	ret = {}

	# ADVFN scraper
	getter = p_sesh( "https://www.advfn.com/nasdaq/nasdaq.asp?companies=A" )
	soup = bs.BeautifulSoup( getter.last_result.text, "lxml", multi_valued_attributes = None )
	table = soup.find( "table", class_="market tab1" )
	looper = iter( table.find_all( lambda tag: tag.name == 'a' and tag.contents[ 0 ].name == None ) )
	while True:
		try:
			val = next( looper )
			if val.string.find( '(delisted)' ) == -1:
				key = next( looper )
				if not key in ret:
					ret[ key ] = val
		except StopIteration:
			break

raw_data = pd.DataFrame()

def add_company ( ticker ):
	obj = yf.Ticker( ticker )
	print( obj.quarterly_financials )

get_tickers()
