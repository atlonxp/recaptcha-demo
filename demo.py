
from configparser import ConfigParser
from ast import literal_eval
import pyautogui
pyautogui.PAUSE = 2.0
pyautogui.FAILSAFE = True

# FYI
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(message)s', datefmt='%H:%M:%S')
#logging.disable(logging.INFO) # uncomment to block debug log messages

# to run .exe
import subprocess

# to access clipboard in windows
# import win32clipboard
# to access clipboard in linux
import pyperclip as clipboard
# to download image
from urllib import request

# to supress the output of exe file
import os

# control time
import time

# self-defined
from utilities import imPath, clickImage, getIndices, rightClickImage

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

# screenshot parameters for title of street signs
strStreetTitle = config.get('images', 'streetSign')
streetTitle = literal_eval(strStreetTitle)
# screenshot parameters for street signs
strImageLoc = config.get('images', 'image')
imageLoc = literal_eval(strImageLoc)
# screenshot parameters for checkmark sign
strPassImg = config.get('images', 'pass')
passImg = literal_eval(strPassImg)

logging.info('To interrupt mouse movement,')
logging.info('move mouse to upper left corner.')

#click I am not a robot
logging.info("Clicking 'I am not a robot'...")
pyautogui.click(robotLoc)
while(pyautogui.locateOnScreen(imPath('images', 'pass.png'), region = passImg) == None):
    # Keep refreshing if it's not street sign
    while(pyautogui.locateOnScreen(imPath('images', 'ifstreet.png'), region = streetTitle) == None):
        # click the refresh button
        logging.info("Not street sign, refreshing...")
        pyautogui.click(refreshLoc)
    # Download image
    pyautogui.PAUSE = 0.05
    logging.info("Downloading street sign...")
    # copye image url
    rightClickImage(imageLoc)
    pyautogui.press('o')
    # get clipboard data
    # win32clipboard.OpenClipboard()
    url = clipboard.paste()
    # win32clipboard.CloseClipboard()
    # Download image
    request.urlretrieve(url, 'data/payload.jpg')
    # Call yolo to find the street sign
    logging.info("Predicting...")
    # suppress the output
    devnull = open(os.devnull, 'w')
    subprocess.call('./predict.sh', stdout=devnull, stderr=devnull)
    indices = getIndices('predict.txt')
    print(indices)
    time.sleep(3)
    # click the streen signs based on prediciton
    pyautogui.PAUSE = 0.5
    logging.info("Choosing the street sign...")
    clickImage(imageLoc, indices)
    pyautogui.PAUSE = 1.0
    logging.info("Next...")
    pyautogui.click(nextLoc)

logging.info("Solved")
