import os


class Config(object):

    IS_JETSON = True

    if IS_JETSON:
        SCREEN_WIDTH = 2000
        SCREEN_HEIGHT = 1000
        SPRITE_SCALE = 0.8
        PLAYBACK_FPS = 5
        ENABLE_TF = True
        OBJECT_DETECTION = "live"
        SLEEP = 0
        VOICE_FPS = 50
    else:
        SCREEN_WIDTH = 720
        SCREEN_HEIGHT = 540
        SPRITE_SCALE = 0.5
        PLAYBACK_FPS = 20
        ENABLE_TF = False
        OBJECT_DETECTION = "fake"
        SLEEP = 0.03
        VOICE_FPS = 50

    ENABLE_BROWSER = True
    VIDEO_PLAYBACK_TIME = 50
    MAX_FPS = 60


    @classmethod
    def frameScale(cls, frames):
        return frames * Config.PLAYBACK_FPS / Config.MAX_FPS

    @classmethod
    def voiceScale(cls, frames):
        return frames * Config.VOICE_FPS / Config.MAX_FPS

    @classmethod
    def speedScale(cls, speed):
        return min(0.5, speed * Config.MAX_FPS / Config.PLAYBACK_FPS)
