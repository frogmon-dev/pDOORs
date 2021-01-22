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

# 프로그램 시작	
GLOB.directoryInit(GLOB.whoami(), "DOORs")

configFileNM = COM.gHomeDir+COM.gSetupFile
controlFileNM = COM.gHomeDir+COM.gControlFile

user_id   = GLOB.readConfig(configFileNM, 'SETUP', 'user_id', '0')
dev_id    = GLOB.readConfig(configFileNM, 'AGENT', 'id', '0')

# 함수 정의
mWhoami = GLOB.whoami()
mUsbDir = "/mnt/usb_stick"
mFaceDir = COM.gHomeDir + "faces/"

GLOB.folderMaker(mFaceDir)

print("whoami = %s" % mWhoami)
print("usb dir = %s" % mUsbDir)
print("face home dir = %s" % mFaceDir)

mSourcePath = []

def usbDir():
	return os.listdir(mUsbDir)

def copyFileList(srcPath, destPath):
	print("copyFileList (%s=>%s)" % (srcPath, destPath))
	if not GLOB.folderExitst(srcPath):
		return False
	try:
		files = os.listdir(destPath)
		print(files)
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

# ASSUMED THAT THIS COMMAND HAS ALREADY BEEN RUN
# sudo mkdir /mnt/usb_stick

def run_command(command):
	# start = time.time()
	ret_code, output = subprocess.getstatusoutput(command)
	if ret_code == 1:
		#raise Exception("FAILED: %s" % command)
		print("FAILED: %s" % command)
	# end = time.time()
	# print "Finished in %s seconds" % (end - start)
	return output.splitlines() 

def uuid_from_line(line):
	start_str = "UUID=\""
	example_uuid = "6784-3407"
	uuid_start = line.index(start_str) + len(start_str)
	uuid_end = uuid_start + len(example_uuid)
	return line[uuid_start: uuid_end]

checkDir = 0
while True:
	time.sleep(1)

	try:
		output = run_command("sudo blkid | grep -v boot | grep -v mm")
		if len(output) > 0:
			# ['/dev/sda1: LABEL="KINGSTON" UUID="6784-3407" TYPE="vfat" PARTUUID="459720e1-01"']
			for usb_device in output:
				if not GLOB.folderExitst(mUsbDir):
					run_command("sudo mkdir %s" % mUsbDir)
				command = "sudo mount --uuid %s %s -o iocharset=utf8" % (uuid_from_line(usb_device), mUsbDir)
				print(command)
				run_command(command)
				break

			if copyFileList("/mnt/usb_stick/faces/", mFaceDir):
				LOG.writeLn("[face_copy]: Sucess!!")
				time.sleep(5)
				run_command("sudo reboot")
	except Exception as e :
		print("usb not detected or faces not found: %s" % e)
