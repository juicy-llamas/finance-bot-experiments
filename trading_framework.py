
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class TradingAlgorithm:
	def __init__ ( self, cash, tickers ):
		self.cash = cash
		self.holdings = dict.fromkeys( keys = tickers, values = [ 0.0 for k in range( len( tickers ) ) ] )

	def update ( self ):
		pass

# start date is given in YYYY-MM-DD fmt
# duration is measured in days and is floored to snap to the given data.
def run_algorithms ( algorithms, data, start_cash = 500.0, start_date = None, duration = None ):
	pass

# start and end dates are datetime objects
def get_days_diff ( start_date, end_date ):
	td = end_date - start_date
	return td.days + ( td.seconds + td.microseconds / 1000000 ) / 3600 / 24

def t2c ( ind ):
	if ind < 0 or ind > len( tickers ):
		raise IndexError( 'Invalid ticker index' )
	return [ ind + i * len( tickers ) + 1 for i in range( 6 ) ]

def fix_dataframe ( data ):
	# get tickers
	tickers = data.iloc[ 0, 1 : int( ( len( data.columns ) - 1 ) / 6 ) + 1 ].values.tolist()
	tickers = dict.from
	data.drop( index = [0,1], inplace = True )

	# handle dates
	dates = data[ 'Price' ].tolist()
	dates = [ datetime.fromisoformat( date ) for date in dates ]
	start_date = dates[ 0 ]
	print( start_date )

	dates = [  for date in dates ]
	data.loc[ :, 'Price' ] = dates

	return ( start_date, tickers, pd.DataFrame( data.rename( columns = { 'Price': 'Day' } ), dtype = np.float32 ) )

start_date, tickers, data = fix_dataframe( pd.read_csv( 'output.csv', low_memory = False ) )

print( data.iloc[ :, t2c( 0 ) ][ data[ 'Day' ] < 4 ] )
