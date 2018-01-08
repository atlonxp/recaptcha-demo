
# coding: utf-8

# In[1]:


import pyautogui
pyautogui.PAUSE = 2.5
pyautogui.FAILSAFE = True


# In[ ]:


pyautogui.alert(text='Ready to rock the reCAPTCHA?', title='Ready?', button='OK')


# In[ ]:


moveToX = 500
moveToY = 500
pyautogui.rightClick(x=moveToX, y=moveToY)


# In[2]:


im = pyautogui.screenshot(region=(115, 12, 50, 50))
im.save('test.jpg')


# In[3]:


loc = pyautogui.locateOnScreen('test.jpg')


# In[4]:


print(loc)

