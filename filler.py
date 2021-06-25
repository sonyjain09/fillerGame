#https://diderot-production.s3.amazonaws.com/media/courses_public/CMU%3APittsburgh%2C%20PA%3A15112%3ASummer-2%3A2019-20/HOMEWORKS/ch%3Ahw13/chapter_attachments/a781ddc2-d1d2-11ea-94c3-0ab634db4e5d_cmu_112_graphics.py
from cmu_112_graphics import *

import random
import sys  
from helper import *
from twoplayer import*
from gameover import *
from hard import*
from gameover2 import*
from easy import*
from gameover3 import*
sys.setrecursionlimit(10000) 
#game inspiration from apple game pigeon
#http://gamepigeonapp.com/
class FillerGame(ModalApp):
    def appStarted(self):
        self.addMode(TwoPlayer(name="play"))
        self.addMode(GameOver(name="gameover"))
        self.addMode(GameOver2(name="gameover2"))
        self.addMode(GameOver3(name="gameover3"))
        self.addMode(HelpMode(name="help"))
        self.addMode(EasyMode(name="easy"))
        self.addMode(HardMode(name="hard"))
        self.setActiveMode("help")

def testAll():
    FillerGame()

if __name__ == "__main__":
    testAll()