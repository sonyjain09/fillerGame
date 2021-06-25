from cmu_112_graphics import *
from filler import *
from easy import*
import random
import sys 

class GameOver3(Mode):
    def appStarted(self):
        mode = self.getMode("easy") 
        self.playerScore = mode.player.score
        self.meScore = mode.me.score
        if self.playerScore > self.meScore:
            self.winner = "YOU"
            self.winnerScore = self.playerScore
        elif self.playerScore < self.meScore:
            self.winner = "MACHINE"
            self.winnerScore = self.meScore
        else: self.winner = "DRAW"
        self.colOptions = ["medium aquamarine", "light coral", "forest green", "chartreuse2", "indianred3", "dark slate gray"]

    def drawRotatingScreen(self,canvas):
        x0,y0 = 0,0
        x1,y1 = self.width,self.height
        interval = self.width/12
        random.shuffle(self.colOptions)
        for i in range(len(self.colOptions)):
            canvas.create_rectangle(x0,y0,x1,y1, fill=self.colOptions[i],outline="")
            x0 += interval
            y0 += interval
            x1 -= interval
            y1 -= interval
    
    def modeActivated(self):
        self.appStarted()

    def keyPressed(self,event):
        if event.key == "r":
            self.setActiveMode("help")

    def redrawAll(self,canvas):
        self.drawRotatingScreen(canvas)
        if self.winner == "DRAW": canvas.create_text(self.width/2,self.height/2,text="DRAW!",font=f"Helvetica {self.width//30}  bold")
        elif self.winner == "YOU": canvas.create_text(self.width/2,self.height/2,text=f"You won with a score of {self.winnerScore}!",font=f"Helvetica {self.width//30}  bold")
        else: canvas.create_text(self.width/2,self.height/2,text=f"You lost!",font=f"Helvetica {self.width//30}  bold")
        canvas.create_text(self.width/2,self.height-self.height/3,text="Press R to play again!",font=f"Helvetica {self.width//30}  bold")