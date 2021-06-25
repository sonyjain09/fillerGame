from cmu_112_graphics import *
from filler import *
from hard import*
from helper import*
import random
import sys 

class GameOver2(Mode):
    def appStarted(self):
        mode = self.getMode("hard") 
        mode2 = self.getMode("help")
        self.playerScore = mode.player.score
        self.meScore = mode.me.score
        #update file if player beat computer
        if self.playerScore > self.meScore:
            self.winner = "YOU"
            self.winnerScore = self.playerScore
            reader = open("users.txt", "rt")
            lines = reader.readlines()
            reader.close()
            writer = open("users.txt", "wt")
            for line in lines:
                x = line.split(" ")
                #only check the line of the current user
                if x[0] != mode2.username:
                    writer.write(line)
                else:
                    if "\n" in x[1]:
                        x[1] = x[1][:-1]
                    if mode.timer < float(x[1]):
                        writer.write(mode2.username + " " + str(mode.timer) + "\n")
                    else:
                        #if they didn't beat their time keep the line the same
                        writer.write(line)

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