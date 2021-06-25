#https://diderot-production.s3.amazonaws.com/media/courses_public/CMU%3APittsburgh%2C%20PA%3A15112%3ASummer-2%3A2019-20/HOMEWORKS/ch%3Ahw13/chapter_attachments/a781ddc2-d1d2-11ea-94c3-0ab634db4e5d_cmu_112_graphics.py
from cmu_112_graphics import *
import random
import sys  
def chooseColor(colors:list, row:int, col:int)->None:
    """Given a list and an integer representing a row and column number chooses 
    a random color for the cell at the given row and col to be based on the cells 
    surrounding it"""
    dirs = [(-1,0),(0,-1),(1,0),(0,1)]
    colOptions,notOptions = ["medium aquamarine", "light coral", "forest green", "chartreuse2", "indianred3", "dark slate gray"],[]
    #loops through every bordering cell and adds their color to a list
    for (drow,dcol) in dirs:
        if 0 <= row+drow < 10 and 0 <= col+dcol < 10:
            notOptions.append(colors[row+drow][col+dcol])
        if row == 9 and col == 0:
            #the bottom left and top right corner can't start off as being the 
            #same because those are the player squares and they can never be the 
            #same color
            notOptions.append(colors[0][9])
    newOptions = []
    for color in colOptions:
        #if color is not the same as a bordering cell color added to options
        if color not in notOptions:
            newOptions.append(color)
    return random.choice(newOptions)

def choosePowerUpCells()->None:
    """Creates a dictionary that has 8 tuple x,y coordinates as keys and a 
    powerup as the value to represent wehre powerups should go on the filler board 
    drawing"""
    result = dict()
    rows,cols = [0,1,2,3,4,5,5,6,7,8,9],[0,1,2,3,4,6,5,6,7,8,9]
    powerups = ["skip","skip","remove","remove","plus","plus","timesTwo","timesTwo","shuffle","bomb"]
    i = 0
    while i < 10:
        row,col = random.choice(rows),random.choice(cols)
        #don't include starting cells for either player
        if (row,col) not in result and (row,col) != (0,9) and (row,col) != (9,0):
            result[(row,col)] = powerups[i]
            i += 1
            #remove so they are somewhat more spread out
            rows.remove(row)
            cols.remove(col)
    return result

def drawSkip(canvas,cx:int,cy:int,radius:int,color)->None:
    """Takes in an x and y coordinate and a radius and draws a slashed circle at
    the location of radius size"""
    canvas.create_oval(cx-radius,cy-radius,cx+radius,cy+radius,fill=color,outline="black")
    canvas.create_line(cx-radius,cy-radius,cx+radius,cy+radius,fill="black")

def drawRemove(canvas,cx:int,cy:int,r:int)->None:
    """Takes in an x and y coordinate and a radius and draws 2 circles of half 
    radius size"""
    newR = r/2
    cx1,cx2= cx-r,cx+r
    canvas.create_oval(cx1-newR,cy-newR,cx1+newR,cy+newR,fill="medium aquamarine",outline="black",width=3)
    canvas.create_oval(cx2-newR,cy-newR,cx2+newR,cy+newR,fill="light coral",outline="black",width=3)

def drawPlus(canvas,cx:int,cy:int,r:int)->None:
    """Takes in an x and y coordinate and a radius and draws a +1 symbol at the 
    location of radius size"""
    r2= r/2
    cx1,cx2 = cx-r,cx+r2
    canvas.create_line(cx1,cy-r2,cx1,cy+r2,fill="white",width=4)
    canvas.create_line(cx1-r2,cy,cx1+r2,cy,fill="white",width=4)
    canvas.create_line(cx2,cy-r,cx2,cy+r,fill="white",width=4)

def drawTimesTwo(canvas,cx:int,cy:int,r:int,cellWidth:int)->None:
    """Takes in an x and y coordinate and a radius and draws x2 at the location 
    of radius size"""
    cx1,cx2 = cx-r,cx+r
    canvas.create_text(cx1,cy,fill="white",text="x",font =f"Helvetica {cellWidth//3}  bold")
    canvas.create_text(cx2,cy,fill="white",text="2",font=f"Helvetica {cellWidth//2} bold")

def drawShuffle(canvas,cx:int,cy:int,r:int,cellWidth:int,color:str)->None:
    """Takes in an x and y coordinate, radius, cellWidth and a string of a color
    and draws two arrows that switch colors to all options besides the color given"""
    cy1,cy2 = cy-r/2,cy+r/2
    newOps = ["medium aquamarine", "light coral", "forest green", "chartreuse2", "indianred3", "dark slate gray"]
    #makes sure arrow is not the same color as the cell it is in
    newOps.remove(color)
    text1 = random.choice(newOps)
    #makes sure arrows aren't the same colors
    newOps.remove(text1)
    text2 = random.choice(newOps)
    canvas.create_text(cx,cy1,fill=text1,text="<--",font =f"Helvetica {cellWidth//4}  bold")
    canvas.create_text(cx,cy2,fill=text2,text="-->",font=f"Helvetica {cellWidth//4} bold")

def drawBomb(canvas,cx:int,cy:int,r:int)->None:
    """Takes in an x and y coordinate and radius and draws a bomb at the location
    of radius size"""
    lineRx = r/2
    lineRy = r/1.5
    canvas.create_oval(cx-r,cy-r,cx+r,cy+r,fill="black")
    canvas.create_line(cx,cy-r,cx+lineRx,cy-r-lineRy,fill="red",width=3)

def fillColors()->list:
    """Fills up a 10x10 2dlist with color values for each index representing the 
    colors that will go in each cell for the filler board"""
    colors = [[None for i in range(10) ] for i in range(10)]
    for rInd in range(10):
        for cInd in range(10):
            color = chooseColor(colors,rInd, cInd)
            colors[rInd][cInd] = color
    return colors

def drawFillerBoard(canvas, width:int, height:int, colors:list,powerups:dict,options:list, margin=50) -> None:
    """Drawsa 10x10 filler board with powerups included"""
    rows = cols = 10
    cellWidth,cellHeight = (width-(2*margin))//rows,(height-(2*margin))//cols
    canvas.create_rectangle(0,0,width,height,fill="black")
    for rInd in range(rows):
        for cInd in range(cols):
            #homework 7 code
            color = colors[rInd][cInd]
            x0,y0 = margin + (cInd*cellWidth),margin + (rInd*cellHeight)
            x1,y1 = x0 + cellWidth,y0 + cellHeight
            canvas.create_rectangle(x0,y0,x1,y1, fill = color, outline="")
            #end of homework 7 code
            if (rInd,cInd) in powerups:
                thingToDraw = powerups[(rInd,cInd)]
                if thingToDraw == "skip": drawSkip(canvas,(x1+x0)/2, (y1+y0)/2, cellWidth/5,color)
                if thingToDraw == "remove": drawRemove(canvas,(x1+x0)/2, (y1+y0)/2, cellWidth/4)
                if thingToDraw == "plus": drawPlus(canvas,(x1+x0)/2, (y1+y0)/2, cellWidth/4)
                if thingToDraw == "timesTwo": drawTimesTwo(canvas,(x1+x0)/2, (y1+y0)/2, cellWidth//4,cellWidth)
                if thingToDraw == "shuffle": drawShuffle(canvas,(x1+x0)/2, (y1+y0)/2, cellWidth//4,cellWidth,color)
                if thingToDraw == "bomb": drawBomb(canvas,(x1+x0)/2, (y1+y0)/2, cellWidth//4)

def drawOptions(canvas,width:int,height:int,options:list,margin=50)->None:
    """Draws four (or sometimes two) squares at the bottom of the screen
    representing the players options for their turn"""
    cellWidth,cellHeight = (width-(2*margin))//10,(height-(2*margin))//10
    start,cy,r = margin + (2*cellWidth),height-(margin/2),margin/3
    for i in range(len(options)):
        color = options[i]
        x1,y1 = start-r, cy-r
        x2,y2 = start+r,cy+r
        canvas.create_rectangle(x1,y1,x2,y2,fill=color)
        start = start + (cellWidth*2)