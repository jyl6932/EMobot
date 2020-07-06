import os
import time
'''
voice control part for differenct situation
'''
from speech import Speech
from config import Config
from faceRecognition import GetLastFrameInf


if Config.IS_JETSON:
    from browserServiceJetson import BrowserService
else:
    from browserServiceMac import BrowserService

from utilities.stopwatch import Stopwatch


class Intent(object):

    def __init__(self):
        self._speech = Speech("audio/")
        self._startPlayingVideoTime = None
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

    def askToComeAndPlay(self):
        self._speech.speak("It's a long day. Do you want to chill up?")

    def GreetingUser(self):
        face_label, emotion_label = GetLastFrameInf()
        self._speech.speak("Hello {0}! You look {1}".format(face_label,emotion_label))

    def askToPlayVideo(self):
        self._speech.speak("Do you want to play some music?")

    def readyToPlayVideo(self):
        self._speech.speak("Well, I am so glad to join you!Hang on a second. Let me play a music for you!")

    def sayGoodby(self):
        face_label, emotion_label = GetLastFrameInf()
        self._speech.speak("Okay {0}! I spent a great time with you! Bye-bye!".format(face_label))

    def askToPlayMoreVideo(self):
        self._speech.speak("It's a great music right? Do you want to play more?")


    def playVideo(self):
        ret = True
        face_label, emotion_label = GetLastFrameInf()
        if Config.ENABLE_BROWSER:
            ret = self._browserService.searchAndPlay(emotion_label)
            print ("**********")
            print (ret)

        if ret:
            self._startPlayingVideoTime = Stopwatch()

        return ret

    def playNextSong(self):
        self._browserService.playNextSong()

    def isPlayingVideo(self):
        if self._startPlayingVideoTime is None:
            return False

        elapsedSec = self._startPlayingVideoTime.get() / 1000

        return elapsedSec < Config.VIDEO_PLAYBACK_TIME

    def stopVideo(self):
        if Config.ENABLE_BROWSER:
            self._browserService.stop()
