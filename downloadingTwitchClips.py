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
import keyboard
import time
import os

class downloadingVideos():
    def __init__(self, game, ranged, links):
        self.clipLinks = [] if links == None else links
        self.driver = {}
        self.game = game # 'Overwatch'
        self.ranged = ranged # '7d'
        self.testing = True if 'testing' in os.environ else False
 
    def allFunctions(self):
        # If there are no links provided then get top links
        if len(self.clipLinks) == 0: 
            self.initializingDriver()
            self.getAllClipLinks()
        elif len(self.clipLinks) == 1:
            # if testing then return error if not, the return error 
            if self.testing:
                return 'Please enter more than one video' 
            else:
                raise SystemExit('Please enter more than one video')
        
        self.initializingDriver()
        self.downloadingClips()

    def initializingDriver(self):
        fireFoxOptions = webdriver.FirefoxOptions()
        fireFoxOptions.headless = True 
        driver = webdriver.Firefox(options=fireFoxOptions)
        driver.get(f"https://www.twitch.tv/directory/game/{self.game}/clips?range={self.ranged}") 
        self.driver = driver

    def getAllClipLinks(self):
        driver = self.driver
        clipLinks = self.clipLinks
        time.sleep(2)
        assert "Twitch" in driver.title
        driver.find_element_by_xpath('/html/body/div[1]/div/div[2]/div/main/div[1]/div[3]/div/div/div/div[1]/div[2]/div/div[2]/div[3]').click()
        page = driver.find_element_by_tag_name('body')
       
        for _ in range(10):
            page.send_keys(Keys.PAGE_DOWN)
            time.sleep(2)

        time.sleep(2)
        allElems = driver.find_elements_by_class_name("tw-hover-accent-effect__children")
        time.sleep(10)

        for curDiv in allElems:
            if len(clipLinks) == 30:
                break
            # getting each Div element containing clips
            values = curDiv.get_attribute('innerHTML').split(" ") 
            result = gettingLinks(values[4], 1, self.game)
            # checking to see if approved channel
            if result != False:
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
            elem = clipDriver.find_element_by_id("clip_url") 
            elem.clear()
            elem.send_keys(curClip)
            elem.send_keys(Keys.RETURN)

            clipDriver.implicitly_wait(2)
            download = clipDriver.find_elements_by_css_selector("div[class='col-md-12']")

            # splitting div to get mp4 link
            values = download[1].get_attribute('innerHTML').split(" ")
            videoLink = gettingLinks(values[-11], 2, self.game)
            result = downloadingVideo(videoLink)

            # refreshing page
            clipDriver.find_element_by_tag_name('body').send_keys(Keys.COMMAND + 'r')
        clipDriver.quit()

    def close_driver(self):
        self.driver.quit()