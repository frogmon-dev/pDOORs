#uGlobal.py

import os
import re
import subprocess
import json

from unidecode       import unidecode
from datetime        import datetime, timedelta

from frogmon.uCommon import COM
from frogmon.uConfig import CONF

class GLOB:
	def __init__(self):
		print('init')

  ## 파일명 검색
	def getJsonFile(dirname, word):
		filenames = os.listdir(dirname)
		rc = []

		for filename in filenames:
			full_filename = os.path.join(dirname, filename)
			if word in full_filename:
				if ('save' not in full_filename) :
					rc.append(full_filename)
		return rc	

	def loadJsonFile(fileName: str):
		f = open(fileName, 'r')
		data = ''.join(f.read().split())
		f.close()
		return data

	def setUpdateTime():
		COM.gNOW  = datetime.now()
		COM.gYYYY = COM.gNOW.strftime('%Y')
		COM.gMM   = COM.gNOW.strftime('%m')
		COM.gDD   = COM.gNOW.strftime('%d')
		COM.gHH   = COM.gNOW.strftime('%H')
		COM.gNN   = COM.gNOW.strftime('%M')
		COM.gSS   = COM.gNOW.strftime('%S')
		COM.gstrYMD = COM.gNOW.strftime('%Y%m%d')
		COM.gstrYMDHMS = COM.gNOW.strftime('%Y%m%d%H%M%S')
		COM.gstrDATE = COM.gNOW.strftime('%Y-%m-%d %H:%M:%S')
		COM.gstrTIME = COM.gNOW.strftime('%H:%M:%S')
		

	def betweenNow(strTm: str):
		convert_date = datetime.strptime(strTm, '%Y%m%d%H%M%S')
		now = datetime.now()
		return (now - convert_date).seconds
		

	def remoteFileFind(path):    
		file_list = os.listdir(path)
		file_list_remote = [file for file in file_list if file.startswith("remote_")]
		return file_list_remote
		
	# Making CSV function
	def makeCSVFile(data, fileName):
		print('fileName ='+fileName)
		print(data)
		if os.path.isfile(fileName) :
			f = open(fileName,'a', newline='')
			wr = csv.writer(f)
			wr.writerow(data)
			f.close()
		else :
			f = open(fileName,'w', newline='')
			wr = csv.writer(f)
			aRow = 'hhnnss', 'temp', 'humi', 'light', 'outTemp'
			wr.writerow(aRow)
			wr.writerow(data)
			f.close()

	# Identifier cleanup
	def clean_identifier(name):
		clean = name.strip()
		for this, that in [[' ', '-'], ['ä', 'ae'], ['Ä', 'Ae'], ['ö', 'oe'], ['Ö', 'Oe'], ['ü', 'ue'], ['Ü', 'Ue'], ['ß', 'ss']]:
			clean = clean.replace(this, that)
		clean = unidecode(clean)
		return clean
		
	def isMacAddress(mac):
		return re.match("[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}:[0-9a-f]{2}", mac.lower())

	def saveJsonData(fileName, opcode, data: str):
		if data:
			afterData = data.replace("'", "\"")
			dict = json.loads(afterData)
			with open(fileName, 'w', encoding='utf-8') as make_file:
				json.dump(dict, make_file, indent="\t")

	def fileExist(fileName):
		return os.path.isfile(fileName) 

	def readConfig(fileName, section, item, defult):
		if os.path.exists(fileName):
			try:
				config  = CONF(fileName)
				rc = config.readConfig(section, item, defult)
				return rc
			except Exception as e:
				print("error : %s" % e)
				return defult

	def writeConfig(fileName, section, item, value):
		if os.path.exists(fileName):
			try:
				config  = CONF(fileName)
				config.writeConfig(section, item, value)
				config.saveConfig()
				return True
			except Exception as e:
				print("error : %s" % e)
				return False
				
	def itemConfig(fileName, section):
		if os.path.exists(fileName):
			try:
				config  = CONF(fileName)
				return config.itemsConfig(section)
			except Exception as e:
				print("error : %s" % e)

	def showProcess():
		for proc in psutil.process_iter(attrs=['pid', 'name', 'username']):
			print(proc.info)

	def findProcess(userNM, procNM):
		rc = 0
		for proc in psutil.process_iter(attrs=['pid', 'name', 'username']):
			if proc.info['username'] == userNM:
				if proc.info['name'] == procNM :
					rc = proc.info['pid']
					#print(proc.info)
					break
		return rc
	
	def getOnlyFileName(filePath):
		x = filePath.split('/')
		x.reverse()
		return x[0]

	def folderMaker(directory):
		try:
			if not os.path.exists(directory):
				os.makedirs(directory)
		except OSError:
			print ('Error: Creating directory. ' +  directory)

	def whoami():
		rc = subprocess.check_output('whoami').decode('utf-8')
		return rc.strip('\n')

	def directoryInit(whoiam, prgNM):
		COM.gHomeDir   = '/home/%s/%s/bin/' % (whoiam, prgNM)
		COM.gLogDir    = COM.gHomeDir+'logs/'
		COM.gJsonDir   = COM.gHomeDir+'json/'	

	def getJsonVal(strJson, section, defVal):
		try:
			json_data = json.loads(strJson)
			return json_data[section]
		except Exception as e :
			#print("getJsonVal Error : '%s' [%s] : error[%s] " % (strJson, section, e))
			return defVal