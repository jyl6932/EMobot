from intent import Intent
from utilities.stopwatch import Stopwatch
from config import Config
from speechRecognition import SpeechRecognition
import time

class BrainState(object):
    Idle = "Idle"
    Approch = "Approch"
    Engaging = "Engaging"
    Conversing = "Conversing"
    PlayingVideo = "PlayingVideo"
    FinishPlayingVideo = "FinishPlayingVideo"
    FailedPlayingVideo = "FailedPlayingVideo"



class TargetName(object):
    Other = "Stranger"
    Yiling = "Yiling"
    Katherine = "Katherine"

class CurrentCommand(object):
    Yes = "Yes"
    No = "No"
    Stop = "Stop"
    Happy = "Happy"
    Sad = "Sad"
    Angry = "Angry"


class BrainStateMachine(object):
    # We don't want to scale the focus_eye_speed excesively so keep it at 0.2
    _DELAY_BEFORE_ASKING_REPEAT_QUESTION = Config.voiceScale(100)  # Ask to bring an object after x second not seeing any
    _DISSENGAGED_PATIENCE = Config.voiceScale(1000)  # If no target for 1000 iterations then totally disengaged

    def __init__(self):
        self._state = BrainState.Idle
        self._currentStateTime = None
        self._currentTarget = None
        self._emotionLabel = None
        self._timeToDissengaged = 0
        self._timeEngaged = 0
        self._currentCommand = None
        self._TEMPFLAG = False
        self._isSetupReady = False
        self._startCtr = 0
        self._listenUserSpeaking = False
        self._speechFrame = 0
        self._speechVideoFrame = 0
        self._speechDuringVideo = False
        self._voiceFrame = 0
        self._lastFrameCommond = None



        self._speechRecognition = SpeechRecognition()





    def _updateBrainState(self,lastFrameCommond):

        # Don't change our state if we are currently talking
        newState = self._state

        # If have target, set state to engaging
        print ("@@@@")
        print (newState)
        print ("currentTarget:",self._currentTarget)
        if self._currentTarget is not None:
            # If we were engaging and already asked the person to come then we jump into conversing
            # State is engaging
            if self._state == BrainState.Engaging:
                print ("Commond:",lastFrameCommond)
                if  (lastFrameCommond == CurrentCommand.Happy) |(lastFrameCommond == CurrentCommand.Sad) |(lastFrameCommond == CurrentCommand.Angry):
                    self._timeEngaged += 1
                    self._emotionLabel = lastFrameCommond
                    newState = BrainState.Conversing
                    self.emotion_label = lastFrameCommond
                    self._intent.GreetingUser(self.emotion_label)
                    time.sleep(4)
                    self._intent.askToPlayVideo()
                    time.sleep(3)
                    self._listenUserSpeaking = True
                    newState= BrainState.Conversing
                    

            # State is Approch ( dont care first )
            elif self._state == BrainState.Approch:
                self._timeEngaged = 0
                newState = BrainState.Engaging
                self._intent.askUserMood()
                time.sleep(3)
                self._listenUserSpeaking = True


            # State is Idle ( dont care first )
            elif self._state == BrainState.Idle:
                newState = BrainState.Approch

            elif self._state == BrainState.Conversing:
                if  lastFrameCommond == None:
                    if self._currentStateTime is not None and self._currentStateTime.get() / 1000 >= self._DELAY_BEFORE_ASKING_REPEAT_QUESTION:
     
                        print ("sp")
                        self._intent.askToPlayVideo()
                        self._listenUserSpeaking = True
                elif lastFrameCommond == CurrentCommand.Yes:
                    self._intent.readyToPlayVideo()
                    self._intent.playVideo(self._emotionLabel)
                    self._emotionLabel = None
                    if not self._intent.isPlayingVideo():
                        print ("Faliue paly music")
                        self._state = BrainState.FailedPlayingVideo
                        self._listenUserSpeaking = False


                    else:
                        newState = BrainState.PlayingVideo
                        self._listenUserSpeaking = True

                if lastFrameCommond == CurrentCommand.No:
                    self._intent.sayGoodby()
                    newState = BrainState.Idle
                    self._listenUserSpeaking = True
                    self._currentTarget = None

 

            elif self._state == BrainState.FailedPlayingVideo:
                print ("resart playing music")
                if not self._intent.playVideo():
                    self._state = BrainState.FailedPlayingVideo
                    self._listenUserSpeaking = False
                else:
                    newState = BrainState.PlayingVideo
                    self._listenUserSpeaking = True


            elif self._state == BrainState.PlayingVideo:
                print ("is palying video")
                self._speechDuringVideo = True

                if str(lastFrameCommond) == CurrentCommand.Stop:
                    print ("ready to stop")
                    self._intent.stopVideo()
                    newState = BrainState.Conversing
                    self._intent.askToPlayMoreVideo()
                    self._listenUserSpeaking = True
                else:
                    pass


                #if self._currentCommand == "Next":
                    #print ("Move to next song")
                    #self._intent.playNextSong()




        else:
            if self._state == BrainState.Idle and self._currentTarget is None:
                self._listenUserSpeaking = True
            self._timeToDissengaged = self._DISSENGAGED_PATIENCE
            # Slowly getting more and more disengaged if no target
            self._timeToDissengaged -= 1

            if self._timeToDissengaged <= 0:
                # Run out of patience, not having a target for a very long time, change to idle state
                newState = BrainState.Idle

        if self._state != BrainState.Idle and self._currentTarget is not None:
            self._timeToDissengaged = self._DISSENGAGED_PATIENCE

        self._setState(newState)

    # how long one state last
    def _setState(self, newState):
        if newState != self._state:
            self._currentStateTime = Stopwatch()

        self._state = newState


    def update(self):
        if self._isSetupReady:
            self._lastFrameCommond = None
            print("Setup ready!")
            if self._listenUserSpeaking == True:
                self._voiceFrame +=  1
                if self._voiceFrame == 20:
                    self._lastFrameCommond = self._speechRecognition.getLastFrameCommond()
                    self._voiceFrame = 0
            self._updatePersonEngae(self._lastFrameCommond)
            self._updateBrainState(self._lastFrameCommond)
        else:
            self._startCtr += 1
            maxScale = Config.frameScale(100)
            print("StartCtr {0} aiming {1}".format(self._startCtr, maxScale))
            if self._startCtr > maxScale:
                self._intent = Intent()
                self._isSetupReady = True

    def _updatePersonEngae(self, lastFrameCaptured):
        # Find greeting voice in last commond
        if self._currentTarget is None and lastFrameCaptured == "Hello":
            self._currentTarget = True
            print ("create a now target")


    def getState(self):
        return self.state
