from frogmon.uCommon import COM
from frogmon.uGlobal import GLOB
from frogmon.uRequest import REQUEST

# 프로그램 시작
GLOB.directoryInit('pi', "DOORs")

configFileNM  = COM.gHomeDir+COM.gSetupFile
user_id       = GLOB.readConfig(configFileNM, 'SETUP', 'user_id', '0')
dev_id        = GLOB.readConfig(configFileNM, 'AGENT', 'id', '0')

print('')
print('--------------------------------------------------')
print('**  Welcome to FROGMON corp.')
print("**  Let's make it together")
print("**  ")
print("**  config file check : %s" % configFileNM)
print("**  user_id     check : %s" % user_id)
print("**  dev_id      check : %s" % dev_id)
print("**  device.json check : %s" % COM.gJsonDir + 'device.json')
print('--------------------------------------------------')
print('')

REQUEST.updateDIYs(user_id, dev_id)
    