from configparser import ConfigParser
from ast import literal_eval
import pyautogui
pyautogui.PAUSE = 2.0
pyautogui.FAILSAFE = True

# FYI
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(message)s', datefmt='%H:%M:%S')
#logging.disable(logging.INFO) # uncomment to block debug log messages

# self-defined
from utilities import imPath, getImage

# Read the location
logging.info('Reading the configure.ini...')
config = ConfigParser()
config.read('config.ini')

# location of I am not a robot
strRobotLoc = config.get('locations', 'iamnotrobot')
robotLoc = literal_eval(strRobotLoc)
# location of refresh
strRefreshLoc = config.get('locations', 'refresh')
refreshLoc = literal_eval(strRefreshLoc)
# location of next/verify
strNextLoc = config.get('locations', 'next')
nextLoc = literal_eval(strNextLoc)

# screenshot parameters for street signs
strImageLoc = config.get('images', 'image')
imageLoc = literal_eval(strImageLoc)

logging.info('Program Started. Press Ctrl-C to abort at any time.')
logging.info('To interrupt mouse movement, move mouse to upper left corner.')

#click I am not a robot
logging.info("Clicking 'I am not a robot'...")
pyautogui.click(robotLoc)
i = 0
while(i < 100 ):
    # Keep refreshing if it's not street sign
    while(pyautogui.locateCenterOnScreen(imPath('images', 'ifstreet.png')) == None):
        # click the refresh button
        logging.info("Not street sign, refreshing...")
        pyautogui.click(refreshLoc)

    # Take a screenshot of image
    logging.info("Taking screenshot of streen sign...")
    name = 'payload' + str(i) + '.jpg'
    getImage(imageLoc, 'test', name)
    logging.info("Refreshing...")
    pyautogui.click(refreshLoc)
    i = i + 1

logging.info("Succeeded!!")
