#https://diderot-production.s3.amazonaws.com/media/courses_public/CMU%3APittsburgh%2C%20PA%3A15112%3ASummer-2%3A2019-20/HOMEWORKS/ch%3Ahw13/chapter_attachments/a781ddc2-d1d2-11ea-94c3-0ab634db4e5d_cmu_112_graphics.py#
from cmu_112_graphics import *
import random
import sys  
from creatingBoard import *
from player import *
class TwoPlayer(Mode):
    def appStarted(self):
        self.colors,self.powerups = fillColors(),choosePowerUpCells()
        self.margin = 50
        self.player1 = Player(self.colors[9][0],[(9,0)],self)
        self.player2 = Player(self.colors[0][9],[(0,9)],self)
        self.options = copy.copy(self.player1.colOptions)
        self.options.remove(self.player1.color)
        self.options.remove(self.player2.color)
        self.cellWidth = (self.width-(2*self.margin))//10
        self.turn = "Player1"
        self.timer = 0
        self.chosenColor = ""
        self.skiparoo,self.boomer = False,False
        #https://www.google.com/search?q=bomb+clipart&sxsrf=ALeKk018y2W6c23Sjlu-Byn5Ub77yVtl-A:1596494848673&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiL0NzijoDrAhWPPM0KHR34AqAQ_AUoAXoECAsQAw&biw=1440&bih=789#imgrc=1m_FQGyYeBgGrM
        self.boom = self.loadImage("boom.png")

    def timerFired(self):
        self.player1.updateTimer()

    def modeActivated(self):
        self.appStarted()
    
    def mousePressed(self,event):
        cellWidth = (self.width-(2*self.margin))//10
        start,cy,r = self.margin + (2*cellWidth),self.height-(self.margin/2),self.margin/3
        clicked = False
        for i in range(len(self.options)):
            if start-r < event.x < start+r and cy-r < event.y < cy+r:
                self.chosenColor = self.options[i]
                clicked = True
            start = start + (cellWidth*2)
        if clicked: self.changeCellColors()

    def keyPressed(self,event):
        if event.key == "1": self.chosenColor = self.options[0]
        elif event.key == "2": self.chosenColor = self.options[1]
        elif event.key == "3" and len(self.options) == 4: self.chosenColor = self.options[2]
        elif event.key == "4" and len(self.options) == 4: self.chosenColor = self.options[3]
        elif event.key == "q": self.setActiveMode("help")
        else: return
        self.changeCellColors()

    def evalBomb(self,player)->None:
        """Removes 5 cells from the opposite players blob and reduces their score 
        by 5 (or to 0)"""
        #determine player that is getting cells removed
        if player == self.player1: victim = self.player2
        else: victim = self.player1
        newList = []
        for i in range(5):
            #user has to be left with at least one cell to keep game goign
            if len(victim.cells) != 1:
                x = victim.cells.pop()
                newList.append(x)
                self.colors[x[0]][x[1]] = None
        #adds removed cells back to board with new valid colors
        for (row,col) in newList:
            self.colors[row][col] = chooseColor(self.colors,row,col)
        victim.score -= 5
        #victim's score has to be at least 1 because they'll always be left
        #with at least one square
        if victim.score < 1:
            victim.score = 1
        self.boomer = True

    def changeCellColors(self)->None:
        """Performs calls to change player self colors and evaluates powerups"""
        if self.turn == "Player1":
            self.player1.updateCells(self.player2)
            if self.skiparoo:
                self.turn = "Player1"
                self.skiparoo = False
            else: self.turn = "Player2"
        elif self.turn == "Player2":
            self.player2.updateCells(self.player1)
            if self.skiparoo:
                self.turn = "Player2"
                self.skiparoo = False
            else: self.turn = "Player1"
        if self.player1.checkGameOver(self.player2): self.setActiveMode("gameover")

    def redrawAll(self,canvas):
        if self.player1.drawPowerUpScreens(canvas,self.width,self.height):
            pass
        else:
            drawFillerBoard(canvas,self.width,self.height,self.colors,self.powerups,self.options)
            drawOptions(canvas,self.width,self.height,self.options)
            heightChange = (self.height-100)/7
            word,word2 = "PLAYER1","PLAYER2"
            if self.turn == "Player1": player1Color,player2Color = "yellow","white"
            else: player2Color,player1Color= "yellow","white"
            canvas.create_text(25,25,text = self.player1.score,fill=self.player1.color)   
            canvas.create_text(self.width-25,25,text = self.player2.score,fill=self.player2.color)   
            for i in range(7):
                canvas.create_text(25,(heightChange*i)+(1.25*self.margin),text= word[i],fill=player1Color)
            for i in range(7):
                canvas.create_text(self.width-25,(heightChange*i)+(1.25*self.margin),text= word2[i],fill=player2Color)
            canvas.create_text(self.width/2,25,text=f"{self.timer} seconds", fill="white")