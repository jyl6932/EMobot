from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import urllib
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

class BrowserService(object):

    #_CHROME_PATH = '/Users/agustinus.nalwan/Downloads/chromedriver'
    _YOUTUBE_BEST_HOME_URL = "https://www.youtube.com/playlist?list=PLFgquLnL59akp3Cc6cj1S_4fQxPhdetsO"
    _YOUTUBE_CHEERUP_HOME_URL = "https://www.youtube.com/watch?v=fyMhvkC3A84&list=PLpRv-cDtJaf58X6EfaSg3hM4atWUhifDA"
    _YOUTUBE_COMFOR_HOME_URL = "https://www.youtube.com/watch?v=eACohWVwTOc&list=PLbdLE0mIYI0x-btMHirbhUOcSWfrTo416"
    _YOUTUBE_Happy_HOME_URL ="https://www.youtube.com/watch?v=LjhCEhWiKXk&list=PL1VuYyZcPYIJTP3W_x0jq9olXviPQlOe1"
    _LOAD_TIMEOUT = 5


    def __init__(self, windowPos=(200, 0, 1080, 960)):
        self._setup(windowPos)

    def _setup(self, windowPos):
        self._driver = webdriver.Chrome(ChromeDriverManager().install())
        self._driver.set_window_position(windowPos[0], windowPos[1])
        self._driver.set_window_size(windowPos[2], windowPos[3])


    def _wait(self, elementId='element_id'):
        try:
            element_present = EC.presence_of_element_located((By.ID, elementId))
            WebDriverWait(self._driver, self._LOAD_TIMEOUT).until(element_present)
        except TimeoutException:
            print
            "Timed out waiting for page to load"


    def _getURL (self,target):
        if target == "Sad":
            musicType = self._YOUTUBE_CHEERUP_HOME_URL
        elif target == "Happy":
            musicType = self._YOUTUBE_Happy_HOME_URL
        elif target == "Angary":
            musicType = self._YOUTUBE_COMFOR_HOME_URL
        else:
            musicType = self._YOUTUBE_BEST_HOME_URL
        return musicType


    def searchAndPlay(self,target):
        windowPos = (200, 0, 1080, 960)
        musicType = self._getURL(target)
        self._driver.get(musicType)
        self._wait()
        print(target)
        print (musicType == self._YOUTUBE_BEST_HOME_URL)
        if musicType == self._YOUTUBE_BEST_HOME_URL:
            try:
                print("start")
                start = self._driver.find_element_by_css_selector('div#container.playlist-items.yt-scrollbar-dark.style-scope.ytd-playlist-panel-renderer')
                print ("video:",start)
                if start is not None:
                    try:
                        start.click()
                        self._wait()
                        self._driver.find_element_by_css_selector('button.ytp-fullscreen-button.ytp-button').click()

                    except Exception as ex:
                        self._wait()
                        self._driver.find_element_by_css_selector('span.ytp-ad-skip-button-icon').click()
                    except Exception as ex:
                        self._wait()
                        self._driver.find_element_by_css_selector('span.ytp-ad-skip-button-icon').click()
                    except Exception as ex:
                        pass
                    return True

            except Exception as ex:
                pass
            return False

        else:
            try:
                print("start")
                #start = self._driver.find_element_by_css_selector('div#items.playlist-items.yt-scrollbar-dark.style-scope.ytd-playlist-panel-renderer')
                start = self._driver.find_element_by_css_selector('button.ytp-play-button ytp-button ytp-play-button-playlist')
                print ("video:",start)
                if start is not None:
                    try:
                        start.click()
                        self._wait()
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
                    return True
            except Exception as ex:
                pass
            return False



    def stop(self):
        #self._driver.find_element_by_css_selector('button.ytp-fullscreen-button.ytp-button').click()
        self._wait()
        self._driver.get(self._YOUTUBE_BEST_HOME_URL)
