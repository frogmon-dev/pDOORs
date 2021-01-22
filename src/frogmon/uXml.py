#uXml.py
from xml.etree import ElementTree

from frogmon.uCommon import COM
from frogmon.uConfig import CONF

class XMLPaser:
	def getHeader(content):
		xmlContents = content.decode("UTF-8").strip()#.replace("	","")
		#print('XML ---------------------')
		#print(xmlContents)
		#print('-------------------------')
		root        = ElementTree.fromstring(xmlContents)
		
		wHeader     = root.find("msgHeader")
		
		wHeaderCD   = wHeader.find("headerCd").text
		wHeaderMsg  = wHeader.find("headerMsg").text
		wOpcode     = wHeader.find("opcode").text
	
		if (wHeaderCD != 0):
			print('header Message : %s' % wHeaderMsg)
		
		return int(wHeaderCD)
		
	def decodeAction(content):
		xmlContents = content.decode("UTF-8").strip()#.replace("	","")
		#print('XML ---------------------')
		#print(xmlContents)
		#print('-------------------------')
		root        = ElementTree.fromstring(xmlContents)
		wBody       = root.find("msgBody")
		rc          = wBody.find("action").text
		#print(rc)
		return rc	
	
