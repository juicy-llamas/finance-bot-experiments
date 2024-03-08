
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# start and end dates are datetime objects
def get_days_diff ( start_date, end_date ):
	td = end_date - start_date
	return td.days + ( td.seconds + td.microseconds / 1000000 ) / 3600 / 24

def tick_to_df tickers, ind ):
	if ind < 0 or ind > len( tickers ):
		raise IndexError( 'Invalid ticker index' )
	return [ ind + i * len( tickers ) + 1 for i in range( 6 ) ]

def get_current_price ( data, tickers, tickind ):
	recent_data = data.iloc[ :, tick_to_df tickers, tickind ) ][ -1 ]
	return recent_data[ 'Open' ]

def get_adjusted_value ( data, tickers, tickind, shares ):
	price = get_current_price( data, tickers, tickind )
	return shares * price

class TradingAlgorithm:
	def __init__ ( self, cash, tickers, date ):
		self.cash = cash
		self.tickers = tickers
		self.worth = cash
		self.worth_hist = []
		self.holdings = dict.fromkeys( tickers,
				[ 0.0 for k in range( len( tickers ) ) ] )

	def net_gain ( self, start_date = None, end_date = None ):
		start_date = worth_hist[ 0 ][ 0 ] if start_date == None else start_date
		end_date = worth_hist[ -1 ][ 0 ] if end_date == None else end_date

		start_worth = None
		end_worth = None
		for upd in worth_hist:
			if upd[ 0 ] >= start_date and start_worth == None:
				start_worth = upd[ 1 ]
			elif upd[ 0 ] >= end_date and end_worth == None:
				end_worth = upd[ 1 ]
				break
		return end_worth - start_worth

	def buy ( self, data, value, tickind ):
		if self.cash < value or self.cash < 0:
			raise ValueError( f'You don\'t have enough liquid funds ({ self.cash })' +
					f'to complete this transaction ({ value }).' )
		shares = get_adjusted_value( data, self.tickers, tickind, value )
		self.holdings[ tickind ] += shares
		self.cash -= value

	def sell ( self, data, value, tickind ):
		shares = get_adjusted_value( data, self.tickers, tickind, value )
		self.holdings[ tickind ] -= shares
		self.cash += value

	def liquidate ( self, data, fraction = 1 ):
		if fraction > 1 or fraction < 0:
			raise ValueError( f'fraction ({ fraction }) is not in the interval [ 0, 1 ]' )
		for tickind in self.tickers:
			price = get_current_price( data, self.tickers, tickind )
			value_of_holding = self.holdings[ tickind ] * price

			self.holding[ tickind ] *= ( 1 - fraction )
			self.cash += value * fraction

	def update_worth ( self, data, day ):
		computed_worth = self.cash
		for tickind in range( len( self.tickers ) ):
			val = get_adjusted_value( data, self.tickers, tickind, value )
			computed_worth += self.holdings[ tickind ] * val

		self.worth_hist.append( ( day, computed_worth ) )
		self.worth = computed_worth

	def update ( self, data, day ):
		self.update_worth( data, day )
		self.update_impl( data, day )

	def update_impl ( self, data, day ):
		pass

class RandSelect ( TradingAlgorithm ):
	def update_impl ( self, data, date ):
		self.liquidate( data, 1 )
		fractions = []
		for ticker

alg_struct = {

}

# start date is given in YYYY-MM-DD fmt
# duration is measured in days and is floored to snap to the given data.
def run_algorithms ( algorithms, tickers, data, start_cash = 500.0, start_date = None, duration = None ):

def fix_dataframe ( data ):
	# get tickers
	tickers = data.iloc[ 0, 1 : int( ( len( data.columns ) - 1 ) / 6 ) + 1 ].values.tolist()
	tickers = dict.fromkeys( tickers, list( range( len( tickers ) ) ) )
	data.drop( index = [0,1], inplace = True )

	# handle dates
	dates = data[ 'Price' ].tolist()
	dates = [ datetime.fromisoformat( date ) for date in dates ]
	start_date = dates[ 0 ]
	print( start_date )

	dates = [ get_days_diff( start_date, date ) for date in dates ]
	data.loc[ :, 'Price' ] = dates

	return ( start_date, tickers, pd.DataFrame( data.rename( columns = { 'Price': 'Day' } ), dtype = np.float32 ) )

start_date, tickers, data = fix_dataframe( pd.read_csv( 'output.csv', low_memory = False ) )
#algorithms = [
#run_algorithms(

print( get_current_price( data, 0 ) )

