import os
import time

from pynput import mouse
import pyautogui
pyautogui.FAILSAFE = False


"""
Due to the network, downloading packages from ARM-MDK will result in a 
network error pop-up window, so you need to use a continuous click.
This software can automatically click on the pop-up window and 
complete the package installation. The software starts running at 
the time of mouse click.
"""


INTERVAL = 5


def on_click(x, y, button, pressed):

    print('Start auto download.')
    
    return False

with mouse.Listener(on_click=on_click) as listener:
    listener.join()


STALL_FIG = os.path.join(os.path.dirname(__file__),'figs/stall_fig.png')

def locate_stall_yes():
    imloc = pyautogui.locateOnScreen(STALL_FIG, confidence=0.6)
    if imloc is None:
        return None
    
    yes_x = imloc.left + 276
    yes_y = imloc.top + 72
    return pyautogui.Point(yes_x, yes_y)

LIC_YES_FIG = os.path.join(os.path.dirname(__file__),'figs/lic_yes_fig.png')
LIC_NEXT_FIG = os.path.join(os.path.dirname(__file__),'figs/lic_next_fig.png')

def locate_lic_yes():
    im1loc = pyautogui.locateOnScreen(LIC_YES_FIG, confidence=0.6)
    if im1loc is None:
        return None
    
    yes_x = im1loc.left + 13
    yes_y = im1loc.top + 8
    yes_pos = pyautogui.Point(yes_x, yes_y)

    im2loc = pyautogui.locateOnScreen(LIC_NEXT_FIG, confidence=0.6)
    if im2loc is None:
        return None

    next_x = im2loc.left + 401
    next_y = im2loc.top + 18
    next_pos = pyautogui.Point(next_x, next_y)

    return yes_pos, next_pos


pyautogui.screenshot()

while True:
    
    orig_pos = pyautogui.position()

    pyautogui.moveTo(0, 0)
    stall_pos = locate_stall_yes()
    if stall_pos is not None:
        print('Find stalled for 10 seconds...')
        pyautogui.click(x=stall_pos.x, y=stall_pos.y, button='left')
        print("click `yes`.")
    
    pyautogui.moveTo(x=orig_pos.x, y=orig_pos.y)

    orig_pos = pyautogui.position()

    pyautogui.moveTo(0, 0)
    lic_pos = locate_lic_yes()
    if lic_pos is not None:
        print('Find license agreement...')
        lic_yes_pos, lic_next_pos = lic_pos
        pyautogui.click(x=lic_yes_pos.x, y=lic_yes_pos.y, button='left')
        print("click `yes` for agreement.")
        time.sleep(0.25)
        pyautogui.click(x=lic_next_pos.x, y=lic_next_pos.y, button='left')
        print("click `next` for closing.")
    
    pyautogui.moveTo(x=orig_pos.x, y=orig_pos.y)

    time.sleep(INTERVAL)
