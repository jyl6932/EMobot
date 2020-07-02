import calendar
import time
import math
import re
import requests
from gtts import gTTS
from gtts_token.gtts_token import Token
import playsound 
import os
import random
import speech_recognition as sr 

class Keyword(object):
    Yes = "yes"
    No = "no"
    Stop = "stop"
    Next = "next"
    Pause = "pause"
    Hello = "hello"
    Happy = "happy"
    Sad = "sad"
    Sad_2 = "sat"
    Sad_3 = "depressed"
    Angry = "angry"
      
class SpeechRecognition(object):

    
    def __init__(self):
        self._recognizer = sr.Recognizer() 
        self._DURATION = 0.5
        self._lastFrameCommond = None

    def _getTxt(self):

        try: 

            # use the microphone as source for input. 
            with sr.Microphone() as source2: 

                # wait for a second to let the recognizer 
                # adjust the energy threshold based on 
                # the surrounding noise level  
                print ("########")
                print ("start recognizaing")
                self._recognizer.adjust_for_ambient_noise(source2, duration=self._DURATION ) 

                #listens for the user's input  
                self._audio2 = self._recognizer.listen(source2) 

                # Using ggogle to recognize audio 
                self._MyText = self._recognizer.recognize_google(self._audio2) 
                self._MyText = self._MyText.lower() 
                print ("text:" ,self._MyText)

            return self._MyText

        except sr.RequestError as e: 
            pass
        except sr.UnknownValueError: 
            pass
        
        return None
    
    def _update(self):
        self._commond = None
        self._MyText = self._getTxt()
        if self._MyText == Keyword.Yes:
                self._commond = "Yes" 
        if self._MyText == Keyword.No:
                self._commond = "No" 
        if self._MyText == Keyword.Stop:
                self._commond = "Stop" 
        if self._MyText == Keyword.Next:
                self._commond = "Next" 
        if self._MyText == Keyword.Hello:
                self._commond = "Hello" 
        if self._MyText == Keyword.Happy:
                self._commond = "Happy" 
        if self._MyText == Keyword.Sad:
                self._commond = "Sad" 
        if self._MyText == Keyword.Sad_2:
                self._commond = "Sad" 
        if self._MyText == Keyword.Sad_3:
                self._commond = "Sad" 
        if self._MyText == Keyword.Angry:
                self._commond = "Angry" 
        print (self._commond)

 

    def getLastFrameCommond(self):
        self._update()
        return self._commond
        

            
