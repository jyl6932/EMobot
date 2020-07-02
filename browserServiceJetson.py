
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import urllib


class BrowserService(object):

    _CHROME_PATH = '/usr/lib/chromium-browser/chromedriver'
    _YOUTUBE_SEARCH_URL = "https://www.youtube.com/results?search_query={0}"
    _LOAD_TIMEOUT = 5

    def __init__(self, windowPos=(3000, 0, 1080, 960)):
        self._setup(windowPos)

    def _setup(self, windowPos):
        print("Setting up Browser!!")
        options = webdriver.ChromeOptions()
        #options.add_argument('--remote-debugging-port=9515')
        #options.add_argument('--no-sandbox')
        #options.add_argument('--disable-dev-shm-usage')
        options.binary_location = BrowserService._CHROME_PATH
        self._driver = webdriver.Chrome(BrowserService._CHROME_PATH)
        self._driver.set_window_position(windowPos[0], windowPos[1])
        self._driver.set_window_size(windowPos[2], windowPos[3])

    def _wait(self, elementId='element_id'):
        try:
            element_present = EC.presence_of_element_located((By.ID, elementId))
            WebDriverWait(self._driver, self._LOAD_TIMEOUT).until(element_present)
        except TimeoutException:
            print
            "Timed out waiting for page to load"

    def _getURL (self,keyword):
        if keyword == "Sad":
            musicType = "cheerupmusic2020mv"
        elif keyword == "Happy":
            musicType = "2020happymv"
        elif keyword == "Angry":
            musicType = "comfortmusic2020mv"
        else:
            musicType = "koreapopmusic2020mv"
        return musicType


    def searchAndPlay(self, keyword):
        #keywordEncoded = urllib.parse.quote(keyword, safe='')
        musicType = self._getURL(keyword)
        flag = False
        try:
            self._driver.get(self._YOUTUBE_SEARCH_URL.format(musicType))
            self._wait()
            print (musicType)
            startButton = self._driver.find_element_by_id("video-title")
            print (startButton)
            if startButton is not None:
                flag = True
                startButton.click()
                self._wait()
                try:
                    self._driver.find_element_by_css_selector('button.ytp-fullscreen-button.ytp-button').click()
                except Exception as ex:
                    pass
                try:
                    self._wait()
                    self._driver.find_element_by_css_selector('span.ytp-ad-skip-button-icon').click()
                except Exception as ex:
                    self._wait()
                    self._driver.find_element_by_css_selector('span.ytp-ad-skip-button-icon').click()
                except Exception as ex:
                    pass
 
        except Exception as ex:
            pass
        if flag == False:
            print ("Return False")
            return False
        if flag == True:
            print ("Return True")
            return True
    def playNextSong(self):

        try:
            nextButton = self._driver.find_element_by_css_selector('a.ytp-next-button.ytp-button')
            print (startButton)
            if nextButton is not None:
                nextButton.click()
                self._wait()
                try:
                    self._wait()
                    self._driver.find_element_by_css_selector('span.ytp-ad-skip-button-icon').click()
                except Exception as ex:
                    self._wait()
                    self._driver.find_element_by_css_selector('span.ytp-ad-skip-button-icon').click()
                except Exception as ex:
                    pass
        except Exception as ex:
             pass







    def stop(self):
        try:
            self._driver.find_element_by_css_selector('button.ytp-fullscreen-button.ytp-button').click()
            self._wait()
        except Exception as ex:
            pass
        self._driver.get(self._YOUTUBE_SEARCH_URL)

