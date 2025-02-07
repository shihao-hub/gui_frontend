import time

import pyautogui

while True:
    point = pyautogui.Point(x=1401, y=56)
    pyautogui.click(point.x, point.y)
    time.sleep(60)
