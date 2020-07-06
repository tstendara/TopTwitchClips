from selenium import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from helpers.downloadingVideos_helper import gettingLinks
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from helpers.downloadingVideos_helper import downloadingVideo
from pynput.mouse import Button, Controller
import keyboard
import time
import os

class downloadingVideos():
    def __init__(self, game, ranged, links):
        self.clipLinks = [] if links == None else links
        self.mouse = Controller()
        self.driver = ''
        self.game = game # 'Overwatch'
        self.ranged = ranged # '7d'
        self.testing = os.environ['testing'] or None 
 
    def allFunctions(self):
        # If there are no links provided then get top links
        if len(self.clipLinks) == 0: 
            self.initializingDriver(False)
            self.getAllClipLinks()
        elif len(self.clipLinks) == 1:
            # if testing then return error if not, the return error 
            if self.testing:
                return 'Please enter more than one video' 
            else:
                raise SystemExit('Please enter more than one video')

        self.initializingDriver(True)
        self.downloadingClips()

    def initializingDriver(self, headless):
        fireFoxOptions = webdriver.FirefoxOptions()
        fireFoxOptions.set_headless() if headless else None
        driver = webdriver.Firefox(options=fireFoxOptions)
        driver.get(f"https://www.twitch.tv/directory/game/{self.game}/clips?range={self.ranged}") if headless == False else None
        self.driver = driver

    def getAllClipLinks(self):
        driver = self.driver
        mouse = self.mouse
        clipLinks = self.clipLinks
        time.sleep(2)
        assert "Twitch" in driver.title

        # clicking on window, the moving down to load more videos
        mouse.click(Button.left, 1)
        
        for _ in range(5):
            time.sleep(1)
            keyboard.press_and_release('end')

        time.sleep(3)

        allElems = driver.find_elements_by_class_name("tw-hover-accent-effect__children")
        time.sleep(6)

        for curDiv in allElems:
            # getting each Div element containing clips
            values = curDiv.get_attribute('innerHTML').split(" ")
            # getting the href prop within a  
            result = gettingLinks(values[4], 1, self.game)
            # checking to see if approved channel
            if result != False:
                # creating links and appending to array
                clipLinks.append('https://twitch.tv' + result)
        print(f'Clips found: {len(clipLinks)} ')
        driver.quit()

    def downloadingClips(self):
        clipDriver = self.driver
        time.sleep(5)
        for curClip in self.clipLinks:
            time.sleep(1)
            clipDriver.get("https://clipr.xyz/")
            time.sleep(2)

            # Getting search div element
            elem = clipDriver.find_element_by_id("clip_url") # cant find element on page, maybe turn off healess to see what happends
            elem.clear()
            elem.send_keys(curClip)
            elem.send_keys(Keys.RETURN)

            clipDriver.implicitly_wait(2)
            download = clipDriver.find_elements_by_css_selector("div[class='col-md-12']")

            # splitting div with mp4 file
            values = download[1].get_attribute('innerHTML').split(" ")
            videoLink = gettingLinks(values[-11], 2, self.game)
            result = downloadingVideo(videoLink)

            # refreshing page to search again 
            clipDriver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'r')
        clipDriver.quit()

    def close_driver(self):
        self.driver.quit()
