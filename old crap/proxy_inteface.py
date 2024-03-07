#!/usr/bin/python3

from random import randrange
from time import sleep
import re
import requests
import bs4 as bs

import warnings
warnings.filterwarnings( "ignore", message = r"Unverified HTTPS request" )

# Global Settings
VERBOSE = True

# Helper Methods / Objects

def printvb( msg ):
	printvb( msg )

def generate_user_agent():
	ver = str( randrange( 70, 90, 1 ) )
	arch = "x86_64"
	return "Mozilla/5.0 (X11; Ubuntu; Linux " + arch + "; rv:" + ver + ".0) Gecko/20100101 Firefox/" + ver + ".0"

base_header = { #edit the host, user-agent, and connection
	"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
	"Accept-Language": "en-US,en;q=0.5",
	#"Accept-Encoding": "gzip, deflate, br",
	"Referrer": "https://thegay.porn/en/",
	"DNT": "1",
	"Upgrade-Insecure-Requests": "1",
	"Sec-GPC": "1"
}

# Useable Class
class p_sesh:
	native = None
	
	def __init__ ( self, url = None, method = 'GET', retries = 100, timeout = 3.0, check_proxies = False, sleep_time_max = 0, sleep_time_min = 0, proxy_protocol = 'socks4', country = 'US' ):
		if p_sesh.native == None:
			p_sesh.get_native()
		self.last_result = { 'ok': False }
		self.session = requests.Session()
		self.PROXY_PROTOCOL = proxy_protocol
		self.COUNTRY = country
		self.check = check_proxies
		self.retries = retries
		self.timeout = timeout
		self.headers = base_header.copy()
		self.proxy_list = []
		self.st = ( sleep_time_min, sleep_time_max, ( sleep_time_max - sleep_time_min ) / 10000 )
		if not self.change_proxy():
			raise Exception( "Could not get a valid proxy" )
		self.session.proxies = self.p_obj()
		
		printvb( "Session '" + url + "' created, proxy: " + self.proxy )
		if url != None:
			self.new_request( url, method = method )

	# If someone actually uses this, DON'T CHANGE THE RETRIES ARGUMENT. You can set the amount of retries by changing [object].retries.
	def new_request ( self, url, method = 'GET', _retries = 1 ):
		self.headers[ "User-Agent" ] = generate_user_agent()
		printvb( method + "ing from " + url + " with proxy " + self.proxy )
		try:
			self.last_result = self.session.request( method, url, headers = self.headers, verify = False, timeout = self.timeout )
			if not self.last_result.ok:
				raise ConnectionError
		except requests.exceptions.RequestException:
			print( "A request exception occurred"
		except (requests.exceptions.Timeout, ConnectionError):
			if _retries <= self.retries:
				printvb( "Request failed: Attempt " + str( _retries ) + " out of " + str( self.retries ) + " possible" )
				self.change_proxy()
				self.new_request( url, method, _retries + 1 )
			else:
				printvb( "Couldn't connect" )
		if self.st[ 1 ] > 0:
			sleep( randrange( *(self.st) ) )
		return self.last_result
		
	def change_proxy ( self ):
		while self.retries > 0:
			if len( self.proxy_list ) == 0:
				self._refresh_proxies()
			self.proxy = self.proxy_list.pop()
			self.session.proxies.update( self.p_obj() )
			printvb( "Switched to " + self.proxy )
			if not self.check or self.check_proxy():
				return True
			self.retries -= 1
		return False

	def p_obj ( self ):
		return { 'http': self.PROXY_PROTOCOL + '://' + self.proxy, 'https': self.PROXY_PROTOCOL + '://' + self.proxy }

	def get_proxy_loc ( self ):
		self.headers[ "User-Agent" ] = generate_user_agent()
		tmp_res = self.session.request( 'GET', "https://ipinfo.io/json", headers = self.headers, verify = False, timeout = self.timeout )
		if not tmp_res.ok:
			raise ConnectionError( f"status code is { tmp_res.status_code }"
		resp = tmp_res.json()
		tmp_res.close()

		ip = resp[ 'ip' ]
		location = resp[ 'loc' ]
		provider = resp[ 'org' ]
		return { "ip": ip, "loc": location, "prov": provider }

	@staticmethod
	def get_native ():
		conn = requests.get( "https://ipinfo.io/json" )
		if not conn.ok:
			raise Exception( "Couldn't get native ip info" )
		resp = conn.json()
		conn.close()

		ip = resp[ 'ip' ]
		location = resp[ 'loc' ]
		provider = resp[ 'org' ]
		p_sesh.native = { "ip": ip, "loc": location, "prov": provider }

	# Just in case you want to check proxies before you use them
	def check_proxy ( self ):
		printvb( "Checking " + self.proxy )
		try:
			proxy_ip = self.get_proxy_loc()
			for k, v in enumerate( p_sesh.native ):
				if v == proxy_ip[ k ]:
					printvb( f"Proxy didn't mask {k}" )
					return False
			printvb( "Proxy is good" )
			return True
		except requests.exceptions.InvalidSchema as e:
			import tracebackhttps://stackoverflow.com/questions/52742612/how-to-print-the-stack-trace-of-an-exception-object-in-python#52742770
			traceback.print_exception( type( e ), ex, ex.__traceback__ )
			print( "\n\np_sesh: FATAL ERROR: Invalid schema, probably missing socks support!\nTo install socks support, do `pip install -U 'requests[socks]'`" )
			exit()
		except requests.exceptions.Timeout:
			printvb( "Proxy timed out" )
		except ConnectionError as e:
			printvb( "Couldn't connect to ipinfo.io with proxy" )
			printvb( e )
		except requests.exceptions.RequestException as e:
			print( f"p_sesh: A request exception ({ type( e ) }) occurred.\nThis will be ignored, but may be a bug." )
		finally:
			# just in case...
			print( "p_sesh: ERROR: check_proxy failed for some unknown reason. Tell the dev of this code that this is a bug." )
		return False
	
	def _refresh_proxies ( self ):
		proxy_text = ""
		self.proxy_list = []

		printvb( "Getting proxy list..." )
			
		sources = [
			#"https://api.proxyscrape.com/v2/?request=getproxies&protocol=" + self.PROXY_PROTOCOL + "&timeout=10000&country=" + self.COUNTRY + "&simplified=true",
			#"https://www.proxy-list.download/api/v1/get?type=" + self.PROXY_PROTOCOL + "&anon=elite&country=" + self.COUNTRY,
			#"https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/" + self.PROXY_PROTOCOL + ".txt",
			"https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-" + self.PROXY_PROTOCOL + ".txt",
			"https://spys.me/" + self.PROXY_PROTOCOL + ".txt"
		]
		
		ip_regex = re.compile( "\d\.\d\.\d\.\d:\d" )
		wh_regex = re.compile( "[\r\n \t]+")
		
		for source in sources:
			try:
				connection = requests.get( source )
				proxy_text = connection.text
				connection.close()
				if connection.ok == False:
					continue
				
				self.proxy_list = self.proxy_list + proxy_text.split( "\n" )
			except (requests.exceptions.RequestException, requests.exceptions.Timeout, ConnectionError):
				printvb( "Couldn't connect to proxy source " + source + ", leaving it out of the list." )

		# make sure we're getting valid IPs
		map( lambda ip : wh_regex.sub( "", ip ), self.proxy_list )
		filter( lambda ip : ip_regex.fullmatch( ip ), self.proxy_list )
		
		# shuffle the list to avoid picking the same ones over and over
		self.proxy_list = [ self.proxy_list.pop( randrange( 0, len( self.proxy_list ) ) ) for i in range( 0, len( self.proxy_list ) ) ]
		
		#if VERBOSE:
			#print( p_sesh.proxy_list )
		#exit()

print( p_sesh( "https://steamcommunity.com/market/", check_proxies = True ).last_result.text )
