import os
import pyautogui

def imPath(folder, filename):
    """A shortcut for joining the folder file path, since it is used so often. Returns the filename with 'images/' prepended."""
    return os.path.join(folder, filename)

def getImage(region, folder, filename):
    im = pyautogui.screenshot(region=region)
    im.save(imPath(folder, filename))

def clickImage(imageLoc, indices):
    # image location (top-left x, top-left y, x width, y width)
    # top-left corner of screen is (0, 0)
    # indices: list of index 0-15
    # assume 4 x 4
    for i in indices:
        xindex = i % 4
        yindex = int(i / 4)
        x = int(imageLoc[0] + imageLoc[2] / 8 + xindex * imageLoc[2] / 4)
        y = int(imageLoc[1] + imageLoc[3] / 8 + yindex * imageLoc[3] / 4)
        pyautogui.click((x, y))

def rightClickImage(imageLoc):
    # image location (top-left x, top-left y, x width, y width)
    # top-left corner of screen is (0, 0)
    # indices: list of index 0-15
    # assume 4 x 4
    # always right click the 6th one
    xindex = 5 % 4
    yindex = int(5 / 4)
    x = int(imageLoc[0] + imageLoc[2] / 8 + xindex * imageLoc[2] / 4)
    y = int(imageLoc[1] + imageLoc[3] / 8 + yindex * imageLoc[3] / 4)
    pyautogui.PAUSE = 0.5
    pyautogui.rightClick((x, y))
    pyautogui.click((x+50, y+220))

def getIndices(file):
    with open(file) as f:
        content = f.readlines()
    # convert elements to int
    content = [int(x.strip()) for x in content]
    indices = [i for i, e in enumerate(content) if e != 0]
    return indices
