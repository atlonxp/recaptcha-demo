
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
import win32clipboard
# to download image
from urllib import request

# to supress the output of exe file
import os

# timing
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
# screenshot parameters for verify
strVerifyImg = config.get('images', 'verify')
verifyImg = literal_eval(strVerifyImg)

logging.info('Program Started. Press Ctrl-C to abort at any time.')
logging.info('To interrupt mouse movement, move mouse to upper left corner.')

problems = 0
streetSigns = 0
solves = 0
attempts = 0

startTime = time.time()
while True:
    #click I am not a robot
    logging.info("Clicking 'I am not a robot'...")
    pyautogui.click(robotLoc)
    while(pyautogui.locateOnScreen(imPath('images', 'pass.png'), region = passImg) == None):
        # Keep refreshing if it's not street sign
        while(pyautogui.locateOnScreen(imPath('images', 'ifstreet.png'), region = streetTitle) == None):
            # click the refresh button
            logging.info("Not street sign, refreshing...")
            problems = problems + 1
            pyautogui.click(refreshLoc)
        # Download image
        pyautogui.PAUSE = 0.05
        logging.info("Downloading street sign...")
        # copye image url
        rightClickImage(imageLoc)
        pyautogui.press('o')
        # get clipboard data
        win32clipboard.OpenClipboard()
        url = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        # Download image
        request.urlretrieve(url, 'data/payload.jpg')
        # Call yolo to find the street sign
        logging.info("Predicting...")
        attempts = attempts + 1
        # suppress the output
        devnull = open(os.devnull, 'w')
        subprocess.call('yolo-street-sign.exe', stdout=devnull, stderr=devnull)
        indices = getIndices('predict.txt')
        print(indices)
        # click the street signs based on prediciton
        pyautogui.PAUSE = 0.5
        logging.info("Choosing the street sign...")
        clickImage(imageLoc, indices)
        pyautogui.PAUSE = 2.0
        # count how many problems
        if (pyautogui.locateOnScreen(imPath('images', 'verify.png'), region = verifyImg) != None):
            problems = problems + 1
            streetSigns = streetSigns + 1

        logging.info("Next...")
        pyautogui.click(nextLoc)

    solves = solves + 1
    msg = "Problems: %d Street Signs: %d Solved: %d Prediction: %d in %s seconds" % (problems, streetSigns, solves, attempts, round(time.time() - startTime))
    logging.info(msg)

    # restart. move cursor to the reCAPTCHA and hit refresh F5
    pyautogui.click(robotLoc)
    pyautogui.press('f5')
