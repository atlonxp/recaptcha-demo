
# coding: utf-8

# In[ ]:


from configparser import ConfigParser
from ast import literal_eval
import pyautogui
pyautogui.PAUSE = 2.0
pyautogui.FAILSAFE = True

# self-defined
from utilities import imPath, getImage

# FYI
import logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(message)s', datefmt='%H:%M:%S')
#logging.disable(logging.INFO) # uncomment to block debug log messages


# In[2]:


# Read the image parameters
logging.info('Reading the screenshot parameters from configure_initial.ini...')
config = ConfigParser()
config.read('config_initial.ini')

# parameters of screenshots
# working region
strWorkRegion = config.get('images', 'workingRegion')
workRegion = literal_eval(strWorkRegion)
# I am not a robot
strRobotImg = config.get('images', 'iamnotrobot')
robotImg = literal_eval(strRobotImg)
# refresh
strRefreshImg = config.get('images', 'refresh')
refreshImg = literal_eval(strRefreshImg)
# street sign
strStreetImg = config.get('images', 'streetSign')
streetImg = literal_eval(strStreetImg)
# next
strNextImg = config.get('images', 'next')
nextImg = literal_eval(strNextImg)
# verify
strVerifyImg = config.get('images', 'verify')
verifyImg = literal_eval(strVerifyImg)
# image
strImg = config.get('images', 'image')
img = literal_eval(strImg)
# pass
strPassImg = config.get('images', 'pass')
passImg = literal_eval(strPassImg)


# In[3]:


# create the image of work region
logging.info('Creating the screenshot of work region...')
getImage(workRegion, 'images', 'work.png')


# In[4]:


# create the reg image to find the checkbox of "I am not robot"
logging.info('Creating the screenshot of I am not robot...')
getImage(robotImg, 'images', 'reg.png')
# location of checkbox of I am not robot
robotLoc = pyautogui.locateCenterOnScreen(imPath('images', 'reg.png'))


# In[5]:


#click I am not a robot
pyautogui.click(robotLoc)
# create the reg image to find the refresh
logging.info("Creating the screenshot of refresh...")
getImage(refreshImg, 'images', 'refresh.png')
# location of refresh
refreshLoc = pyautogui.locateCenterOnScreen(imPath('images', 'refresh.png'))
# add 20 in Y direction taken into accout the offset introduced by error message
refreshLoc = (refreshLoc[0], refreshLoc[1] + 20)


# In[8]:


# need to manually change it to street sign
pyautogui.alert('Will create addressing image for street sign. Please make sure the street sign is shown')
# create the reg image to street sign
logging.info("Creating the screenshot of title of street sign...")
getImage(streetImg, 'images', 'ifstreet.png')


# In[9]:


# create the screenshot of image of street signs
logging.info("Creating the screenshot of street sign...")
getImage(img, 'images', 'payload.jpg')


# In[10]:


# need to manually assistance to get next button
pyautogui.alert('Please manually select the answers so that next button is shown')
# create the reg image to next
logging.info("Creating the screenshot of next...")
getImage(nextImg, 'images', 'next.png')
# location of next
nextLoc = pyautogui.locateCenterOnScreen(imPath('images', 'next.png'))


# In[12]:


# need to manually assistance to get verify button
pyautogui.alert('Please manually select the answers until the verify button is shown')
# create the reg image to verify
logging.info("Creating the screenshot of verify...")
getImage(verifyImg, 'images', 'verify.png')
# location of verify
verifyLoc = pyautogui.locateCenterOnScreen(imPath('images', 'verify.png'))


# In[13]:


# need to manually assistance to get the check mark
pyautogui.alert('Please make sure to pass the recapcha check')
# create the reg image to pass sign
logging.info("Creating the screenshot of check mark...")
getImage(passImg, 'images', 'pass.png')

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

