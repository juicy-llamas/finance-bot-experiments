
class transaction_error:
	pass

class server_error:
	pass

#class item:
	#def __init__ ( self, name, buy_action, sell_action, description = "" ):
		#self.name = name
		#self.buy_action = buy_action
		#self.sell_action = sell_action
		#self.description = description

class store:	
	
	def __init__ ( self, name, search_url, item_list = [] ):
		self.item_list = []
		self.name = name
		self.
		
	def search ( self, term, category ):
		# Does a search on the marketplace for new items
		pass
	
	def buy ( self, quantity, item_id = 0, item_name = "" ):
		# Perform the specified buy action. If the server
		# rejects our action, we will throw a server_error.
		# Otherwise, we will adjust our logs accordingly.
		pass
		
	def sell ( self, quantity, item_id = 0, item_name = "", sell_all = False ):
		# Check our logs. If we have enough of the item to sell,
		# we will complete the transaction. If we do not have
		# enough, a transaction_error will be thrown unless
		# sell_all is true. If sell_all is true and the quantity
		# specified is greater than our stock, we will sell our
		# entire stock, or if the stock is zero, we will just do
		# nothing (SHOULD WE THROW AN ERROR??). Next, we perform
		# the transaction, which is most likely to post a 
		# listing on the specified market, but it could be any
		# action. If the server rejects our action, we will 
		# throw a server error with details as to why the action
		# was rejected. When the action succeeds, we adjust our
		# logs accordingly. NOTE: only either item_id or 
		# item_name need to be specified; if both are specified
		# and in conflict, or if nothing is specified, we throw a
		# transaction_error.
		pass
		
	def __create_new_item ( self, url ):
		pass
