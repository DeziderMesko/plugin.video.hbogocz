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

__addon_id__= 'plugin.video.hbogopl'
__Addon = xbmcaddon.Addon(__addon_id__)
__settings__ = xbmcaddon.Addon(id='plugin.video.hbogopl')

UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'
MUA = 'Dalvik/2.1.0 (Linux; U; Android 8.0.0; Nexus 5X Build/OPP3.170518.006)'

se = __settings__.getSetting('se')
language = __settings__.getSetting('language')
if language == '0':
	lang = 'Polish'
	Code = 'POL'
	srtsubs_path = xbmc.translatePath('special://temp/hbogo.Polish.Forced.srt')
elif language == '1':
	lang = 'Polish'
	Code = 'POL'
	srtsubs_path = xbmc.translatePath('special://temp/hbogo.Polish.Forced.srt')
elif language == '2':
	lang = 'English'
	Code = 'ENG'
	srtsubs_path = xbmc.translatePath('special://temp/hbogo.English.Forced.srt')
	

md = xbmc.translatePath(__Addon.getAddonInfo('path') + "/resources/media/")
search_string = urllib.unquote_plus(__settings__.getSetting('lastsearch'))

operator = __settings__.getSetting('operator')
op_ids = [
'00000000-0000-0000-0000-000000000000', # Anonymous NonAuthenticated
'07b113ce-1c12-4bfd-9823-db951a6b4e87', # nc+
'a35f8cd2-05d7-4c0f-832f-0ddfad3b585d', # Plus
'c5ff7517-8ef8-4346-86c7-0fb328848671', # UPC
'7021fee7-bab1-4b4b-b91c-a2dc4fdd7a05', # Vectra
'22eaaeb6-1575-419f-9f1b-af797e86b9ee', # PLAY
'598a984f-bc08-4e77-896b-a82d8d6ea8de', # Multimedia Polska
'c454b13c-5c82-4a01-854f-c34b2901d1b2', # Netia
'48b81f9b-cb72-48cd-85d2-e952f78137c0', # Orange
'82ae5dfd-9d29-4059-a843-2aa16449c42a', # INEA
'357890f0-2698-445b-8712-b82f715b0648', # TOYA
'5eb57ea8-9cd7-4bbf-8c6c-e56b186dd5c0', # JAMBOX
'2e0325fa-d4b3-41eb-a9e4-0a36ee59aec5', # PROMAX
'892771be-a48c-46ab-a0d0-3f51cdc50cf2', # Asta-Net
'6a47f04f-cdd6-428b-abb5-135e38a43b38', # TK Chopin
'36f365ac-4ca2-4e8b-9b21-14479e5fe6bb', # ELSAT
'99eed640-107c-4732-81d0-59305ff6b520', # Eltronik
'f7f4d300-23ab-4b79-bb35-49568eb7cd4a', # SatFilm
'5893f3c1-0bcd-4ae3-b434-45666925b5d1', # Master
'8f34fcd8-3b74-4c16-b91c-c8375ab3ffdb', # STANSAT
'878e69aa-be98-4a7d-a08e-b11c7330d8b3', # Dialog
'b49a6c5d-033d-4bf1-b273-37ba188aef97', # Internetia
'62f7b31b-c866-4ff3-a7a1-800fac10de16', # Petrotel
'1366289b-86ae-4695-8d4b-a6b14eacdd8b', # Cinema City – promocja
'64d88671-b490-44b9-b1ee-e145347732b3', # Samsung - promocja
'57332e2f-958c-4a83-86cc-e569842868a2', # Player+
'b7018ed3-1858-4436-8e7f-d92a6d0b9bfc', # HBO GO Vip/Club Poland
'dbaf3435-6ee2-4a79-af13-dac5a1c550a3', # HBO Polska
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
	'Referer': 'https://www.hbogo.pl/',
	'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
	'Origin': 'https://www.hbogo.pl',
	'X-Requested-With': 'XMLHttpRequest',
	'GO-Language': 'POL',
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
'Origin': 'https://hbogo.pl',
'Accept-Encoding': '',
'Accept-Language': 'en-US,en;q=0.9',
'User-Agent': UA,
'Content-Type': 'application/json',
'Accept': '*/*',
'Referer': 'https://hbogo.pl/',
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
'OperatorName':'HBO Poland',
'Language':'POL',
'CustomerCode':'',
'ServiceCode':'HBO_Premium',
'CountryName':'Poland',
'AppLanguage':'POL',
'AudioLanguage':'POL',
'DefaultSubtitleLanguage':'POL',
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



# Zapisz dane uwierzytelniania na stałe; jest wykonywane raz
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


# Zarejestruj urządzenie na platformie; jest wykonywane raz
def SILENTREGISTER():
	global goToken
	global individualization
	global customerId
	global sessionId
	
	#За HBO Polska
	if op_id =='dbaf3435-6ee2-4a79-af13-dac5a1c550a3':
		payload = LOGINVIAHBOPAYLOAD("")
		req = urllib2.Request('https://api.ugw.hbogo.eu/v3.0/Authentication/POL/JSON/POL/COMP', json.dumps(payload), loggedviahbo_headers)
		opener = urllib2.build_opener()
		f = opener.open(req)
		jsonrsp = json.loads(f.read())
		try:
			if jsonrsp['ErrorMessage']:
				xbmcgui.Dialog().ok('Błąd', jsonrsp['Error'])
		except:
			#goToken = jsonrsp['Token']
			sessionId = jsonrsp['SessionId']
			custid = jsonrsp['Customer']['Id']
			indiv = jsonrsp['Customer']['CurrentDevice']['Individualization']
			storeIndiv(indiv, custid)
		
	#За inni operatorzy
	else:
		req = urllib2.Request('https://pl.hbogo.eu/services/settings/silentregister.aspx', None, loggedin_headers)
		
		opener = urllib2.build_opener()
		f = opener.open(req)
		jsonrsp = json.loads(f.read())

		if jsonrsp['Data']['ErrorMessage']:
			xbmcgui.Dialog().ok('Błąd', jsonrsp['Data']['ErrorMessage'])
		else:
			indiv = jsonrsp['Data']['Customer']['CurrentDevice']['Individualization']
			custid = jsonrsp['Data']['Customer']['CurrentDevice']['Id']
			storeIndiv(indiv, custid)
			sessionId = jsonrsp['Data']['SessionId']
	return jsonrsp

# Uwierzytelnianie; jest wykonywane przed otwarciem wideo
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
		xbmcgui.Dialog().ok('HBO GO', 'Podaj dane logowania w ustawieniach wtyczki.')
		xbmcaddon.Addon(id='plugin.video.hbogopl').openSettings("Konto")
		xbmc.executebuiltin("Container.Refresh")
		return False

	#За HBO Polska
	if op_id =='dbaf3435-6ee2-4a79-af13-dac5a1c550a3':
		payload = LOGINVIAHBOPAYLOAD(individualization)
		req = urllib2.Request('https://api.ugw.hbogo.eu/v3.0/Authentication/POL/JSON/POL/COMP', json.dumps(payload), loggedviahbo_headers)
		opener = urllib2.build_opener()
		f = opener.open(req)
		jsonrspl = json.loads(f.read())
		
		try:
			if jsonrspl['Data']['ErrorMessage']:
				xbmcgui.Dialog().ok('Błąd', jsonrspl['Data']['ErrorMessage'])
		except:
			pass
		
		sessionId = jsonrspl['SessionId']
		if sessionId == '00000000-0000-0000-0000-000000000000':
			xbmcgui.Dialog().ok('Logowanie nie powiodło się','Sprawdź, czy poprawnie wpisałeś dane logowania w ustawieniach i spróbuj ponownie.')
			xbmcaddon.Addon(id='plugin.video.hbogopl').openSettings("Konto")
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
			'Referer': 'https://www.hbogo.pl/',
			'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
			'GO-Language': 'POL',
			'GO-Individualization': individualization,
			'GO-Token': goToken,
			'GO-SessionId': sessionId,
			'GO-CustomerId': GOcustomerId,
			'GO-swVersion': '4.8.0',
			'GO-requiredPlatform': 'CHBR',
			'GO-Customer': go_customer,
			'X-Requested-With': 'XMLHttpRequest',
			'Origin': 'https://www.hbogo.pl',
			'Connection': 'keep-alive'
			}
		
		usernamekey = 'EmailAddress'
		
		# UPC
		if op_id =='c5ff7517-8ef8-4346-86c7-0fb328848671':
			usernamekey = 'Nick'

		sn_payload = urllib.urlencode({'OperatorId': op_id, usernamekey: username, 'Password': password})
		req = urllib2.Request('https://pl.hbogo.eu/services/settings/signin.aspx', sn_payload, sn_headers)
		opener = urllib2.build_opener()
		f = opener.open(req)
		jsonrspl = json.loads(f.read())
		
		try:
			if jsonrspl['Data']['ErrorMessage']:
				xbmcgui.Dialog().ok('Błąd', jsonrspl['Data']['ErrorMessage'])
		except:
			pass
		
		sessionId = jsonrspl['Data']['SessionId']
		if sessionId == '00000000-0000-0000-0000-000000000000':
			xbmcgui.Dialog().ok('Logowanie nie powiodło się','Sprawdź, czy poprawnie wpisałeś dane logowania w ustawieniach i spróbuj ponownie.')
			xbmcaddon.Addon(id='plugin.video.hbogopl').openSettings("Konto")
			xbmc.executebuiltin("Action(Back)")
		else:
			#xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(username,'Czas na popcorn!', 4000, md+'DefaultUser.png'))
		
			goToken = jsonrspl['Data']['Token']
			GOcustomerId = jsonrspl['Data']['Customer']['Id']
		
			loggedin_headers['GO-SessionId'] = str(sessionId)
			loggedin_headers['GO-Token'] = str(goToken)
			loggedin_headers['GO-CustomerId'] = str(GOcustomerId)




#Kategorie
def CATEGORIES():
	addDir('Wyszukiwanie filmów, seriali ...','search','',4,md+'DefaultAddonsSearch.png')
	#Pobieranie kategorii
	req = urllib2.Request('http://plapi.hbogo.eu/v7/Groups/json/POL/ANMO/0/True', None, loggedin_headers)
	opener = urllib2.build_opener()
	f = opener.open(req)
	jsonrsp = json.loads(f.read())

	try:
		if jsonrsp['ErrorMessage']:
			xbmcgui.Dialog().ok('Błąd', jsonrsp['ErrorMessage'])
	except:
		pass
	#Lista kategorii
	for cat in range(0, 3): #Do 3, aby uwzględnić fałszywą kategorię Kids oraz moja lista
		addDir(jsonrsp['Items'][cat]['Name'].encode('utf-8', 'ignore'),jsonrsp['Items'][cat]['ObjectUrl'],'',1,md+'DefaultFolder.png')
	#Ręcznie dodana kategoria Kids
	addDir(jsonrsp['Items'][3]['Name'].encode('utf-8', 'ignore'),'http://plapi.hbogo.eu/v7/Group/json/POL/ANMO/b071fcca-7b15-459d-9b2a-53b108d1df6c/0/0/0/0/0/0/True','',1,md+'DefaultFolder.png')
	addDir('Moja lista','http://plapi.hbogo.eu/v7/CustomerGroup/json/POL/ANMO/c79efa9f-be92-4bfd-90d8-31a9c30d4b80/0/0/0/0/0/0/false','',1,md+'DefaultFolder.png')


#Zawartosc kategorii
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
			xbmcgui.Dialog().ok('Błąd', jsonrsp['ErrorMessage'])
	except:
		pass
	#Jeśli istnieje podkategoria / gatunki
	if len(jsonrsp['Container']) > 1:
		for Container in range(0, len(jsonrsp['Container'])):
			addDir(jsonrsp['Container'][Container]['Name'].encode('utf-8', 'ignore'),jsonrsp['Container'][Container]['ObjectUrl'],'',1,md+'DefaultFolder.png')
	else:
		xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_UNSORTED)
		xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_DATE)
		xbmcplugin.addSortMethod( handle=int( sys.argv[ 1 ] ), sortMethod=xbmcplugin.SORT_METHOD_TITLE)
		#Jeśli nie ma podkategorii / gatunków
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
				#Odcinek serialu
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
				#Seria
				xbmcplugin.setContent(int(sys.argv[1]), 'season')
				plot = jsonrsp['Container'][0]['Contents']['Items'][titles].get( 'Description', None )
				if plot is None:
					plot = jsonrsp['Container'][0]['Contents']['Items'][titles].get( 'Abstract', None )
				if plot is None:
					plot = ''
				plot.encode('utf-8', 'ignore')
				addDir(jsonrsp['Container'][0]['Contents']['Items'][titles]['Name'].encode('utf-8', 'ignore'),jsonrsp['Container'][0]['Contents']['Items'][titles]['ObjectUrl'],plot,2,jsonrsp['Container'][0]['Contents']['Items'][titles]['BackgroundUrl'])



#Serie
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




#Odcinki
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


#Ładowanie wideo
def PLAY(url):
	global goToken
	global individualization
	global customerId
	global GOcustomerId
	global sessionId
	global loggedin_headers

	#Logowanie, jeśli użytkownik jest anonimowy
	if sessionId == '00000000-0000-0000-0000-000000000000':
		if LOGIN() == False:
			return
			
	#Napisy
	if se=='true':
		try:
			req = urllib2.Request('http://plapi.hbogo.eu/v7/Content/json/POL/ANMO/'+cid, None, loggedin_headers)
			req.add_header('User-Agent', MUA)
			opener = urllib2.build_opener()
			f = opener.open(req)
			jsonrsps = json.loads(f.read())
			
			#Pobieramy oficjalne napisy do odcinka w formacie TTML i konwertujemy je na SRT
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
				#Wyjątek dla niepoprawnych napisow
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
		'Origin': 'https://www.hbogo.pl',
		'User-Agent': UA
		}

	req = urllib2.Request('https://plapi.hbogo.eu/v7/Purchase/Json/POL/COMP', purchase_payload, purchase_headers)
	opener = urllib2.build_opener()
	f = opener.open(req)
	jsonrspp = json.loads(f.read())

	try:
		if jsonrspp['ErrorMessage']:
			xbmcgui.Dialog().ok('Błąd',jsonrspp['ErrorMessage'])
	except:
		pass

	MediaUrl = jsonrspp['Purchase']['MediaUrl'] + "/Manifest"

	PlayerSessionId = jsonrspp['Purchase']['PlayerSessionId']
	x_dt_auth_token = jsonrspp['Purchase']['AuthToken']
	dt_custom_data = base64.b64encode("{\"userId\":\"" + GOcustomerId + "\",\"sessionId\":\"" + PlayerSessionId + "\",\"merchant\":\"hboeurope\"}")

	#Odtwórz wideo
	is_helper = inputstreamhelper.Helper('mpd', drm='com.widevine.alpha')
	if not is_helper.check_inputstream():
		return False

	li = xbmcgui.ListItem(iconImage=thumbnail, thumbnailImage=thumbnail, path=MediaUrl)
	if (se=='true' and sub=='true'): #Ustaw zewnętrzne napisy, jeśli wybrany jest ten tryb
		li.setSubtitles([srtsubs_path])
	license_server = 'https://lic.drmtoday.com/license-proxy-widevine/cenc/'
	license_headers = 'dt-custom-data=' + dt_custom_data + '&x-dt-auth-token=' + x_dt_auth_token + '&Origin=https://www.hbogo.pl&Content-Type='
	license_key = license_server + '|' + license_headers + '|R{SSM}|JBlicense'

	li.setProperty('inputstreamaddon', 'inputstream.adaptive')
	li.setProperty('inputstream.adaptive.manifest_type', 'ism')
	li.setProperty('inputstream.adaptive.license_type', 'com.widevine.alpha')
	li.setProperty('inputstream.adaptive.license_data', 'ZmtqM2xqYVNkZmFsa3Izag==')
	li.setProperty('inputstream.adaptive.license_key', license_key)
	
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, li)


#Wyszukiwarka
def SEARCH():
	keyb = xbmc.Keyboard(search_string, 'Wyszukiwanie filmów, seriali ...')
	keyb.doModal()
	searchText = ''
	if (keyb.isConfirmed()):
		searchText = urllib.quote_plus(keyb.getText())
		if searchText == "":
			addDir('Wróć - nie ma wyników pasujących do wyszukiwania','','','',md+'DefaultFolderBack.png')
		else:
			#Zapis ostatniego zapytania
			__settings__.setSetting('lastsearch', searchText)
			#Wyszukaj
			req = urllib2.Request('https://plapi.hbogo.eu/v7/Search/Json/POL/ANMO/'+searchText.decode('utf-8', 'ignore').encode('utf-8', 'ignore')+'/0/0/0/0/0/1', None, loggedin_headers)
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
					#Odcinek
					addLink(jsonrsp['Container'][0]['Contents']['Items'][index]['ObjectUrl'],'',jsonrsp['Container'][0]['Contents']['Items'][index]['AgeRating'],jsonrsp['Container'][0]['Contents']['Items'][index]['ImdbRate'],jsonrsp['Container'][0]['Contents']['Items'][index]['BackgroundUrl'],[jsonrsp['Container'][0]['Contents']['Items'][index]['Cast'].split(', ')][0],jsonrsp['Container'][0]['Contents']['Items'][index]['Director'],jsonrsp['Container'][0]['Contents']['Items'][index]['Writer'],jsonrsp['Container'][0]['Contents']['Items'][index]['Duration'],jsonrsp['Container'][0]['Contents']['Items'][index]['Genre'],jsonrsp['Container'][0]['Contents']['Items'][index]['SeriesName'].encode('utf-8', 'ignore')+' '+jsonrsp['Container'][0]['Contents']['Items'][index]['Name'].encode('utf-8', 'ignore'),jsonrsp['Container'][0]['Contents']['Items'][index]['OriginalName'],jsonrsp['Container'][0]['Contents']['Items'][index]['ProductionYear'],5,'',True)
				else:
					#Seria
					addDir(jsonrsp['Container'][0]['Contents']['Items'][index]['Name'].encode('utf-8', 'ignore'),jsonrsp['Container'][0]['Contents']['Items'][index]['ObjectUrl'],'',2,jsonrsp['Container'][0]['Contents']['Items'][index]['BackgroundUrl'])
				br=br+1
			if br==0:
				addDir('Wróć - nie ma wyników pasujących do wyszukiwania','','','',md+'DefaultFolderBack.png')


def addLink(ou,plot,ar,imdb,bu,cast,director,writer,duration,genre,name,on,py,mode,date,playble):
	cid = ou.rsplit('/',2)[1]
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&cid="+cid+"&thumbnail="+bu
	ok=True
	if playble:
		playble = 'true'
	else:
		playble = 'false'
		u = ''
		name = name + ' - Wkrótce'
	liz=xbmcgui.ListItem(name, iconImage=bu, thumbnailImage=bu)
	liz.setProperty("IsPlayable" , playble)
	liz.setArt({ 'thumb': bu,'poster': bu, 'banner' : bu, 'fanart': bu })
	liz.setInfo( type="Video", infoLabels={'plot': plot, "mpaa": str(ar)+'+', "rating": imdb, "cast": cast, "director": director, "writer": writer, "duration": duration, "genre": genre, "title": name, "originaltitle": on, "year": py, "date": date, 'sorttitle': name , 'aired': date} )
	liz.addStreamInfo('video', { 'width': 1280, 'height': 720 })
	liz.addStreamInfo('video', { 'aspect': 1.78, 'codec': 'h264' })
	liz.addStreamInfo('audio', { 'codec': 'aac', 'channels': 2 })

	contextmenu = []
	contextmenu.append(('Informacje', 'XBMC.Action(Info)'))
	liz.addContextMenuItems(contextmenu)
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	return ok



#Moduł do dodawania oddzielnego katalogu i jego atrybutów do zawartości wyswietlanego katalogu Kodi
def addDir(name,url,plot,mode,iconimage):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": plot } )

	print("plot: "+str(plot.count))
	if len(plot)>0:
		contextmenu = []
		contextmenu.append(('Informacje', 'XBMC.Action(Info)'))
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


#Lista poszczególnych modułów w tej wtyczce - musi w pełni odpowiadać powyższemu kodowi
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
