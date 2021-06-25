#https://diderot-production.s3.amazonaws.com/media/courses_public/CMU%3APittsburgh%2C%20PA%3A15112%3ASummer-2%3A2019-20/HOMEWORKS/ch%3Ahw13/chapter_attachments/a781ddc2-d1d2-11ea-94c3-0ab634db4e5d_cmu_112_graphics.py#
from cmu_112_graphics import *
import random
import sys  
from creatingBoard import *
from player import *
class EasyMode(Mode):
    def appStarted(self):
        self.colors,self.powerups = fillColors(),choosePowerUpCells()
        self.margin = 50
        self.player = Player(self.colors[9][0],[(9,0)],self)
        self.me = Player(self.colors[0][9],[(0,9)],self)
        self.options = copy.copy(self.player.colOptions)
        self.options.remove(self.player.color)
        self.options.remove(self.me.color)
        self.cellWidth = (self.width-(2*self.margin))//10
        self.turn = "player"
        self.timer = 0
        self.chosenColor = ""
        self.skiparoo,self.boomer = False,False
        #https://www.google.com/search?q=bomb+clipart&sxsrf=ALeKk018y2W6c23Sjlu-Byn5Ub77yVtl-A:1596494848673&source=lnms&tbm=isch&sa=X&ved=2ahUKEwiL0NzijoDrAhWPPM0KHR34AqAQ_AUoAXoECAsQAw&biw=1440&bih=789#imgrc=1m_FQGyYeBgGrM
        self.boom = self.loadImage("boom.png")

    def timerFired(self):
        self.player.updateTimer()

    def modeActivated(self):
        self.appStarted()
    
    def mousePressed(self,event):
        cellWidth = (self.width-(2*self.margin))//10
        start,cy,r = self.margin + (2*cellWidth),self.height-(self.margin/2),self.margin/3
        clicked = False
        if self.turn == "player":
            for i in range(len(self.options)):
                if start-r < event.x < start+r and cy-r < event.y < cy+r:
                    self.chosenColor = self.options[i]
                    clicked = True
                start = start + (cellWidth*2)
            if clicked: 
                self.changeCellColors()
                self.compTurn()

    def keyPressed(self,event):
        if self.turn == "player":
            if event.key == "1": self.chosenColor = self.options[0]
            elif event.key == "2": self.chosenColor = self.options[1]
            elif event.key == "3" and len(self.options) == 4: self.chosenColor = self.options[2]
            elif event.key == "4" and len(self.options) == 4: self.chosenColor = self.options[3]
            elif event.key == "q": self.setActiveMode("help")
            else: return
        self.changeCellColors()
        self.compTurn()
    
    def evalCompSkip(self):
        if self.skiparoo == True and self.turn == "me":
            self.skiparoo = False
            self.compTurn()
    
    def compTurn(self):
        if self.turn == "me":
            dirs = [(-1,0),(0,-1),(1,0),(0,1)]
            mostCells = 0
            option = self.options[0]
            for color in self.options:
                currentCells = 0
                for (row,col) in self.me.cells:
                    for (drow,dcol) in dirs:
                        if 0 <= row+drow < 10 and 0 <= col+dcol < 10:
                            newRow,newCol = row+drow,col+ dcol
                            if self.colors[newRow][newCol] == color and (newRow,newCol) not in self.me.cells:
                                currentCells += 1
                if currentCells > mostCells:
                    mostCells = currentCells
                    option = color
            self.chosenColor = option
            self.changeCellColors()
        else:
            return

    def evalBomb(self,player)->None:
        """Removes 5 cells from the opposite players blob and reduces their score 
        by 5 (or to 0)"""
        #determine player that is getting cells removed
        if player == self.player: victim = self.me
        else: victim = self.player
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
        if self.turn == "player":
            self.player.updateCells(self.me)
            if self.skiparoo:
                self.turn = "player"
                self.skiparoo = False
            else: 
                self.turn = "me"
        elif self.turn == "me":
            self.me.updateCells(self.player)
            if self.skiparoo:
                self.turn = "me"
                self.evalCompSkip()
            else: self.turn = "player"
        if self.player.checkGameOver(self.me): self.setActiveMode("gameover3")

    def redrawAll(self,canvas):
        if self.player.drawPowerUpScreens(canvas,self.width,self.height):
            pass
        else:
            drawFillerBoard(canvas,self.width,self.height,self.colors,self.powerups,self.options)
            heightChange = (self.height-100)/7
            word,word2 = "PLAYER1","MACHINE"
            if self.turn == "player": playerColor,meColor = "yellow","white"
            else: meColor,playerColor= "yellow","white"
            canvas.create_text(25,25,text = self.player.score,fill=self.player.color)   
            canvas.create_text(self.width-25,25,text = self.me.score,fill=self.me.color)   
            for i in range(7):
                canvas.create_text(25,(heightChange*i)+(1.25*self.margin),text= word[i],fill=playerColor)
            for i in range(7):
                canvas.create_text(self.width-25,(heightChange*i)+(1.25*self.margin),text= word2[i],fill=meColor)
            canvas.create_text(self.width/2,25,text=f"{self.timer} seconds", fill="white")
        if self.turn == "player":
            drawOptions(canvas,self.width,self.height,self.options)