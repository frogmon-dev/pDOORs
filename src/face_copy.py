# -*- coding: utf-8 -*- 

# 중복 실행 방지
from tendo import singleton
try:
	me = singleton.SingleInstance()
except :
	print("another process running!")
	exit()


import sys, os
import time
import datetime
import glob
import subprocess
import shutil
 
from frogmon.uConfig     import CONF
from frogmon.uLogger     import LOG
from frogmon.uCommon     import COM
from frogmon.uGlobal     import GLOB
#from frogmon.ulogger import LOG

# 프로그램 시작	
GLOB.directoryInit(GLOB.whoami(), "DOORs")

configFileNM = COM.gHomeDir+COM.gSetupFile
controlFileNM = COM.gHomeDir+COM.gControlFile

user_id   = GLOB.readConfig(configFileNM, 'SETUP', 'user_id', '0')
dev_id    = GLOB.readConfig(configFileNM, 'AGENT', 'id', '0')

# 함수 정의
mWhoami = GLOB.whoami()
mUsbDir = "/media/%s/" % mWhoami
mFaceDir = COM.gHomeDir + "faces/"

GLOB.folderMaker(mFaceDir)

print("whoami = %s" % mWhoami)
print("usb dir = %s" % mUsbDir)
print("face home dir = %s" % mFaceDir)

mSourcePath = []

def usbDir():
	return os.listdir(mUsbDir)

def getDirs():
	dirs = []
	try:
		for usb in usbDir():
			dirs.append(r"%s%s/faces/" % (mUsbDir, usb))
	except Exception as e :
		print("[ERROR]: %s" % e)
	
	return dirs

def copyFileList(srcPath, destPath):
	print("copyFileList (%s=>%s)" % (srcPath, destPath))
	try:
		files = os.listdir(destPath)
		for afile in files:
			os.remove(destPath+afile)
		files = os.listdir(srcPath)
		for afile in files:
			shutil.copy(srcPath+afile, destPath+afile)
		return True
	except Exception as e :
		LOG.writeLn("[face_copy ERROR]: %s" % e)
		return False
 
print('')
print('--------------------------------------------------')
print('**  Welcome to FROGMON corp.')
print("**  Let's make it together")
print("**  ")
print('**  USER = %s' % user_id)
print('**  PRODUCT = %s' % dev_id)
print('--------------------------------------------------')
print('')

checkDir = 0
while True:
	time.sleep(1)

	Paths = []
	Paths = getDirs()
	if checkDir == 0:
		if len(Paths) > 0:	
			for aPath in Paths:
				if copyFileList(aPath, mFaceDir):
					LOG.writeLn("[face_copy]: Sucess!!")
					checkDir = 1
	else :
		if len(Paths) == 0:
			checkDir = 0

	
	

	