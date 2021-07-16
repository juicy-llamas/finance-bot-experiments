#!/usr/bin/python3

import proxy_interface as proxy

games = {
	"cs:go": {
		"appid": 730,
		"categories": {
			"ItemSet": [
				
			],
			"ProPlayer": [
				
			],
			"StickerCapsule": [
				
			],
			"TournamentTeam": [
				
			],
			"Weapon": [
				
			],
			"SprayColorCategory": [
				
			]
		},
	}
}

class steam_crawler:
	# URL / HARDCODING GOES HERE
	url = "https://steamcommunity.com/market/"
	search = "https://steamcommunity.com/market/search?q="
	
	def __init__ ( self ):
		self.client = proxy.p_sesh()
		
	def search ( self ):
		self.client.new_request( "https://steamcommunity.com/market/search?q=&category_730_ItemSet[]=any&category_730_ProPlayer[]=any&category_730_StickerCapsule[]=any&category_730_TournamentTeam[]=any&category_730_Weapon[]=any&appid=730#p1_popular_desc" )
