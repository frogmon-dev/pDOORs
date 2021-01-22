# uRequest.py

#-*- coding:utf-8 -*-

import requests
import urllib.parse

from datetime import datetime, timedelta

from frogmon.uCommon import COM
from frogmon.uGlobal import GLOB
from frogmon.uConfig import CONF
from frogmon.uLogger import LOG
from frogmon.uXml    import XMLPaser

class REQUEST():	
	def updateDIYs(user_id, dev_id):
		rc = -1
		if user_id == 'empty' or dev_id == 'empty' :
			LOG.writeLn("user_id or dev_id is empty")
			return rc
			
		phpFileNm = "call_from_DIYs.php"
		
		fileName = COM.gJsonDir + 'device.json'
		if GLOB.fileExist(fileName) :
			f = open(fileName, 'r')
			data = f.read()
			print(data)
			f.close()
		else:
			data = "{}"

		url = 'https://frogmon.synology.me/svr_api/'
		url = '%s%s' % (url, phpFileNm)
		r = requests.post(url, data={'user_id': user_id, 'product_id': dev_id, 'status_json': data})
		#print(r.url)
		if (XMLPaser.getHeader(r.content) != 0):
			LOG.writeLn("sendModuleStat send Error ")	
			rc = -1
		else:
			actionJson = XMLPaser.decodeAction(r.content)
			if actionJson == '':
				print('no Actions')
			else :
				GLOB.saveJsonData(COM.gJsonDir+'action.json', '0x11', actionJson)
			rc = 0
		return rc

	def checkProduct(user_id, dev_id, macAddr):
		rc = -1
		if user_id == 'empty' or dev_id == 'empty' :
			LOG.writeLn("user_id or dev_id is empty")
			return rc
			
		phpFileNm = "product_login.php"
		
		url = 'https://frogmon.synology.me/svr_api/'
		url = '%s%s' % (url, phpFileNm)
		params = {'user_id': user_id, 'product_id': dev_id, 'mac_address' : macAddr}
		r = requests.get(url, params=params)
		print(r.url)
		if (XMLPaser.getHeader(r.content) != 0):
			LOG.writeLn("sendModuleStat send Error ")
		else:
			rc = 0
		
		return rc

