#https://diderot-production.s3.amazonaws.com/media/courses_public/CMU%3APittsburgh%2C%20PA%3A15112%3ASummer-2%3A2019-20/HOMEWORKS/ch%3Ahw13/chapter_attachments/a781ddc2-d1d2-11ea-94c3-0ab634db4e5d_cmu_112_graphics.py
from cmu_112_graphics import *
import random
import sys  
from filler import *
class HelpMode(Mode):
    def appStarted(self):
        self.screen = "home"
        self.lastWidth = self.width
        #made on Paint X
        self.home = self.loadImage("homepage.png")
        #made on Paint X
        self.login = self.loadImage("login.png")
        #made on Paint X
        self.signup = self.loadImage("signup.png")
        #made on google docs
        self.instructions = self.loadImage("instructions.png")
        #made on google docs
        self.choose = self.loadImage("choose.png")
        #made on google docs
        self.hard = self.loadImage("hard.png")
        self.timerFiredCall = 1
        self.username =""
        first = dict()
        with open("users.txt", "rt") as names:
            for username in names:
                x = username.split(" ")
                if "\n" in x[1]:
                    x[1] = x[1][0:-1]
                first[x[0]] = float(x[1])
        x = sorted(first.items(), key=lambda x: x[1])
        self.users = dict()
        for pair in x:
            self.users[pair[0]] = pair[1]

    def resetImage(self):
        #made on Paint X
        if self.screen == "home" or self.screen == "error":
            self.home = self.loadImage("homepage.png")
            self.imageSize = int(self.width//1.05)
            self.w,self.h = self.home.size
            self.home = self.scaleImage(self.home, self.imageSize/self.w)
        elif self.screen == "login":
            self.login = self.loadImage("login.png")
            self.imageSize = int(self.width//1.05)
            self.w,self.h = self.login.size
            self.login = self.scaleImage(self.login, self.imageSize/self.w)
        elif self.screen == "signup":
            self.signup = self.loadImage("signup.png")
            self.imageSize = int(self.width//1.05)
            self.w,self.h = self.signup.size
            self.signup = self.scaleImage(self.signup, self.imageSize/self.w)
        elif self.screen == "instructions":
            self.instructions = self.loadImage("instructions.png")
            self.imageSize = int(self.width//1.05)
            self.w,self.h = self.instructions.size
            self.instructions = self.scaleImage(self.instructions, self.imageSize/self.w)
        elif self.screen == "choose":
            self.choose = self.loadImage("choose.png")
            self.imageSize = int(self.width//1.05)
            self.w,self.h = self.choose.size
            self.choose = self.scaleImage(self.choose, self.imageSize/self.w)
        elif self.screen == "hard":
            self.choose = self.loadImage("hard.png")
            self.imageSize = int(self.width//1.05)
            self.w,self.h = self.hard.size
            self.hard = self.scaleImage(self.hard, self.imageSize/self.w)

    def timerFired(self):
        if self.timerFiredCall == 1:
            self.resetImage()
            self.timerFiredCall += 1
        #resets the size of the images every time the canvas changes height and width
        if self.width != self.lastWidth:
            self.resetImage()
            self.lastWidth = self.width

    def keyPressed(self,event):
        if self.screen == "home":
            if event.key == "l": self.screen = "login"
            elif event.key == "s": self.screen = "signup"
            else: return
        elif self.screen == "error":
            if event.key == "l": self.screen = "login"
            if event.key == "s": self.screen = "signup"
            else: return
        elif self.screen == "login":
            if event.key != "Enter":
                if (event.key.isalpha() and len(event.key) == 1) or event.key.isdigit(): self.username += event.key
                elif event.key == "Delete":
                    self.username = self.username[:-1]
            else:
                if self.username in self.users: self.screen = "choose"
                else:
                    self.username = ""
                    self.screen = "error"
        elif self.screen == "signup":
            if event.key != "Enter":
                if (event.key.isalpha() and len(event.key) == 1) or event.key.isdigit(): self.username += event.key
                elif event.key == "Delete": self.username = self.username[:-1]
            else:
                if self.username in self.users:
                    self.username = ""
                    self.screen = "error"
                else:
                    with open("users.txt", "a") as x:
                        x.write(self.username + " inf" + "\n")
                    self.screen = "choose"
        elif self.screen == "leaderboard":
            if event.key == "1": self.screen = "hard"
            elif event.key == "2": self.setActiveMode("play")
            else: return
        elif self.screen == "hard":
            if event.key == "h": self.setActiveMode("hard")
            elif event.key == "e": self.setActiveMode("easy")
            else: return
        elif self.screen == "choose":
            if event.key == "i": self.screen = "instructions"
            elif event.key == "l": self.screen = "leaderboard"
            else: return
        elif self.screen == "instructions":
            if event.key == "1": self.screen = "hard"
            elif event.key == "2": self.setActiveMode("play")
            elif event.key == "l": self.screen = "leaderboard"
            else: return

    def modeActivated(self):
        self.appStarted()
    
    def redrawAll(self,canvas):
        if self.screen == "home":
            canvas.create_image(self.width/2,self.height/2,image=ImageTk.PhotoImage(self.home))
        if self.screen == "login":
            canvas.create_image(self.width/2,self.height/2,image=ImageTk.PhotoImage(self.login))
            welcomeTextSize = self.width//15
            radius = welcomeTextSize * 4
            x0 = self.width/2-radius
            y0 = self.height-self.height/4-welcomeTextSize
            x1 = self.width/2+radius
            y1 = self.height-self.height/4+welcomeTextSize
            canvas.create_rectangle(x0,y0,x1,y1)
            canvas.create_text((x1+x0)/2,(y1+y0)/2,text=self.username,font = f"Times {int(welcomeTextSize//1.1)} bold italic")
        if self.screen == "signup":
            canvas.create_image(self.width/2,self.height/2,image=ImageTk.PhotoImage(self.signup))
            welcomeTextSize = self.width//15
            radius = welcomeTextSize * 4
            x0 = self.width/2-radius
            y0 = self.height-self.height/4-welcomeTextSize
            x1 = self.width/2+radius
            y1 = self.height-self.height/4+welcomeTextSize
            canvas.create_rectangle(x0,y0,x1,y1)
            canvas.create_text((x1+x0)/2,(y1+y0)/2,text=self.username,font = f"Times {int(welcomeTextSize//1.1)} bold italic")
        if self.screen == "leaderboard":
            welcomeTextSize = self.width//20
            canvas.create_rectangle(0,0,self.width,self.height,fill="dark slate gray")
            canvas.create_text(self.width/2,self.height/11,text="Beating the hard computer in the fastest time",font=f"Times {self.height//20} bold italic",fill="rosy brown")
            diff = self.height/(len(self.users)+5)
            canvas.create_text(self.width/2,self.height/7,text="LEADERBOARD",font=f"Times {self.height//20} bold italic",fill="white")
            i = 1
            for key,val in self.users.items():
                if val == float("inf"):
                    pass
                else:
                    canvas.create_text(self.width/2,(i+3)*diff,text=f"{i}: {key} - {val} seconds",font=f"Times {self.height//40} bold italic",fill="white")
                    i += 1
            canvas.create_text(self.width/5,self.height/2, text="Join the leaderboard!\nPress 1 to play the computer\nPress 2 to play a friend",font=f"Times {self.height//50} bold italic",fill="rosy brown")
        if self.screen == "error":
            canvas.create_image(self.width/2,self.height/2,image=ImageTk.PhotoImage(self.home))
            canvas.create_text(self.width/2,30,text="Invalid username, try again", font=f"Times {self.height//20} bold italic",fill="red")
        if self.screen == "hard":
            canvas.create_image(self.width/2,self.height/2,image=ImageTk.PhotoImage(self.hard))
        if self.screen == "choose":
            canvas.create_image(self.width/2,self.height/2,image=ImageTk.PhotoImage(self.choose))
        if self.screen == "instructions":
            canvas.create_image(self.width/2,self.height/2,image=ImageTk.PhotoImage(self.instructions))