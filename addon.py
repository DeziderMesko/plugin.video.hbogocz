# -*- coding: utf-8 -*-
import re
import sys
import os
import urllib
import urllib2
import json
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import xbmcvfs
import base64
import time
import inputstreamhelper

__addon_id__= 'plugin.video.hbogocz'
__Addon = xbmcaddon.Addon(__addon_id__)
__settings__ = xbmcaddon.Addon(id='plugin.video.hbogocz')

UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'
MUA = 'Dalvik/2.1.0 (Linux; U; Android 8.0.0; Nexus 5X Build/OPP3.170518.006)'

se = __settings__.getSetting('se')
language = __settings__.getSetting('language')
if language == '0':
	lang = 'Czech'
	Code = 'CES'
	srtsubs_path = xbmc.translatePath('special://temp/hbogo.Czech.Forced.srt')
elif language == '1':
	lang = 'Czech'
	Code = 'CES'
	srtsubs_path = xbmc.translatePath('special://temp/hbogo.Czech.Forced.srt')
elif language == '2':
	lang = 'English'
	Code = 'ENG'
	srtsubs_path = xbmc.translatePath('special://temp/hbogo.English.Forced.srt')
	

md = xbmc.translatePath(__Addon.getAddonInfo('path') + "/resources/media/")
search_string = urllib.unquote_plus(__settings__.getSetting('lastsearch'))

operator = __settings__.getSetting('operator')
op_ids = [
'e04b20c2-be50-4b65-9b77-9e17e854de32', # asi HBO GO
'f8e915f5-4641-47b1-a585-d93f61bbbfd3', # freeSAT Česká republika
'c55e69f0-2471-46a9-a8b7-24dac54e6eb9', # Skylink
'f0e09ddb-1286-4ade-bb30-99bf1ade7cff', # UPC CZ
'3a2f741b-bcbc-455f-b5f8-cfc55fc910a3', # Slovák Telekom
'5696ea41-2087-46f9-9f69-874f407f8103', # Lepší.TV
'b8a2181d-b70a-49a7-b823-105c995199a2', # O2
'a72f9a11-edc8-4c0e-84d4-17247c1111f5', # RIO Media
'249309a7-6e61-436d-aa12-eeaddcfeb72e', # UPC BROADBAND SLOVAKIA
'cdb7396a-bd2c-45e9-a023-71441e8dae64', # AIM
'ac49b07c-4605-409c-83bd-16b5404b16a7', # T-MOBILE Czech Republic a.s.
'ad5a1855-1abd-4aa5-a947-f9942a08ca75', # Antik Telecom
'80c3f17b-718c-4f1b-9a58-67b5ac13b6fd', # CentroNet, a. s.
'b132e3a1-ea76-4659-8656-1aac32bccd56', # DIGI CZ s.r.o.
'cd2b4592-90be-4ad7-96a0-54e34ee74866', # DIGI SLOVAKIA s.r.o.
'6c9e2104-83dc-48fb-a44c-ee3b8d689005', # FixPro
'1bfb5785-446d-4ca7-b7a4-cc76f48c97fe', # flexiTV
'b3ce9ab2-af8f-4e02-8ab7-9a01d587a35f', # freeSAT Slovensko
'25e0270f-ae80-49b1-9a20-bfa47b7690e1', # GRAPE SC
'82811c4a-ad87-4bda-a1bd-2f4a4215eac4', # HD Kabel
'aa2a90c0-292c-444e-a069-1ae961fa59f7', # Kuki
'95a5f7c8-95b7-4978-8fff-abe023249196', # MARTICO
'6925e9ca-9d97-446c-b3c2-09971f441f2a', # Nej.cz
'a2edba6f-bffb-4efe-bb7a-3b51e2fc0573', # NETBOX
'939ffed6-d015-427e-a2f7-a82d1b846eb7', # Satro
'064a6c6a-0556-4ff1-8d4d-c8cf3141131a', # SATT
'c2c2fdb7-8562-4b16-a09c-f7530ce2ce78', # SELFNET
'980a4419-1336-4056-a561-268afe7907f3', # sledovanitv.cz s.r.o.
'8a312c76-9e9c-42e4-b38c-c0adbd6c6a93', # Slovanet a.s.
'5b8544f8-784a-473b-97ad-159a2f95d0fb', # SWAN, a.s.
'69253de6-3935-4c48-9557-5a1e930f30de', # Tesatel
'b59ee559-45b9-46a0-a40c-7f41ab6e53e9', # HBO GO special
'a215610d-aecb-4357-934f-403813a7566c', # HBO GO Vip/Club Czech Republic
'ad729e98-c792-4bce-9588-106f11ce3b90', # HBO Development
'2e61999a-1b77-4ed2-b531-081dfdd3bee0'  # HBO GO Vip/Club Slovakia
]
op_id = op_ids[int(operator)];


username = __settings__.getSetting('username')
password = __settings__.getSetting('password')

individualization = __settings__.getSetting('individualization')
goToken = ""
customerId = ""
GOcustomerId = ""
sessionId = '00000000-0000-0000-0000-000000000000'

loggedin_headers = {
	'User-Agent': UA,
	'Accept': '*/*',
	'Accept-Language': 'en-US,en;q=0.5',
	'Referer': 'https://www.hbogo.cz/',
	'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
	'Origin': 'https://www.hbogo.cz',
	'X-Requested-With': 'XMLHttpRequest',
	'GO-Language': 'CES',
	'GO-requiredPlatform': 'CHBR',
	'GO-Token': '',
	'GO-SessionId': '',
	'GO-swVersion': '4.8.0',
	'GO-CustomerId': '',
	'Connection': 'keep-alive',
	'Accept-Encoding': ''
}

loggedviahbo_headers = {
'GO-requiredPlatform': 'CHBR',
'Origin': 'https://hbogo.cz',
'Accept-Encoding': '',
'Accept-Language': 'en-US,en;q=0.9',
'User-Agent': UA,
'Content-Type': 'application/json',
'Accept': '*/*',
'Referer': 'https://hbogo.cz/',
'GO-swVersion': '4.7.4',
'Connection': 'keep-alive',
'GO-CustomerId': ''
}

def LOGINVIAHBOPAYLOAD(indiv):
	return {
'Id':'',
'Action':'L',
'IsPromo':False,
'OperatorId':op_id,
'IsAnonymus':False,
'EmailAddress':username,
'Password':password,
'Nick':'',
'BirthYear':0,
'SubscribeForNewsletter':False,
'IpAddress':'',
'OperatorName':'HBO Czech Republic',
'Language':'CES',
'CustomerCode':'',
'ServiceCode':'HBO_Premium',
'CountryName':'Czech Republic',
'AppLanguage':'CES',
'AudioLanguage':'CES',
'DefaultSubtitleLanguage':'CES',
'AutoPlayNext':False,
'ProfileName':'',
'SubtitleSize':'MEDIUM',
'IsDefaultProfile':True,
'Gender':0,
'ZipCode':'',
'FirstName':'',
'LastName':'',
'SubscState':'VALID',
'CurrentDevice':{
	'Id':'',
	'Individualization':indiv,
	'Name':'COMP',
	'Platform':'COMP',
	'CreatedDate':time.strftime('%d/%m/%Y'),
	'IsDeleted':False,
	'OSName':'Linux',
	'Brand':'Chrome',
	'Modell':'61.0.3163',
	'SWVersion':'4.7.4'
}}



# Data o ověření uložte trvale; provádí se jednou
def storeIndiv(indiv, custid):
	global individualization
	global customerId
	individualization = __settings__.getSetting('individualization')
	if individualization == "":
		__settings__.setSetting('individualization', indiv)
		individualization = indiv

	customerId = __settings__.getSetting('customerId')
	if customerId == "":
		__settings__.setSetting('customerId', custid)
		customerId = custid


# Zaregistrujte přístroj na plošině; provádí se jednou
def SILENTREGISTER():
	global goToken
	global individualization
	global customerId
	global sessionId
	
	#За HBO Czech Republic
	if op_id =='e04b20c2-be50-4b65-9b77-9e17e854de32':
		payload = LOGINVIAHBOPAYLOAD("")
		req = urllib2.Request('https://api.ugw.hbogo.eu/v3.0/Authentication/CZE/JSON/CES/COMP', json.dumps(payload), loggedviahbo_headers)
		opener = urllib2.build_opener()
		f = opener.open(req)
		jsonrsp = json.loads(f.read())
		try:
			if jsonrsp['ErrorMessage']:
				xbmcgui.Dialog().ok('Chyba', jsonrsp['Error'])
		except:
			#goToken = jsonrsp['Token']
			sessionId = jsonrsp['SessionId']
			custid = jsonrsp['Customer']['Id']
			indiv = jsonrsp['Customer']['CurrentDevice']['Individualization']
			storeIndiv(indiv, custid)
		
	#За inni operatorzy
	else:
		req = urllib2.Request('https://cz.hbogo.eu/services/settings/silentregister.aspx', None, loggedin_headers)
		
		opener = urllib2.build_opener()
		f = opener.open(req)
		jsonrsp = json.loads(f.read())

		if jsonrsp['Data']['ErrorMessage']:
			xbmcgui.Dialog().ok('Chyba', jsonrsp['Data']['ErrorMessage'])
		else:
			indiv = jsonrsp['Data']['Customer']['CurrentDevice']['Individualization']
			custid = jsonrsp['Data']['Customer']['CurrentDevice']['Id']
			storeIndiv(indiv, custid)
			sessionId = jsonrsp['Data']['SessionId']
	return jsonrsp

# autentizace; je provedeno před otevřením videa
def LOGIN():
	global sessionId
	global goToken
	global customerId
	global GOcustomerId
	global individualization
	global loggedin_headers

	customerId = __settings__.getSetting('customerId')
	individualization = __settings__.getSetting('individualization')

	if (individualization == "" or customerId == ""):
		jsonrsp = SILENTREGISTER()

	if (username=="" or password==""):	
		xbmcgui.Dialog().ok('HBO GO', 'Zadejte přihlašovací údaje do nastavení pluginů.')
		xbmcaddon.Addon(id='plugin.video.hbogocz').openSettings("Účet")
		xbmc.executebuiltin("Container.Refresh")
		return False

	#За HBO Czech Republic
	if op_id =='e04b20c2-be50-4b65-9b77-9e17e854de32':
		payload = LOGINVIAHBOPAYLOAD(individualization)
		req = urllib2.Request('https://api.ugw.hbogo.eu/v3.0/Authentication/CZE/JSON/CES/COMP', json.dumps(payload), loggedviahbo_headers)
		opener = urllib2.build_opener()
		f = opener.open(req)
		jsonrspl = json.loads(f.read())
		
		try:
			if jsonrspl['Data']['ErrorMessage']:
				xbmcgui.Dialog().ok('Chyba', jsonrspl['Data']['ErrorMessage'])
		except:
			pass
		
		sessionId = jsonrspl['SessionId']
		if sessionId == '00000000-0000-0000-0000-000000000000':
			xbmcgui.Dialog().ok('Přihlášení se nezdařilo','Zkontrolujte, zda jste v nastavení správně zadali přihlašovací údaje, a zkuste to znovu.')
			xbmcaddon.Addon(id='plugin.video.hbogocz').openSettings("Účet")
			xbmc.executebuiltin("Action(Back)")
		else:
			#xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(username,'Czas na popcorn!', 4000, md+'DefaultUser.png'))
		
			goToken = jsonrspl['Token']
			GOcustomerId = jsonrspl['Customer']['Id']
		
			loggedin_headers['GO-SessionId'] = str(sessionId)
			loggedin_headers['GO-Token'] = str(goToken)
			loggedin_headers['GO-CustomerId'] = str(GOcustomerId)
		
		
	#За inni operatorzy
	else:
		go_customer = base64.b64encode(bytes({
			"AllowedContents": [],
			"BirthYear": 1900,
			"IpAddress": None,
			"CurrentDevice": {
				"Id": customerId,
				"Individualization": individualization,
				"Name": "Chrome 61.0.3163",
				"Platform": "COMP",
				"CreatedDate": time.strftime("%d.%m.%Y"),
				"DeletedDate": "01.01.0001",
				"IsDeleted": False,
				"OSName": "Linux",
				"OSVersion": None,
				"Brand": "Chrome 61.0.3163",
				"Modell": "Chrome 61.0.3163",
				"SWVersion": "4.0.30319.42000"
			},
			"CustomerCode": None,
			"DebugMode": False,
			"EmailAddress": "",
			"Gender": 2,
			"GroupIndexes": None,
			"Id": GOcustomerId,
			"IsAnonymus": True,
			"Nick": "",
			"OperatorId": op_id,
			"OperatorToken": None,
			"ParentId": "00000000-0000-0000-0000-000000000000",
			"ParentalControl": None,
			"Password": "",
			"SecondarySpecificData": None,
			"SpecificData": None,
			"SubscribeForNewsletter": False,
			"TVPinCode": None,
			"ZipCode": ""
			}))
		sn_headers = {
			'User-Agent': UA,
			'Accept': '*/*',
			'Accept-Language': 'en-US,en;q=0.5',
			'Referer': 'https://www.hbogo.cz/',
			'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
			'GO-Language': 'CES',
			'GO-Individualization': individualization,
			'GO-Token': goToken,
			'GO-SessionId': sessionId,
			'GO-CustomerId': GOcustomerId,
			'GO-swVersion': '4.8.0',
			'GO-requiredPlatform': 'CHBR',
			'GO-Customer': go_customer,
			'X-Requested-With': 'XMLHttpRequest',
			'Origin': 'https://www.hbogo.cz',
			'Connection': 'keep-alive'
			}
		
		usernamekey = 'EmailAddress'
		
		# UPC
		if op_id =='c5ff7517-8ef8-4346-86c7-0fb328848671':
			usernamekey = 'Nick'

		sn_payload = urllib.urlencode({'OperatorId': op_id, usernamekey: username, 'Password': password})
		req = urllib2.Request('https://cz.hbogo.eu/services/settings/signin.aspx', sn_payload, sn_headers)
		opener = urllib2.build_opener()
		f = opener.open(req)
		jsonrspl = json.loads(f.read())
		
		try:
			if jsonrspl['Data']['ErrorMessage']:
				xbmcgui.Dialog().ok('Chyba přihlášení', jsonrspl['Data']['ErrorMessage'])
		except:
			pass
		
		sessionId = jsonrspl['Data']['SessionId']
		if sessionId == '00000000-0000-0000-0000-000000000000':
			xbmcgui.Dialog().ok('Přihlášení se nezdařilo','Zkontrolujte, zda jste v nastavení správně zadali přihlašovací údaje, a zkuste to znovu.')
			xbmcaddon.Addon(id='plugin.video.hbogocz').openSettings("Účet")
			xbmc.executebuiltin("Action(Back)")
		else:
			xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(username,'Czas na popcorn!', 4000, md+'DefaultUser.png'))
		
			goToken = jsonrspl['Data']['Token']
			GOcustomerId = jsonrspl['Data']['Customer']['Id']
		
			loggedin_headers['GO-SessionId'] = str(sessionId)
			loggedin_headers['GO-Token'] = str(goToken)
			loggedin_headers['GO-CustomerId'] = str(GOcustomerId)




#Kategorie
def CATEGORIES():
	addDir('Vyhledávání filmů, seriálů ...','search','',4,md+'DefaultAddonsSearch.png')
	#Stahování kategorií
	req = urllib2.Request('http://czapi.hbogo.eu/v7/Groups/json/CES/ANMO/0/True', None, loggedin_headers)
	opener = urllib2.build_opener()
	f = opener.open(req)
	jsonrsp = json.loads(f.read())

	try:
		if jsonrsp['ErrorMessage']:
			xbmcgui.Dialog().ok('Chyba', jsonrsp['ErrorMessage'])
	except:
		pass
	#Lista kategorii
	for cat in range(0, 3): #Do 3, aby obsahovala falešnou kategorii Kids a Můj seznam
		addDir(jsonrsp['Items'][cat]['Name'].encode('utf-8', 'ignore'),jsonrsp['Items'][cat]['ObjectUrl'],'',1,md+'DefaultFolder.png')
	#Kategorie Kids byla přidána ručně
	addDir(jsonrsp['Items'][3]['Name'].encode('utf-8', 'ignore'),'http://czapi.hbogo.eu/v7/Group/json/CES/ANMO/b071fcca-7b15-459d-9b2a-53b108d1df6c/0/0/0/0/0/0/True','',1,md+'DefaultFolder.png')
	addDir('Můj seznam','http://czapi.hbogo.eu/v7/CustomerGroup/json/CES/ANMO/c79efa9f-be92-4bfd-90d8-31a9c30d4b80/0/0/0/0/0/0/false','',1,md+'DefaultFolder.png')


#Obsah kategorií
def LIST(url):
	groupid = url.find("c79efa9f-be92-4bfd-90d8-31a9c30d4b80", 0, len(url))
	if groupid > -1 and sessionId == '00000000-0000-0000-0000-000000000000':
		if LOGIN() == False:
			return

	req = urllib2.Request(url, None, loggedin_headers)
	opener = urllib2.build_opener()
	f = opener.open(req)
	jsonrsp = json.loads(f.read())
	try:
		if jsonrsp['ErrorMessage']:
			xbmcgui.Dialog().ok('Chyba', jsonrsp['ErrorMessage'])
	except:
		pass
	#Pokud existuje podkategorie / žánry
	if len(jsonrsp['Container']) > 1:
		for Container in range(0, len(jsonrsp['Container'])):
			addDir(jsonrsp['Container'][Container]['Name'].encode('utf-8', 'ignore'),jsonrsp['Container'][Container]['ObjectUrl'],'',1,md+'DefaultFolder.png')
	else:
		xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED)
		xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_DATE)
		xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_TITLE)
		#Pokud neexistují žádné podkategorie / druhy
		for titles in range(0, len(jsonrsp['Container'][0]['Contents']['Items'])):

			allowplay = jsonrsp['Container'][0]['Contents']['Items'][titles].get( 'AllowPlay', None )
			if allowplay is None:
				allowplay = False

			if jsonrsp['Container'][0]['Contents']['Items'][titles]['ContentType'] == 1: #1=MOVIE/EXTRAS, 2=SERIES(serial), 3=SERIES(episode)
				#Film
				xbmcplugin.setContent(int(sys.argv[1]), 'movie')
				plot = jsonrsp['Container'][0]['Contents']['Items'][titles].get( 'Description', None )
				if plot is None:
					plot = jsonrsp['Container'][0]['Contents']['Items'][titles].get( 'Abstract', None )
				if plot is None:
					plot = ''
				plot.encode('utf-8', 'ignore')
				firstGenre = jsonrsp['Container'][0]['Contents']['Items'][titles]['Genre']
				secondGenre = jsonrsp['Container'][0]['Contents']['Items'][titles]['SecondaryGenre']
				genre = [firstGenre.capitalize(), secondGenre.capitalize()]
				date = jsonrsp['Container'][0]['Contents']['Items'][titles]['AvailabilityFrom']
				addLink(jsonrsp['Container'][0]['Contents']['Items'][titles]['ObjectUrl'],plot,jsonrsp['Container'][0]['Contents']['Items'][titles]['AgeRating'],jsonrsp['Container'][0]['Contents']['Items'][titles]['ImdbRate'],jsonrsp['Container'][0]['Contents']['Items'][titles]['BackgroundUrl'],[jsonrsp['Container'][0]['Contents']['Items'][titles]['Cast'].split(', ')][0],jsonrsp['Container'][0]['Contents']['Items'][titles]['Director'],jsonrsp['Container'][0]['Contents']['Items'][titles]['Writer'],jsonrsp['Container'][0]['Contents']['Items'][titles]['Duration'],genre,jsonrsp['Container'][0]['Contents']['Items'][titles]['Name'].encode('utf-8', 'ignore'),jsonrsp['Container'][0]['Contents']['Items'][titles]['OriginalName'],jsonrsp['Container'][0]['Contents']['Items'][titles]['ProductionYear'],5,date,allowplay)
				#xbmc.log("GO: FILMI: DUMP: " + jsonrsp['Container'][0]['Contents']['Items'][titles]['ObjectUrl'], xbmc.LOGNOTICE)
				
			elif jsonrsp['Container'][0]['Contents']['Items'][titles]['ContentType'] == 3:
				#Epizoda seriálu
				xbmcplugin.setContent(int(sys.argv[1]), 'episode')
				plot = jsonrsp['Container'][0]['Contents']['Items'][titles].get( 'Abstract', None )
				if plot is None:
					plot = ''
				plot.encode('utf-8', 'ignore')
				firstGenre = jsonrsp['Container'][0]['Contents']['Items'][titles]['Genre']
				secondGenre = jsonrsp['Container'][0]['Contents']['Items'][titles]['SecondaryGenre']
				genre = [firstGenre.capitalize(), secondGenre.capitalize()]
				date = jsonrsp['Container'][0]['Contents']['Items'][titles]['AvailabilityFrom']
				addLink(jsonrsp['Container'][0]['Contents']['Items'][titles]['ObjectUrl'],plot,jsonrsp['Container'][0]['Contents']['Items'][titles]['AgeRating'],jsonrsp['Container'][0]['Contents']['Items'][titles]['ImdbRate'],jsonrsp['Container'][0]['Contents']['Items'][titles]['BackgroundUrl'],[jsonrsp['Container'][0]['Contents']['Items'][titles]['Cast'].split(', ')][0],jsonrsp['Container'][0]['Contents']['Items'][titles]['Director'],jsonrsp['Container'][0]['Contents']['Items'][titles]['Writer'],jsonrsp['Container'][0]['Contents']['Items'][titles]['Duration'],genre,jsonrsp['Container'][0]['Contents']['Items'][titles]['SeriesName'].encode('utf-8', 'ignore')+' Sezon '+str(jsonrsp['Container'][0]['Contents']['Items'][titles]['SeasonIndex'])+' odc. '+str(jsonrsp['Container'][0]['Contents']['Items'][titles]['Index']),jsonrsp['Container'][0]['Contents']['Items'][titles]['OriginalName'],jsonrsp['Container'][0]['Contents']['Items'][titles]['ProductionYear'],5,date,allowplay)
			else:
				#Seriál
				xbmcplugin.setContent(int(sys.argv[1]), 'season')
				plot = jsonrsp['Container'][0]['Contents']['Items'][titles].get( 'Description', None )
				if plot is None:
					plot = jsonrsp['Container'][0]['Contents']['Items'][titles].get( 'Abstract', None )
				if plot is None:
					plot = ''
				plot.encode('utf-8', 'ignore')
				addDir(jsonrsp['Container'][0]['Contents']['Items'][titles]['Name'].encode('utf-8', 'ignore'),jsonrsp['Container'][0]['Contents']['Items'][titles]['ObjectUrl'],plot,2,jsonrsp['Container'][0]['Contents']['Items'][titles]['BackgroundUrl'])



#Seriál
def SEASON(url):
	xbmcplugin.setContent(int(sys.argv[1]), 'season')
	req = urllib2.Request(url, None, loggedin_headers)
	opener = urllib2.build_opener()
	f = opener.open(req)
	jsonrsp = json.loads(f.read())

	try:
		if jsonrsp['ErrorMessage']:
			xbmcgui.Dialog().ok('Błąd', jsonrsp['ErrorMessage'])
	except:
		pass
	for season in range(0, len(jsonrsp['Parent']['ChildContents']['Items'])):
		plot = jsonrsp['Parent']['ChildContents']['Items'][season].get( 'Description', None )
		if plot is None:
			plot = jsonrsp['Parent']['ChildContents']['Items'][season].get( 'Abstract', None )
		if plot is None:
			plot = ''
		plot.encode('utf-8', 'ignore')
		addDir(jsonrsp['Parent']['ChildContents']['Items'][season]['Name'].encode('utf-8', 'ignore'),jsonrsp['Parent']['ChildContents']['Items'][season]['ObjectUrl'],plot,3,jsonrsp['Parent']['ChildContents']['Items'][season]['BackgroundUrl'])




#Epizody
def EPISODE(url):
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED)
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_DATE)
	xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_TITLE)
	xbmcplugin.setContent(int(sys.argv[1]), 'episode')
	req = urllib2.Request(url, None, loggedin_headers)
	opener = urllib2.build_opener()
	f = opener.open(req)
	jsonrsp = json.loads(f.read())

	try:
		if jsonrsp['ErrorMessage']:
			xbmcgui.Dialog().ok('Błąd', jsonrsp['ErrorMessage'])
	except:
		pass

	for episode in range(0, len(jsonrsp['ChildContents']['Items'])):
		plot = jsonrsp['ChildContents']['Items'][episode].get( 'Abstract', None )
		if plot is None:
			plot = ''
		plot.encode('utf-8', 'ignore')
		firstGenre = jsonrsp['Genre']
		secondGenre = jsonrsp['SecondaryGenre']
		genre = [firstGenre.capitalize(), secondGenre.capitalize()]
		date = jsonrsp['AvailabilityFrom']
		allowplay = jsonrsp['ChildContents']['Items'][episode].get( 'AllowPlay', None )
		if allowplay is None:
			allowplay = False
		addLink(jsonrsp['ChildContents']['Items'][episode]['ObjectUrl'],plot,jsonrsp['ChildContents']['Items'][episode]['AgeRating'],jsonrsp['ChildContents']['Items'][episode]['ImdbRate'],jsonrsp['ChildContents']['Items'][episode]['BackgroundUrl'],[jsonrsp['ChildContents']['Items'][episode]['Cast'].split(', ')][0],jsonrsp['ChildContents']['Items'][episode]['Director'],jsonrsp['ChildContents']['Items'][episode]['Writer'],jsonrsp['ChildContents']['Items'][episode]['Duration'],genre,jsonrsp['ChildContents']['Items'][episode]['SeriesName'].encode('utf-8', 'ignore')+' Sezon '+str(jsonrsp['ChildContents']['Items'][episode]['SeasonIndex'])+' '+jsonrsp['ChildContents']['Items'][episode]['Name'].encode('utf-8', 'ignore'),jsonrsp['ChildContents']['Items'][episode]['OriginalName'],jsonrsp['ChildContents']['Items'][episode]['ProductionYear'],5,date,allowplay)


#Načítání videa
def PLAY(url):
	global goToken
	global individualization
	global customerId
	global GOcustomerId
	global sessionId
	global loggedin_headers

	#Přihlaste se, pokud je uživatel anonymní
	if sessionId == '00000000-0000-0000-0000-000000000000':
		if LOGIN() == False:
			return
			
	#Titulky
	if se=='true':
		try:
			req = urllib2.Request('http://czapi.hbogo.eu/v7/Content/json/CES/ANMO/'+cid, None, loggedin_headers)
			req.add_header('User-Agent', MUA)
			opener = urllib2.build_opener()
			f = opener.open(req)
			jsonrsps = json.loads(f.read())
			
			#Stáhneme oficiální titulky k epizodě ve formátu TTML a převedeme je na SRT
			try:
				if jsonrsps['Subtitles'][0]['Code']==Code:
					slink = jsonrsps['Subtitles'][0]['Url']
				elif jsonrsps['Subtitles'][1]['Code']==Code:
					slink = jsonrsps['Subtitles'][1]['Url']
				req = urllib2.Request(slink, None, loggedin_headers)
				response = urllib2.urlopen(req)
				data=response.read()
				response.close()
					
				subs = re.compile('<p[^>]+begin="([^"]+)\D(\d+)"[^>]+end="([^"]+)\D(\d+)"[^>]*>([\w\W]+?)</p>').findall(data)
				row = 0
				buffer = ''
				for sub in subs:
					row = row + 1
					buffer += str(row) +'\n'
					buffer += "%s,%03d" % (sub[0], int(sub[1])) + ' --> ' + "%s,%03d" % (sub[2], int(sub[3])) + '\n'
					buffer += urllib.unquote_plus(sub[4]).replace('<br/>','\n').replace('<br />','\n').replace("\r\n", "").replace("&lt;", "<").replace("&gt;", ">").replace("\n    ","").strip()
					buffer += '\n\n'
					sub = 'true'
					with open(srtsubs_path, "w") as subfile:
						subfile.write(buffer)
				#Výjimka pro nesprávné titulky
				if sub != 'true':
					raise Exception()
					
			except:
				sub = 'false'
		except:
			sub = 'false'
	
	
	#Zadanie manifestu ism
	purchase_payload = '<Purchase xmlns="go:v7:interop" xmlns:i="http://www.w3.org/2001/XMLSchema-instance"><AllowHighResolution>true</AllowHighResolution><ContentId>'+cid+'</ContentId><CustomerId>'+GOcustomerId+'</CustomerId><Individualization>'+individualization+'</Individualization><OperatorId>'+op_id+'</OperatorId><IsFree>false</IsFree><RequiredPlatform>COMP</RequiredPlatform><UseInteractivity>false</UseInteractivity></Purchase>'

	purchase_headers = {
		'Accept': 'application/json, text/javascript, */*; q=0.01',
		'Accept-Encoding': '',
		'Accept-Language': 'en-US,en;q=0.8',
		'Connection': 'keep-alive',
		'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
		'GO-CustomerId': str(GOcustomerId),
		'GO-requiredPlatform': 'CHBR',
		'GO-SessionId': str(sessionId),
		'GO-swVersion': '4.7.4',
		'GO-Token': str(goToken),
		'Origin': 'https://www.hbogo.cz',
		'User-Agent': UA
		}

	req = urllib2.Request('https://czapi.hbogo.eu/v7/Purchase/Json/CES/COMP', purchase_payload, purchase_headers)
	opener = urllib2.build_opener()
	f = opener.open(req)
	jsonrspp = json.loads(f.read())

	try:
		if jsonrspp['ErrorMessage']:
			xbmcgui.Dialog().ok('Chyba',jsonrspp['ErrorMessage'])
	except:
		pass

	MediaUrl = jsonrspp['Purchase']['MediaUrl'] + "/Manifest"

	PlayerSessionId = jsonrspp['Purchase']['PlayerSessionId']
	x_dt_auth_token = jsonrspp['Purchase']['AuthToken']
	dt_custom_data = base64.b64encode("{\"userId\":\"" + GOcustomerId + "\",\"sessionId\":\"" + PlayerSessionId + "\",\"merchant\":\"hboeurope\"}")

	#Přehrajte video
	is_helper = inputstreamhelper.Helper('mpd', drm='com.widevine.alpha')
	if not is_helper.check_inputstream():
		return False

	li = xbmcgui.ListItem(iconImage=thumbnail, thumbnailImage=thumbnail, path=MediaUrl)
	if (se=='true' and sub=='true'): #Pokud je tento režim vybrán, nastavte externí titulky
		li.setSubtitles([srtsubs_path])
	license_server = 'https://lic.drmtoday.com/license-proxy-widevine/cenc/'
	license_headers = 'dt-custom-data=' + dt_custom_data + '&x-dt-auth-token=' + x_dt_auth_token + '&Origin=https://www.hbogo.cz&Content-Type='
	license_key = license_server + '|' + license_headers + '|R{SSM}|JBlicense'

	li.setProperty('inputstreamaddon', 'inputstream.adaptive')
	li.setProperty('inputstream.adaptive.manifest_type', 'ism')
	li.setProperty('inputstream.adaptive.license_type', 'com.widevine.alpha')
	li.setProperty('inputstream.adaptive.license_data', 'ZmtqM2xqYVNkZmFsa3Izag==')
	li.setProperty('inputstream.adaptive.license_key', license_key)
	
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, li)


#Vyhledávání
def SEARCH():
	keyb = xbmc.Keyboard(search_string, 'Vyhledávání filmů, seriálů ...')
	keyb.doModal()
	searchText = ''
	if (keyb.isConfirmed()):
		searchText = urllib.quote_plus(keyb.getText())
		if searchText == "":
			addDir('Návrat - neexistují žádné výsledky odpovídající vašemu vyhledávání','','','',md+'DefaultFolderBack.png')
		else:
			#Záznam posledního dotazu
			__settings__.setSetting('lastsearch', searchText)
			#Hledej
			req = urllib2.Request('https://czapi.hbogo.eu/v7/Search/Json/CES/ANMO/'+searchText.decode('utf-8', 'ignore').encode('utf-8', 'ignore')+'/0/0/0/0/0/1', None, loggedin_headers)
			opener = urllib2.build_opener()
			f = opener.open(req)
			jsonrsp = json.loads(f.read())        

			try:
				if jsonrsp['ErrorMessage']:
					xbmcgui.Dialog().ok('Błąd', jsonrsp['ErrorMessage'])
			except:
				pass

			br=0
			for index in range(0, len(jsonrsp['Container'][0]['Contents']['Items'])):
				allowplay = jsonrsp['Container'][0]['Contents']['Items'][index].get( 'AllowPlay', None )
				if (jsonrsp['Container'][0]['Contents']['Items'][index]['ContentType'] == 1 or jsonrsp['Container'][0]['Contents']['Items'][index]['ContentType'] == 7): #1,7=MOVIE/EXTRAS, 2=SERIES(serial), 3=SERIES(episode)
					#Film
					addLink(jsonrsp['Container'][0]['Contents']['Items'][index]['ObjectUrl'],'',jsonrsp['Container'][0]['Contents']['Items'][index]['AgeRating'],jsonrsp['Container'][0]['Contents']['Items'][index]['ImdbRate'],jsonrsp['Container'][0]['Contents']['Items'][index]['BackgroundUrl'],[jsonrsp['Container'][0]['Contents']['Items'][index]['Cast'].split(', ')][0],jsonrsp['Container'][0]['Contents']['Items'][index]['Director'],jsonrsp['Container'][0]['Contents']['Items'][index]['Writer'],jsonrsp['Container'][0]['Contents']['Items'][index]['Duration'],jsonrsp['Container'][0]['Contents']['Items'][index]['Genre'],jsonrsp['Container'][0]['Contents']['Items'][index]['Name'].encode('utf-8', 'ignore'),jsonrsp['Container'][0]['Contents']['Items'][index]['OriginalName'],jsonrsp['Container'][0]['Contents']['Items'][index]['ProductionYear'],5,'',True)
				elif jsonrsp['Container'][0]['Contents']['Items'][index]['ContentType'] == 3:
					#Epizoda
					addLink(jsonrsp['Container'][0]['Contents']['Items'][index]['ObjectUrl'],'',jsonrsp['Container'][0]['Contents']['Items'][index]['AgeRating'],jsonrsp['Container'][0]['Contents']['Items'][index]['ImdbRate'],jsonrsp['Container'][0]['Contents']['Items'][index]['BackgroundUrl'],[jsonrsp['Container'][0]['Contents']['Items'][index]['Cast'].split(', ')][0],jsonrsp['Container'][0]['Contents']['Items'][index]['Director'],jsonrsp['Container'][0]['Contents']['Items'][index]['Writer'],jsonrsp['Container'][0]['Contents']['Items'][index]['Duration'],jsonrsp['Container'][0]['Contents']['Items'][index]['Genre'],jsonrsp['Container'][0]['Contents']['Items'][index]['SeriesName'].encode('utf-8', 'ignore')+' '+jsonrsp['Container'][0]['Contents']['Items'][index]['Name'].encode('utf-8', 'ignore'),jsonrsp['Container'][0]['Contents']['Items'][index]['OriginalName'],jsonrsp['Container'][0]['Contents']['Items'][index]['ProductionYear'],5,'',True)
				else:
					#Seriál
					addDir(jsonrsp['Container'][0]['Contents']['Items'][index]['Name'].encode('utf-8', 'ignore'),jsonrsp['Container'][0]['Contents']['Items'][index]['ObjectUrl'],'',2,jsonrsp['Container'][0]['Contents']['Items'][index]['BackgroundUrl'])
				br=br+1
			if br==0:
				addDir('Návrat - neexistují žádné výsledky odpovídající vašemu vyhledávání','','','',md+'DefaultFolderBack.png')


def addLink(ou,plot,ar,imdb,bu,cast,director,writer,duration,genre,name,on,py,mode,date,playble):
	cid = ou.rsplit('/',2)[1]
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&cid="+cid+"&thumbnail="+bu
	ok=True
	if playble:
		playble = 'true'
	else:
		playble = 'false'
		u = ''
		name = name + ' - Brzy'
	liz=xbmcgui.ListItem(name, iconImage=bu, thumbnailImage=bu)
	liz.setProperty("IsPlayable" , playble)
	liz.setArt({ 'thumb': bu,'poster': bu, 'banner' : bu, 'fanart': bu })
	liz.setInfo( type="Video", infoLabels={'plot': plot, "mpaa": str(ar)+'+', "rating": imdb, "cast": cast, "director": director, "writer": writer, "duration": duration, "genre": genre, "title": name, "originaltitle": on, "year": py, "date": date, 'sorttitle': name , 'aired': date} )
	liz.addStreamInfo('video', { 'width': 1280, 'height': 720 })
	liz.addStreamInfo('video', { 'aspect': 1.78, 'codec': 'h264' })
	liz.addStreamInfo('audio', { 'codec': 'aac', 'channels': 2 })

	contextmenu = []
	contextmenu.append(('Informace', 'XBMC.Action(Info)'))
	liz.addContextMenuItems(contextmenu)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	return ok



#Modul pro přidání samostatného adresáře a jeho atributů do obsahu katalogu Kodi
def addDir(name,url,plot,mode,iconimage):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": plot } )

	print("plot: "+str(plot.count))
	if len(plot)>0:
		contextmenu = []
		contextmenu.append(('Informace', 'XBMC.Action(Info)'))
		liz.addContextMenuItems(contextmenu)

	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok


def get_params():
	param=[]
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
		params=sys.argv[2]
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:
				param[splitparams[0]]=splitparams[1]
	return param

params=get_params()
url=None
name=None
iconimage=None
mode=None

try:
		url=urllib.unquote_plus(params["url"])
except:
		pass
try:
		name=urllib.unquote_plus(params["name"])
except:
		pass
try:
		thumbnail=str(params["thumbnail"])
except:
		pass
try:
		mode=int(params["mode"])
except:
		pass
try:
		cid=str(params["cid"])
except:
		pass


#Seznam jednotlivých modulů v tomto pluginu - musí plně odpovídat výše uvedenému kódu
if mode==None or url==None or len(url)<1:
		CATEGORIES()

elif mode==1:
		LIST(url)

elif mode==2:
		SEASON(url)

elif mode==3:
		EPISODE(url)
		
elif mode==4:
		SEARCH()

elif mode==5:
		PLAY(url)

elif mode==6:
		SILENTREGISTER()

elif mode==7:
		LOGIN()


xbmcplugin.endOfDirectory(int(sys.argv[1]))
