from cmu_112_graphics import *
from filler import *
from twoplayer import*
import random
import sys  

class GameOver(Mode):
    def appStarted(self):
        mode = self.getMode("play") 
        self.player1Score = mode.player1.score
        self.player2Score = mode.player2.score
        if self.player1Score > self.player2Score:
            self.winner = "PLAYER 1"
            self.winnerScore = self.player1Score
        elif self.player1Score < self.player2Score:
            self.winner = "PLAYER 2"
            self.winnerScore = self.player2Score
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
        else: canvas.create_text(self.width/2,self.height/2,text=f"{self.winner} is the winner with a score of {self.winnerScore}!",font=f"Helvetica {self.width//30}  bold")
        canvas.create_text(self.width/2,self.height-self.height/3,text="Press R to play again!",font=f"Helvetica {self.width//30}  bold")