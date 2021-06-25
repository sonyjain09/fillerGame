#https://diderot-production.s3.amazonaws.com/media/courses_public/CMU%3APittsburgh%2C%20PA%3A15112%3ASummer-2%3A2019-20/HOMEWORKS/ch%3Ahw13/chapter_attachments/a781ddc2-d1d2-11ea-94c3-0ab634db4e5d_cmu_112_graphics.py
from cmu_112_graphics import *
import random
import sys  
from twoplayer import *
sys.setrecursionlimit(10000) 

class Player(object):
    def __init__(self, color, cells,app):
        """Initializes parameters that are needed throughout the class in many 
        of the methods to make a functioning Player object"""
        self.color = color
        self.cells = cells
        self.score = 1
        self.app = app
        self.onlyTwo,self.double,self.shuffler = False,False,False
        self.colOptions = ["medium aquamarine", "light coral", "forest green", "chartreuse2", "indianred3", "dark slate gray"]
        self.timerFiredCounter, self.frequency = 0,1000
        self.boomFrequency, self.boomCounter = 1000,0
    
    def updateTimer(self):
        #Code from homework 9
        """Adds 1 to the timer at top of screen every second and controls bomb screen"""
        self.timerFiredCounter += 1
        limit = self.frequency // self.app.timerDelay
        if self.timerFiredCounter % limit == 0:
            self.app.timer += 1
        #makes the bomb screen last for 3 seconds
        if self.app.boomer:
            self.boomCounter += 1
            lim = self.boomFrequency / self.app.timerDelay
            if self.boomCounter % lim == 0:
                self.app.boomer = False

    def evalShuffle(self,other)->None:
        """Shuffles all of the cells on the board besides the ones in the players
        cells"""
        all = [(x,y) for x in range(10) for y in range(10)]
        #list of the coordinates of all cells not in player cells
        remainder = list(set(all) - set(self.cells) - set(other.cells))
        for (r,c) in remainder:
            newCol = chooseColor(self.app.colors, r, c)
            #new color to each cell
            self.app.colors[r][c] = newCol
        shuffler = dict()
        #gives all the powerups new valid cells to be in
        for key,val in self.app.powerups.items():
            if val != "shuffle":
                x = remainder[random.randrange(0,len(remainder))]
                shuffler[x] = val
        self.app.powerups = shuffler
        self.shuffler = False

    def checkGameOver(self,other)->bool:
        """Checks if the game is over"""
        if len(self.cells) + len(other.cells) == 100: return True
        return False

    def drawPowerUpScreens(self,canvas,width:int,height:int)->bool:
        """Draws a bomb on the whole screen if the bomb powerup has been chosen.
        Returns True if drawing was successful"""
        if self.app.boomer:
            canvas.create_rectangle(0,0,width,height,fill="black")
            canvas.create_image(width/2,height/2,image=ImageTk.PhotoImage(self.app.boom))
            return True
        return False

    def updatePowerups(self,other):
        """If any powerups have been used, removes them from the powerup list"""
        updated = dict ()
        for key,val in self.app.powerups.items():
            if key not in self.cells and key not in other.cells: updated[key] = val
        self.app.powerups = updated
    
    def updateOptions(self,other):
        """"Based on both players current colors updates options for next turn"""
        updated = []
        for color in self.colOptions:
            if color != self.color and color != other.color: updated.append(color)
        #if last player got remove power up only two options are presented for 
        #next player
        if self.onlyTwo:
            self.app.options = updated[0:2]
            self.onlyTwo = False
        else: self.app.options = updated
    
    def evalPowerups(self,coordinate:tuple,other)->None:
        """Based on what powerup is over taken by player, sets up action to be
        performed on screen"""
        if self.app.powerups[coordinate]== "skip": self.app.skiparoo = True
        elif self.app.powerups[coordinate] == "remove": self.onlyTwo = True
        elif self.app.powerups[coordinate] == "plus": self.score += 1
        elif self.app.powerups[coordinate] == "shuffle": self.shuffler = True
        elif self.app.powerups[coordinate] == "bomb": self.app.evalBomb(self)
        else: self.double = True

    def updateCells(self,other)->None:
        """Adds any cells that need to be added to a players blob and updates powerups
        as needed"""
        addedCells = 0
        dirs = [(-1,0),(0,-1),(1,0),(0,1)]
        self.color = self.app.chosenColor
        for (row,col) in self.cells:
            for (drow,dcol) in dirs:
                #make sure cell is in bounds
                if 0 <= row+drow < 10 and 0 <= col+dcol < 10:
                    newRow,newCol = row+drow,col+ dcol
                    #don't add a cell that is already in the blob
                    if self.app.colors[newRow][newCol] == self.app.chosenColor and (newRow,newCol) not in self.cells:
                        addedCells += 1
                        if (newRow,newCol) in self.app.powerups:
                            self.evalPowerups((newRow,newCol),other)
                        self.score += 1
                        self.cells.append((newRow,newCol))
        for (x,y) in self.cells:
            self.app.colors[x][y] = self.app.chosenColor
        if self.double: self.score += addedCells
        self.double = False
        self.updatePowerups(other)
        self.updateOptions(other)
        if self.shuffler: self.evalShuffle(other)