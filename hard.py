#https://diderot-production.s3.amazonaws.com/media/courses_public/CMU%3APittsburgh%2C%20PA%3A15112%3ASummer-2%3A2019-20/HOMEWORKS/ch%3Ahw13/chapter_attachments/a781ddc2-d1d2-11ea-94c3-0ab634db4e5d_cmu_112_graphics.py#
from cmu_112_graphics import *
import random
import sys  
import time
from creatingBoard import *
from player import *
class HardMode(Mode):
    def appStarted(self):
        self.colors,self.powerups = fillColors(),self.choosePowerUpCells()
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

    def keyPressed(self,event):
        if self.turn == "player":
            if event.key == "1": self.chosenColor = self.options[0]
            elif event.key == "2": self.chosenColor = self.options[1]
            elif event.key == "3" and len(self.options) == 4: self.chosenColor = self.options[2]
            elif event.key == "4" and len(self.options) == 4: self.chosenColor = self.options[3]
            elif event.key == "q": self.setActiveMode("help")
            else: return
        self.changeCellColors()
    
    def choosePowerUpCells(self)->None:
        """Creates a dictionary that has 6 tuple x,y coordinates as keys and a 
        powerup as the value to represent wehre powerups should go on the filler board 
        drawing"""
        result = dict()
        #only included middle rows and columns so powerups hopefully aren't too close to
        #either players side
        rows,cols = [2,3,4,5,6,7],[2,3,4,5,6,7]
        powerups = ["skip","remove","plus","timesTwo","shuffle","bomb"]
        i = 0
        while i < 6:
            row,col = random.choice(rows),random.choice(cols)
            #don't include starting cells for either player
            if (row,col) not in result:
                result[(row,col)] = powerups[i]
                i += 1
                #remove the row and col added so the powerups are more spread out
                rows.remove(row)
                cols.remove(col)
        return result

    def evalCompSkip(self):
        """When the computer gets the skip powerup gives it another turn"""
        if self.skiparoo == True and self.turn == "me":
            self.skiparoo = False
            self.compTurn()
    
    def compTurn(self):
        """Chooses a color for the computer to play on their next turn"""
        thullu = gameObject(self.me.cells, self.player.cells, 
                            self.colors, self.options, self.powerups,  
                            self.player.color, self.me.color, False, 
                            self.me.score, self.player.score
                            )
        self.chosenColor = self.minimax(thullu, 4, True, float('-inf'),float('inf'))[1]
        self.changeCellColors()
    
    def evaluate(self, gameObject):
        """Returns the difference between both scores after a move is made"""
        return gameObject.myScore - gameObject.oppScore

    # minimax inspiration
    # https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-1-introduction/
    # https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-2-evaluation-function/?ref=rp
    # https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-3-tic-tac-toe-ai-finding-optimal-move/?ref=rp
    # https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/?ref=rp
    # https://www.youtube.com/watch?v=fInYh90YMJU
    # https://www.youtube.com/watch?v=l-hh51ncgDI
    # alpha beta pruning inspiration
    # https://www.geeksforgeeks.org/minimax-algorithm-in-game-theory-set-4-alpha-beta-pruning/
    # https://www.youtube.com/watch?v=xBXHtz4Gbdo`
    def minimax(self, gameObject, depth:int, isMax:bool, alpha, beta):
        #make a copy of the original game object which has all the original attributes
        #to undo move later
        originalGameObject = copy.deepcopy(gameObject)
        #base case
        if depth == 0 or gameObject.checkGameOver(): return (self.evaluate(gameObject), None)
        #computers turn
        if isMax:
            maxEval = float('-inf')
            bestOption = None
            maxScore = float('-inf')
            #loop through all the options
            for i in gameObject.options:
                #doesn't perform a move if the computers turn has been skipped
                if gameObject.skip:
                    gameObject.skip = False
                    x = self.minimax(gameObject,depth-1,not isMax,alpha,beta)[0]  
                    #change maxEval based on current score after move  
                    if x > maxEval:
                        bestOption = i
                        maxEval = x
                    gameObject.skip = True
                    #undo move (might not be needed but just to be safe)
                    gameObject = originalGameObject
                    continue
                else:
                    #test run performs move
                    self.testRun(gameObject,"comp", i)
                    x = self.minimax(gameObject,depth-1,not isMax, alpha, beta)[0]
                    #if there's a tie the bestOption should be the one with more
                    #cells acquired
                    if x == maxEval and maxScore < gameObject.myScore:
                        bestOption = i
                        maxEval = x
                        maxScore = gameObject.myScore
                    #change maxEval based on current score after move
                    if x > maxEval:
                        bestOption = i
                        maxEval = x
                        maxScore = gameObject.myScore
                    #set new alpha and check if it's greater than beta
                    alpha = max(alpha, maxEval)
                    if beta <= alpha:
                        break
                #undo move
                gameObject = copy.deepcopy(originalGameObject)
            return (maxEval, bestOption)
        #players turn
        if not isMax:
            minEval = float('inf')
            minScore = float('inf')
            bestOption = None
            #loop through all the options
            for i in gameObject.options:
                #doesn't perform a move if the players turn has been skipped
                if gameObject.skip:
                    gameObject.skip = False
                    x = self.minimax(gameObject,depth-1,not isMax, alpha, beta)[0]
                    #change minEvals based on current score after move  
                    if x < minEval:
                        bestOption = i
                        minEval = x
                    gameObject.skip = True
                    #undo move (might not be needed but just to be safe)
                    gameObject = originalGameObject
                    continue
                else:
                    #test run performs move
                    self.testRun(gameObject,"player", i)
                    x = self.minimax(gameObject,depth-1,not isMax, alpha, beta)[0]
                    #if there's a tie the bestOption should be the one with more
                    #cells acquired
                    if x == minEval and minScore < gameObject.oppScore:
                        minScore = gameObject.oppScore
                        bestOption = i
                        minEval = x
                    #change minEval based on current score after move
                    elif x < minEval:
                        minScore = gameObject.oppScore
                        bestOption = i
                        minEval = x
                    #set new beta and check if it's less than alpha
                    beta = min(alpha, minEval)
                    if beta <= alpha:
                        break
                #undo move
                gameObject = copy.deepcopy(originalGameObject)
            return (minEval, bestOption)

    def evalBomb(self,player):
        """Removes 5 cells (or however many for them to be left with just one) from 
        the opposite players blob and reduces their score by 5 (or to 1)"""
        #determine player that is getting cells removed
        if player == self.player: victim = self.me
        else: victim = self.player
        newList = []
        for i in range(5):
            #user has to be left with at least one cell to keep game going
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
                self.compTurn()
        elif self.turn == "me":
            self.me.updateCells(self.player)
            if self.skiparoo:
                self.turn = "me"
                self.evalCompSkip()
            else: self.turn = "player"
        if self.player.checkGameOver(self.me): self.setActiveMode("gameover2")
    
    def testRun(self,gameObject,turn, color):
        """Simulates a game at the current state of the game to allow the computer
         to make a move in minmax and look at outcomes without affecting the actual game"""
        self.colOptions = ["medium aquamarine", "light coral", "forest green", "chartreuse2", "indianred3", "dark slate gray"]
        self.remove = False
        self.double = False
        def updatePowerups(other):
            updated = dict ()
            for key,val in gameObject.powerups.items():
                if key not in gameObject.myCells and key not in gameObject.yourcells: 
                    updated[key] = val
            powerups = updated

        def updateOptions(chosenColor,opponentColor):
            updated = []
            for color in self.colOptions:
                if color != chosenColor and color != opponentColor: updated.append(color)
            gameObject.options = updated
            if self.remove:
                gameObject.options = gameObject.options[0:2]
                self.remove = False

        def chooseColor(colors:list, row:int, col:int):
            dirs = [(-1,0),(0,-1),(1,0),(0,1)]
            colOptions,notOptions = ["medium aquamarine", "light coral", "forest green", "chartreuse2", "indianred3", "dark slate gray"],[]
            for (drow,dcol) in dirs:
                if 0 <= row+drow < 10 and 0 <= col+dcol < 10:
                    notOptions.append(colors[row+drow][col+dcol])
                if row == 9 and col == 0:
                    notOptions.append(colors[0][9])
            newOptions = []
            for color in colOptions:
                if color not in notOptions:
                    newOptions.append(color)
            return random.choice(newOptions)

        def evalBomb():
            if turn == "comp": 
                victim = gameObject.yourCells
                gameObject.oppScore -= 5
                if gameObject.oppScore < 1:
                    gameObject.oppScore = 1
            else: 
                victim = gameObject.myCells
                gameObject.myScore -= 5
                if gameObject.myScore < 1:
                    gameObject.myScore = 1 
            newList = []
            for i in range(5):
                if len(victim) != 1:
                    x = victim.pop()
                    newList.append(x)
                    gameObject.board[x[0]][x[1]] = None
            for (row,col) in newList:
                gameObject.board[row][col] = chooseColor(gameObject.board,row,col)
            
        def evalPowerups(coordinate, opponentCells, powerups)->None:
            if powerups[coordinate]== "skip": gameObject.skip = True
            elif powerups[coordinate] == "remove": self.remove = True
            elif powerups[coordinate] == "plus": 
                if turn == "comp":
                    gameObject.myScore += 1
                else:
                    gameObject.oppScore += 1
            elif powerups[coordinate] == "bomb": evalBomb()
            elif powerups[coordinate] == "double": self.double = True

        def updateCells(chosenColor,opponentColor):
            addedCells = 0
            dirs = [(-1,0),(0,-1),(1,0),(0,1)]
            if turn == "comp":
                for (row,col) in gameObject.myCells:
                    for (drow,dcol) in dirs:
                        if 0 <= row+drow < 10 and 0 <= col+dcol < 10:
                            newRow,newCol = row+drow,col+ dcol
                            if gameObject.board[newRow][newCol] == chosenColor and (newRow,newCol) not in gameObject.myCells:
                                gameObject.myScore += 1
                                addedCells += 1
                                gameObject.myCells.append((newRow,newCol))
                            if (newRow,newCol) in gameObject.powerups:
                                evalPowerups((newRow,newCol),gameObject.yourCells,gameObject.powerups)
                if self.double: 
                    gameObject.myScore += addedCells
                    self.double = False
            else:
                for (row,col) in gameObject.yourCells:
                    for (drow,dcol) in dirs:
                        if 0 <= row+drow < 10 and 0 <= col+dcol < 10:
                            newRow,newCol = row+drow,col+ dcol
                            if gameObject.board[newRow][newCol] == chosenColor and (newRow,newCol) not in gameObject.yourCells:
                                gameObject.oppScore += 1
                                addedCells += 1
                                gameObject.yourCells.append((newRow,newCol))
                            if (newRow,newCol) in gameObject.powerups:
                                evalPowerups((newRow,newCol),gameObject.yourCells,gameObject.powerups)
                if self.double: 
                    gameObject.oppScore += addedCells
                    self.double = False
            updateOptions(chosenColor,opponentColor)

        def changeColors(chosenColor,opponentColor):
            updateCells(chosenColor,opponentColor)
            if turn == "comp":
                for (x,y) in gameObject.myCells:
                    gameObject.board[x][y] = chosenColor
            else:
                for (x,y) in gameObject.yourCells:
                    gameObject.board[x][y] = chosenColor
        #running this method calls a big loop of all the methods being ran which 
        #changes the parameters as needed when a move is made
        changeColors(color,gameObject.oppColor)

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


class gameObject(object):
    """The game object stores all of the attributes we need to run a game. Only needed 
    to store attributes so we don't have to call them every time and to check if 
    the simulation game is over"""
    def __init__(self, myCells, yourCells, board, options, powerups, opoColor, ownColor,skip, myScore, oppScore):
        self.myCells = copy.deepcopy(myCells)
        self.yourCells = copy.deepcopy(yourCells)
        self.board = copy.deepcopy(board)
        self.options = copy.deepcopy(options)
        self.powerups = copy.deepcopy(powerups)
        self.oppColor = copy.deepcopy(opoColor)
        self.ownColor = copy.deepcopy(ownColor)
        self.skip = copy.deepcopy(skip)
        self.myScore = copy.deepcopy(myScore)
        self.oppScore = copy.deepcopy(oppScore)

    def checkGameOver(self):
        """Checks if the game is over"""
        if len(self.myCells) + len(self.yourCells) == 100: return True
        return False