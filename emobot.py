import arcade
import time

from config import Config
from robot import Robot
from morphTarget import MorphTarget
from utilities.vector import Vector
from animation import Animation
from speechRecognition import SpeechRecognition
from utilities.fpsCalc import FpsCalc
from datetime import datetime, timedelta




class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, width, height):
        super().__init__(width, height)

        arcade.set_background_color(arcade.color.WHITE)
        self._width = width
        self._height = height
        self._fpsCalc = FpsCalc()

    def setup(self):
        self._speechRecognition = SpeechRecognition()

        self._robot = Robot((self._width, self._height))

        # self._paramVec = Vector(0.0, 0.0)
        # self._targetParamVec = Vector(0.0, 0.0)

        #TODO: Testing the eye target animation using a timer animation. Remove this code when we
        #already replace with vector containing location of face from object detection
        # self._animateParamVectorTo(Vector(0.0, -0.5), 0.05)

    # def _animateParamVectorTo(self, newVector, speed):
    #     self._animation = Animation(newVector, speed)

    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()
        # Your drawing code goes here
        self._robot.spriteList().draw()
        # arcade.glEnable(arcade.GL_TEXTURE_2D)
        # arcade.glTexParameteri(arcade.GL_TEXTURE_2D, arcade.GL_TEXTURE_MIN_FILTER, arcade.GL_NEAREST)
        # arcade.glTexParameteri(arcade.GL_TEXTURE_2D, arcade.GL_TEXTURE_MAG_FILTER, arcade.GL_NEAREST)

    def update(self, delta_time):
        if Config.SLEEP > 0:
            time.sleep(Config.SLEEP)

        """ All the logic to move, and the game logic goes here. """
        # print(delta_time)
        lastFrameCommond = None
        self._robot.update()

def main():

    game = MyGame(Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT)
    game.setup()
    arcade.run()



if __name__ == "__main__":
    main()
