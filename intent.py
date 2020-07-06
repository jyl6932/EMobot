import os
import time
'''
voice control part for differenct situation
'''
from speech import Speech
from config import Config
from messageBox import MessageBox

if Config.IS_JETSON:
    from browserServiceJetson import BrowserService
else:
    from browserServiceMac import BrowserService

from utilities.stopwatch import Stopwatch


class Intent(object):

    def __init__(self):
        self._messageDuration = Config.MESSAGE_DURATION
        self._speech = Speech("audio/")
        self._startPlayingVideoTime = None
        self._messageBox = MessageBox()
        if Config.ENABLE_BROWSER:
            print("Initing browser intent")
            self._browserService = BrowserService()

    def isBusy(self):
        #TODO: Add a bit of delay to keep busy status 2 seconds after talking
        return self.isTalking() or self.isAfterTalking() or self.isPlayingVideo()

    def isTalking(self):
        return self._speech.isSpeaking()

    def isAfterTalking(self):
        return self._speech.isAfterSpeaking()

    #voice part

    def askToPlayVideoOrMessage(self):
        self._speech.speak("Do you want me to play some music for you or open the messagebox? say music or message")

    def GreetingUser(self,emotion_label):
        if emotion_label == "Happy":
            self._speech.speak("It's a beautiful day to be grateful and happy, keep on rocking!")
        if emotion_label == "Sad":
            self._speech.speak("You seem sad! would you like a hug?")
        if emotion_label == "Angry":
            self._speech.speak("Uh oh, you seem angry! I have kids, please don't hurt me")

    def askUserMood(self):
        self._speech.speak("It's a long day right? How are you feeling today")

    def readyToPlayVideo(self):
        self._speech.speak("Well, I am so glad to join you!Hang on a second. Let me play some music for you!")

    def sayGoodby(self):
        self._speech.speak("Okay! I spent a great time with you! Bye-bye!")

    def askToPlayMoreVideo(self):
        self._speech.speak("It's a great music right? Do you want to play more?")
    def askToPlayOrRecordMessage(self):
        self._speech.speak("Welcome to messagebox! Do you want to listen to previous message or record a new one? say play or record")
    def askToPlayMessageBox(self):
        self._speech.speak("Then do you want to switch to messagebox?")
    def ReadyToRecordMessage(self):
        self._speech.speak("Ok, you have 15 seconds to record your current mood.")
    def ReadyToPlayMessage(self):
        self._speech.speak("This is the message from past you")
    def askToPlayMusic(self):
        self._speech.speak("Then, would you like to listen to music with me?")

    def finishRecord(self):
        self._speech.speak("Ok,finish record")



    def playVideo(self,emotion_label):
        ret = True
        if Config.ENABLE_BROWSER:
            ret = self._browserService.searchAndPlay(emotion_label)
            print ("**********")
            print (ret)

        if ret:
            self._startPlayingVideoTime = Stopwatch()

        return ret

    def playNextSong(self):
        self._browserService.playNextSong()

    def recordMessage(self):
        self._messageBox.recordMessage()
        time.sleep(self._messageDuration)

    def playMessage(self):
        self._messageBox.playMessage()
        time.sleep(self._messageDuration)

    def isPlayingVideo(self):
        if self._startPlayingVideoTime is None:
            return False

        elapsedSec = self._startPlayingVideoTime.get() / 1000

        return elapsedSec < Config.VIDEO_PLAYBACK_TIME

    def stopVideo(self):
        if Config.ENABLE_BROWSER:
            self._browserService.stop()
