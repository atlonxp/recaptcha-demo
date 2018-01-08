from configparser import ConfigParser
from ast import literal_eval
import pyautogui
pyautogui.PAUSE = 2.5
pyautogui.FAILSAFE = True

# self-defined
from utilities import imPath, getImage

# FYI
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(message)s', datefmt='%H:%M:%S')
#logging.disable(logging.INFO) # uncomment to block debug log messages

# Read the image parameters
logging.info('Reading the screenshot parameters from configure_initial.ini...')
config = ConfigParser()
config.read('config_initial.ini')

logging.info('Locating the screenshot of I am not robot...')
# location of checkbox of I am not robot
robotLoc = pyautogui.locateCenterOnScreen(imPath('images', 'reg.png'))

#click I am not a robot
pyautogui.click(robotLoc)

logging.info("Locating the screenshot of refresh...")
# location of refresh
refreshLoc = pyautogui.locateCenterOnScreen(imPath('images', 'refresh.png'))
# add 20 in Y direction taken into accout the offset introduced by error message
refreshLoc = (refreshLoc[0], refreshLoc[1] + 20)

# need to make sure street sign is shown
while(pyautogui.locateCenterOnScreen(imPath('images', 'ifstreet.png')) == None):
       # click the refresh button
       logging.info("Not street sign, refreshing...")
       pyautogui.click(refreshLoc)

# need to click one image to get next button
pyautogui.alert('Please manually select the answers so that next button is shown')
# location of next
nextLoc = pyautogui.locateCenterOnScreen(imPath('images', 'next.png'))

verifyLoc = pyautogui.locateCenterOnScreen(imPath('images', 'next.png'))

# get the screen size
screenSize = pyautogui.size() 

# convert to strings
strRobotLoc = ','.join(map(str, robotLoc)) 
strRefreshLoc = ','.join(map(str, refreshLoc)) 
strNextLoc = ','.join(map(str, nextLoc)) 
strVerifyLoc = ','.join(map(str, verifyLoc)) 
strScreenSize = ','.join(map(str, screenSize)) 

# save the locations into configure.ini
logging.info("Saving the screenshot parameters and locations into configure.ini...")
config.add_section('locations')
config.set('locations', 'screenSize', strScreenSize)
config.set('locations', 'iamnotrobot', strRobotLoc)
config.set('locations', 'refresh', strRefreshLoc)
config.set('locations', 'next', strNextLoc)
config.set('locations', 'verify', strVerifyLoc)

with open('config.ini', 'w') as f:
    config.write(f)
