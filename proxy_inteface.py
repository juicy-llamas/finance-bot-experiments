#!/usr/bin/python3

from random import randrange
from time import sleep
import re
import lxml
import requests
import bs4 as bs

import warnings
warnings.filterwarnings( "ignore", message = r"Unverified HTTPS request" )

#Global Settings
PROXY_PROTOCOL = 'socks4'
COUNTRY = 'US'
VERBOSE = True

#Helper Methods / Objects
def p_obj ( proxy ):
	return { 'http': PROXY_PROTOCOL + '://' + proxy, 'https': PROXY_PROTOCOL + '://' + proxy }

def get_my_ip_loc ( proxy = None, timeout = 3.0 ):
	conn = {}
	headers = base_header
	headers[ "User-Agent" ] = generate_user_agent()
	if proxy == None:
		conn = requests.get( "https://ipinfo.io/json", headers = headers )
	else:
		conn = requests.get( "https://ipinfo.io/json", proxies = p_obj( proxy ), headers = headers, verify = False, timeout = timeout )
	resp = conn.json()
	conn.close()
	ip = resp[ 'ip' ]
	location = resp[ 'loc' ]
	provider = resp[ 'org' ]
	return { "ip": ip, "loc": location, "prov": provider }

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
	proxy_list = []
	native_ip = None
	
	def __init__ ( self, url = None, method = 'GET', retries = 100, timeout = 3.0, check_proxies = False, sleep_time_max = 0, sleep_time_min = 0 ):
		self.session = requests.Session()
		self.check = check_proxies
		self.change_proxy()
		self.session.proxies = p_obj( self.proxy )
		self.retries = retries
		self.timeout = timeout
		self.st = ( sleep_time_min, sleep_time_max, ( sleep_time_max - sleep_time_min ) / 10000 )
		
		if VERBOSE:
			print( "Session '" + url + "' created, proxy: " + self.proxy )
		if url != None:
			self.new_request( url, method = method )

	# If someone actually uses this, DON'T CHANGE THE RETRIES ARGUMENT. You can set the amount of retries by changing [object].retries.
	def new_request ( self, url, method = 'GET', _retries = 1 ):
		headers = base_header
		headers[ "User-Agent" ] = generate_user_agent()
		if VERBOSE:
			print( method + "ing from " + url + " with proxy " + self.proxy )
		try:
			self.last_result = self.session.request( method, url, headers = headers, verify = False, timeout = self.timeout )
			if not self.last_result.ok:
				raise ConnectionError
		except (requests.exceptions.RequestException, requests.exceptions.Timeout, ConnectionError):
			if _retries <= self.retries:
				if VERBOSE:
					print( "Request failed: Attempt " + str( _retries ) + " out of " + str( self.retries ) + " possible" )
				self.change_proxy()
				self.new_request( url, method, _retries + 1 )
			else:
				print( "Couldn't connect" )
		if self.st[ 1 ] > 0:
			sleep( randrange( *(self.st) ) )
		
	def change_proxy ( self ):
		if len( p_sesh.proxy_list ) == 0:
			p_sesh._refresh_proxies()
		self.proxy = p_sesh.proxy_list.pop()
		self.session.proxies.update( p_obj( self.proxy ) )
		if self.check and not self.check_proxy():
			self.change_proxy()

	# Just in case you want to check proxies before you use them
	def check_proxy ( self ):
		if VERBOSE:
			print( "Checking " + self.proxy )
		if p_sesh.native_ip == None:
			p_sesh.native_ip = get_my_ip_loc()
		try:
			proxy_ip = get_my_ip_loc( self.proxy, self.timeout )
			if p_sesh.native_ip[ "ip" ] != proxy_ip[ "ip" ]:
				if VERBOSE:
					print( "Proxy is good" )
				return True
			else:
				if VERBOSE:
					print( "Proxy didn't mask IP" )
				return False
		except (requests.exceptions.RequestException, requests.exceptions.Timeout, ConnectionError):
			if VERBOSE:
				print( "Couldn't connect to ipinfo.io with proxy" )
			return False
		
		# just in case...
		print( "p_sesh.check_proxy failed for some unkown reason. Tell the dev of this code that this is a bug." )
		return False
	
	@staticmethod
	def _refresh_proxies ():
		proxy_text = ""

		if VERBOSE:
			print( "Getting proxy list..." )
			
		sources = [
			"https://api.proxyscrape.com/v2/?request=getproxies&protocol=" + PROXY_PROTOCOL + "&timeout=10000&country=" + COUNTRY + "&simplified=true",
			"https://www.proxy-list.download/api/v1/get?type=" + PROXY_PROTOCOL + "&anon=elite&country=" + COUNTRY,
			"https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/" + PROXY_PROTOCOL + ".txt"
		]
		
		ip_regex = re.compile( "\d\.\d\.\d\.\d:\d" )
		wh_regex = re.compile( "[\r\n \t]+")
		
		for source in sources:
			try:
				connection = requests.get( source )
				proxy_text = connection.text
				connection.close()
				
				p_sesh.proxy_list = proxy_text.split( "\n" )
				
				# make sure we're getting valid IPs
				map( lambda ip : wh_regex.sub( "", ip ), p_sesh.proxy_list )
				filter( lambda ip : ip_regex.fullmatch( ip ), p_sesh.proxy_list )
			except (requests.exceptions.RequestException, requests.exceptions.Timeout, ConnectionError):
				if VERBOSE:
					print( "Couldn't connect to proxy source " + source + ", leaving it out of the list." )
		
		# shuffle the list to avoid picking the same ones over and over
		p_sesh.proxy_list = [ p_sesh.proxy_list.pop( randrange( 0, len( p_sesh.proxy_list ) ) ) for i in range( 0, len( p_sesh.proxy_list ) ) ]
		
		#if VERBOSE:
			#print( p_sesh.proxy_list )
		#exit()

print( p_sesh( "https://steamcommunity.com/market/" ).last_result.text )
