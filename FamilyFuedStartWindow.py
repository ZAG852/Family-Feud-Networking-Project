# Authors: Zachary Garner and Taylor O'neil
# Zachary Garner
# worked on creating all the GUI elements and converting the game portion  to be used
# with the GUI
# Taylor O'neil
#  worked on Game functionality
import tkinter as tk
from tkinter import ttk
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
from tkinter import messagebox
import os
from queue import *
from signal import *
import random
import time
LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)
HEIGHT = 500
WIDTH = 600
NUM_ENTRIES = 0;
NUM_GUESSES = 0
ourScoreEntryBox = []
ALL_ENTRIES = [] #the answers with 0-9 corresponding with 1-10. 0 = 1 where one is the number one answer
TimeToPlay = 120;
q = Queue(maxsize = 0)
category = ""
answers = {}
overAllGuesses = 0
X_Nums = 0
crossBoxes = []
gameOver = False
Clicked = False
stopTimer = False
msgPoints = "Score"+"\t"+str(0) +"\n\r"

def countdownTimer(controller):
    global gameOver
    global msgPoints
    global Clicked
    global TimeToPlay
    global stopTimer
    timer = 0
    gameOver = False
    outOfTime = False
    stopTimer = False
    while((outOfTime == False) and (gameOver == False) and (stopTimer == False)):
        time.sleep(1)
        timer = timer +1
        print("Timer: ",timer)
        if(timer>=TimeToPlay):
            print("GAME OVER")
            outOfTime = True
            gameOver = True
    if(gameOver ==True):
        send(msgPoints)
        waitForResponse(controller)
        NUM_GUESSES =0
        points = 0
        guessed.clear()
        Clicked = False
        category = ""
        overAllGuesses = 0
        gameOver == False
        msgPoints = "Score"+"\t"+str(0) +"\n\r"
def clearAll():
    for x in ALL_ENTRIES:
      x["text"] = ""
    ourScoreEntryBox[0]["text"]= ""
    category = ""
    for x in crossBoxes:
      x["text"] = ""
def survey_results(num):
  categories = ["naming something that costs 1 dollar", "naming countries that speak spanish", "naming something that breaks down"]

  answers = {}
#Question 1 answers and scores
  if num == 0:
    answers = {"FRUIT" : 29, "FAST FOOD" : 23, "SOFT DRINK" : 17, "NEWSPAPER" : 10, "STAMP" : 6, "GUM" :4}
#Question 2 answers and scores
  elif num == 1:
    answers = {"SPAIN" : 38, "MEXICO" : 24, "UNITED STATES": 10, "CUBA": 10, "ARGENTINA" : 5, "COSTA RICA" : 3, "CHILE" : 4, "COLUMBIA" : 4 }
#Question 3 answers and scores
  elif num == 2:
    answers = {"CAR": 44, "BODY" : 22, "COMPUTER": 17, "COMMUNICATION": 7, "FOREIGN RELATIONS": 2, "TV": 2}
#Question 4 answers and scores
  elif num == 3:
    answers = {"CHURCH": 35,"GROCERIES": 24,"LAUNDRY": 12,"CLEAN HOUSE": 6,"SLEEP IN": 6,"EAT OUT": 4}
#Question 5 answers and scores
  elif num == 4:
    answers = {"SOAP": 46,"VINEGAR": 30,"COOKING OIL": 16,"SOY SAUCE": 4,"BACON GREASE": 2}
#Question 6 answers and scores
  elif num == 5:
    answers = {"TV": 33,"PHONE": 25,"COMPUTER": 24,"LAMP": 11,"HEADPHONES": 2,"COMPUTER MOUSE": 2}
#Question 7 answers and scores
  elif num == 6:
    answers = {"COFFEE": 31,"ORANGE JUICE": 30,"MILK": 16,"GRAPEFRUIT JUICE": 6,"WATER": 4,"CHAMPAGNE": 2}
#Question 8 answers and scores
  elif num ==  7:
    answers = {"POLICE CAR": 44,"FIRETRUCK": 16,"AMBULANCE": 15,"TRAIN": 10,"HEARSE": 6,"HUMMER": 2,"LIMO": 2}
#Question 9 answers and scores
  elif num ==  8:
    answers = {"VENDING MACHING": 29,"LAUNDROMAT": 22,"BUS": 21,"PARKING METER": 20,"PAY PHONE": 3,"BANK": 2}
#Question 10 answers and scores
  elif num ==  9:
    answers = {"CELL PHONE": 46,"PURSE": 30,"WALLET": 10,"KEYS": 5,"MONEY": 2,"KIDS": 2,"CAR": 2}
  return answers

def getCategories(num):
    categories = ["naming something that costs 1 dollar", "naming countries that speak spanish", "naming something that breaks down",
                  "Tell me something many people do just once a week.","Name a liquid in your kitchen that you hope no one ever accidentally drinks.",
                  "Name something you always have to keep plugged in.","Name a beverage some people drink exclusively with breakfast.",
                  "Name a type of vehicle you really wouldn't want to hit while driving.","Name a place where people have to use coins.",
                  "Name something you never leave home without."]
    return categories[num]
def guess(_guess, answers, controller):
#there are three guesses, capital and lowercase is ignored
    global NUM_GUESSES
    global points
    global guessed
    global category
    global overAllGuesses
    global gameOver
    global msgPoints
    if(category != ""):
      if( NUM_GUESSES < 3):
          guess = _guess
      #If the guess is in the answers output the points
          i = 0
          #Checks if the guess is in the 
          if guess.upper() in answers and guess.upper() not in guessed:
            overAllGuesses = 1 + overAllGuesses
            for x, y in answers.items(): #Looks for the position to place the text in the GUI
              if guess.upper() == x and guess.upper() not in guessed:#if not already found place it and assign points
                points += y
                guessed += [guess.upper()]
                print(guess +" -Correct")
                ALL_ENTRIES[i]["text"] =x #sets the text of the label boxes for the correct answsers
                break #breaks if found
              else:
                i = i+1 #allows the assigning of correct
          #If the guess is not in the answers output X and 0 points
          else:
            print ("X")
            NUM_GUESSES += 1
            crossBoxes[NUM_GUESSES - 1]["text"] ='X'
                  
          msgPoints = "Score"+"\t"+str(points) +"\n\r"
      if(NUM_GUESSES >= 3 or len(answers) == overAllGuesses):
          gameOver = True
    else:
      ourScoreEntryBox[0]["text"] ="No Category Selected"
      print("No Category Selected")
def receive():
    ###Handles receiving of messages.###
    while True:
        try:
            
            msg = client_socket.recv(BUFSIZ).decode("ascii")#recieves msg from server
            print(msg)
            q.put(msg)#queues the servers message to be processed
        except OSError:
            #q.task_done()
            break

def send(s):
    ###Handles sending of messages.###
    msg = s 
    client_socket.send(msg.encode())
    if msg == "Quit":#if the user quits this will send the quit message to the server and close the client ontop of quiting the app
        client_socket.close()
        app.quit()
#Makes the program shut down correctly on quit
def on_closing():
    global stopTimer
    if messagebox.askokcancel("Quit", "Do you want to quit?"):#asks the user if the want to truely quit
        stopTimer = True
        send("Quit")
        app.destroy()
#this will wait and handle the reponse from the server
def waitForResponse(controller):
    global stopTimer #allows for the stoping of the timer on logout to avoid errors
    global Clicked   #this will allow the theme box to be clicked again if the user logs out
    contin = True
    
    while(contin):
      print(q.qsize()) # wait for server response
      if(not q.empty()):#process response
          while(not q.empty()):#while requests come in while processing the first request so we don't get a back log
            thingToProcess = q.get()
            print(thingToProcess)
            if(thingToProcess.split("\t")[0].strip() == "LoginResponse"):#be sure to change this to be more relevant
              contin = False
              if(thingToProcess.split("\t")[1].strip() == "Success"): #When an account is created
                  controller.show_frame(ChoicePage)
              else:#On a failure with the reason given by the server
                  errorMsg = thingToProcess.split("\t")[1].strip()
                  print(errorMsg)
                  #messagebox.Show("Error", errorMsg)
            if(thingToProcess.split("\t")[0].strip() == "SignUp"):
              if(thingToProcess.split("\t")[1].strip() == "Success"): #When an account is created
                  #messagebox.show("Success", "You Have successfully created an account")
                  contin= False
                  controller.show_frame(StartPage)
              else:
                  print("Error " + thingToProcess.split("\t")[1].strip())
                  contin = False
                  #messagebox.show("Error", thingToProcess.split("\t")[1].strip())
            #will implement time later
            if(thingToProcess.split("\t")[0].strip() == "PlayGame"):
              controller.show_frame(PlayPage) #shows the play page
              contin = False
            if(thingToProcess.split("\t")[0].strip() == "Score"):#affirms if the server got the score
              if(thingToProcess.split("\t")[1].strip() == "Recieved"):
                controller.show_frame(ChoicePage)
                clearAll()
                contin = False
            if(thingToProcess.split("\t")[0].strip() == "NoScore"): #if the client with specific user name does not have any scores
              if(thingToProcess.split("\t")[1].strip() == "Error"): #if there is no user although this will never happen
                print(thingToProcess.split("\t")[2].strip())
              else:
                print(thingToProcess.split("\t")[1].strip()) #if no score
              contin = False
            if(thingToProcess.split("\n")[0].strip() == "Returned Score"): # this will be all the user scores
              print(thingToProcess)
              sv = tk.StringVar()
              sv.set(thingToProcess)
              ourScoreEntryBox[1]["text"] =thingToProcess #The scores for the user
              contin = False
            if(thingToProcess.split("\t")[0].strip() == "Logout"):
              ourScoreEntryBox[1]["text"] ='' #resets the scores on logout
              ourScoreEntryBox[0]["text"] ='' #resets the theme box
              contin = False
              Clicked = False #Clicking possible
              stopTimer = True #stops timer
              clearAll() #clears everything else
              controller.show_frame(StartPage)
                        
def do_Both(msg, controller):
    send(msg) #sends message
    waitForResponse(controller) #waits for response
    
class FamilyFued(tk.Tk):
    def __init__(self,*args,**kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Family Feud")
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        #Dictionary of frames
        self.frames = {}

        for F in (StartPage, ChoicePage, PlayPage,SignUpPage, LoginPage, SettingsPage, ScorePage):
            #adds StartPage to the dictionary
            frame = F(container, self)

            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)


    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

#changes the time
def changeTime(t, timeLabel, controller):
    global TimeToPlay #allows for the modification of the global variable
    if(t == 1):
        TimeToPlay = 120
        timeLabel["text"] = ("The Time is: "+ str(TimeToPlay/60)+" minutes")
        controller.show_frame(ChoicePage)
    if(t == 2):
        TimeToPlay = 180
        timeLabel["text"] = ("The Time is: "+ str(TimeToPlay/60)+" minutes")
        controller.show_frame(ChoicePage)
    if(t == 3):
        TimeToPlay = 300
        timeLabel["text"] = ("The Time is: "+ str(TimeToPlay/60)+" minutes")
        controller.show_frame(ChoicePage)
    
    #We will send time to the server whenever we want to play
    #maybe the client should just handle this and tell the server when its done
    #just a client side change for now

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        canvas = tk.Canvas(self, height = HEIGHT, width=WIDTH, bg = "#FFE174")
        canvas.place(relx = 0, rely = 0, relwidth = 1, relheight = 1)
        label = tk.Label(self, text = "Start Page", font=LARGE_FONT)
        label.place(relx = 0, rely = 0, relwidth = 1, relheight = 0.2)
        LoginMsg = "Login" +"\n\r"
        button1= ttk.Button(self, text="Login", command= lambda: controller.show_frame(LoginPage))
        button1.place(relx = 0.35, rely = 0.75, relwidth = 0.3, relheight = 0.1)
        signUpMsg = "SignUp" +"\n\r"
        button2= ttk.Button(self, text="Sign Up", command= lambda: controller.show_frame(SignUpPage))
        button2.place(relx = 0.35, rely = 0.35, relwidth = 0.3, relheight = 0.1)

class PlayPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        canvas = tk.Canvas(self, height = HEIGHT, width=WIDTH, bg = "#FFE174")
        canvas.place(relx = 0, rely = 0, relwidth = 1, relheight = 1)
        
        logoutMsg ="Logout"+"\t"+"\t"+"\n\r"
        logout = ttk.Button(self, text="logout", command=lambda: do_Both("Logout"+"\n\r", controller))
        logout.place(relx = 0, rely = 0, relwidth = 0.1, relheight = 0.1)
        
        
        guessframe = tk.Frame(self, bg='#F9FF33', bd = 5)
        guessframe.place(relx = 0.5, rely = 0.025, relwidth = 0.75, relheight=0.1, anchor = 'n')

        theGuess = tk.Entry(guessframe, font=NORM_FONT)
        theGuess.place(relwidth = 0.65, relheight = 1)
        
        button = ttk.Button(guessframe, text="Guess", command=lambda: guess(theGuess.get(),answers,controller))
        button.place(relx = 0.7, relwidth = 0.3, relheight = 1)

        middle_frame = tk.Frame(self, bg='#F9FF33', bd = 10)
        middle_frame.place(relx = 0.5, rely = 0.14, relwidth= 0.75, relheight = 0.1, anchor = 'n')

        entryTheme = tk.Label(middle_frame, text=category, font=NORM_FONT)
        #entryTheme.config(state='readonly')
        ourScoreEntryBox.append(entryTheme)
        entryTheme.place(relwidth = 1, relheight = 1)
        
        the_X_frame = tk.Frame(self, bg='#F9FF33', bd = 10)
        the_X_frame.place(relx = 0.5, rely = 0.25, relwidth= 0.75, relheight = 0.1, anchor = 'n')
        
        xSeries1 =tk.Label(the_X_frame, text=category, font=NORM_FONT)
        xSeries1.place(relx = 0, rely = 0, relwidth = 0.3, relheight = 1)
        crossBoxes.append(xSeries1)
        xSeries2 =tk.Label(the_X_frame, text=category, font=NORM_FONT)
        xSeries2.place(relx = 0.35, rely = 0, relwidth = 0.3, relheight = 1)
        crossBoxes.append(xSeries2)
        xSeries3 =tk.Label(the_X_frame, text=category, font=NORM_FONT)
        xSeries3.place(relx = 0.7, rely = 0, relwidth = 0.3, relheight = 1)
        crossBoxes.append(xSeries3)
        lower_frame = tk.Frame(self, bg='#F9FF33', bd = 10)
        lower_frame.place(relx = 0.5, rely = 0.37, relwidth= 0.75, relheight = 0.6, anchor = 'n')

        entry1 = tk.Label(lower_frame, bd = 3,font=NORM_FONT)
        #entry1.config(state='readonly')
        entry1.place(relx = 0, rely = 0, relwidth= 0.4, relheight = 0.1)
        ALL_ENTRIES.append(entry1)
        global NUM_ENTRIES
        NUM_ENTRIES = NUM_ENTRIES+1

        entry2 = tk.Label(lower_frame, bd = 3,font=NORM_FONT)
        #entry2.config(state='readonly')
        entry2.place(relx = 0, rely = 0.2, relwidth= 0.4, relheight = 0.1)
        ALL_ENTRIES.append(entry2)
        NUM_ENTRIES += 1
        
        entry3 = tk.Label(lower_frame, bd = 3,font=NORM_FONT)
        #entry3.config(state='readonly')
        entry3.place(relx = 0, rely = 0.4, relwidth= 0.4, relheight = 0.1)
        ALL_ENTRIES.append(entry3)
        NUM_ENTRIES += 1
        
        entry4 = tk.Label(lower_frame, bd = 3,font=NORM_FONT)
        #entry4.config(state='readonly')
        entry4.place(relx = 0, rely = 0.6, relwidth= 0.4, relheight = 0.1)
        ALL_ENTRIES.append(entry4)
        NUM_ENTRIES += 1
        
        entry5 = tk.Label(lower_frame, bd = 3,font=NORM_FONT)
        #entry5.config(state='readonly')
        entry5.place(relx = 0, rely = 0.8, relwidth= 0.4, relheight = 0.1)
        ALL_ENTRIES.append(entry5)
        NUM_ENTRIES += 1
        
        entry6 = tk.Label(lower_frame, bd = 3,font=NORM_FONT)
        #entry6.config(state='readonly')
        entry6.place(relx = 0.6, rely = 0, relwidth= 0.4, relheight = 0.1)
        ALL_ENTRIES.append(entry6)
        NUM_ENTRIES += 1
        
        entry7 = tk.Label(lower_frame, bd = 3,font=NORM_FONT)
        #entry7.config(state='readonly')
        entry7.place(relx = 0.6, rely = 0.2, relwidth= 0.4, relheight = 0.1)
        ALL_ENTRIES.append(entry7)
        NUM_ENTRIES += 1
        
        entry8 = tk.Label(lower_frame, bd = 3,font=NORM_FONT)
        #entry8.config(state='readonly')
        entry8.place(relx = 0.6, rely = 0.4, relwidth= 0.4, relheight = 0.1)
        ALL_ENTRIES.append(entry8)
        NUM_ENTRIES += 1
        
        entry9 = tk.Label(lower_frame, bd = 3,font=NORM_FONT)
        #entry9.config(state='readonly')
        entry9.place(relx = 0.6, rely = 0.6, relwidth= 0.4, relheight = 0.1)
        ALL_ENTRIES.append(entry9)
        NUM_ENTRIES += 1
        
        entry10 = tk.Label(lower_frame, bd = 3,font=NORM_FONT)
        #entry10.config(state='readonly')
        entry10.place(relx = 0.6, rely = 0.8, relwidth= 0.4, relheight = 0.1)
        ALL_ENTRIES.append(entry10)
        NUM_ENTRIES += 1

        button = ttk.Button(self, text="New Theme", command= lambda: getTheme(controller))
        button.place(relx = 0.4,rely = 0.9, relwidth= 0.2, relheight = 0.1)
def getTheme(controller):
    global NUM_GUESSES
    global points
    global guessed
    global category
    global answers
    global overAllGuesses
    global Clicked
    if(not Clicked):
        Clicked = True
        NUM_GUESSES =0
        points = 0
        guessed.clear()
        clearAll()
        overAllGuesses = 0
        select = random.randint(0, 9)
        category = getCategories(select)
        answers = survey_results(select)
        ourScoreEntryBox[0]["text"] =category
        t1 =Thread(target=countdownTimer,args=(controller,))
        t1.daemon = True
        t1.start()
        print(category)
    else:
        print("You have a category no cheating")

class ScorePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        global ourScoreEntryBox
        label = tk.Label(self, text = "Page 2", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        logoutMsg ="Logout"+"\n\r"
        button1= ttk.Button(self, text="Logout", command=lambda: do_Both("Logout"+"\t"+"\n\r", controller))
        button1.pack()
        button2= ttk.Button(self, text="Back", command=lambda: controller.show_frame(ChoicePage))
        button2.pack()

        ScoreButton = ttk.Button(self, text="Get the Score", command=lambda: do_Both("GetScore" + "\n\r", controller))
        ScoreButton.pack()

        middle_frame = tk.Frame(self, bg='#F9FF33', bd = 10)
        middle_frame.place(relx = 0.5, rely = 0.4, relwidth= 0.75, relheight = 0.6, anchor = 'n')
        S = tk.Scrollbar(middle_frame)
        
        entryScores = tk.Label(middle_frame, font=NORM_FONT)
        #entryTheme.config(state='readonly')
        entryScores.place(relwidth = 1, relheight = 1)
        S.pack(side=tk.RIGHT, fill=tk.Y)
        ourScoreEntryBox.append(entryScores)
class ChoicePage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "Page 2", font=LARGE_FONT)
        label.pack(pady=10,padx=10)
        logoutMsg ="Logout"+"\n\r"
        button1= ttk.Button(self, text="Logout", command=lambda: do_Both("Logout"+"\t"+"\n\r", controller))
        button1.pack()
        playMsg = "PlayGame"+"\n\r"
        button2= ttk.Button(self, text="Play", command=lambda: do_Both(playMsg, controller))
        button2.pack()
        TimeButton = ttk.Button(self, text="Scorings", command=lambda: controller.show_frame(ScorePage))
        TimeButton.pack()
        TimeButton = ttk.Button(self, text="Settings", command=lambda: controller.show_frame(SettingsPage))
        TimeButton.pack()
        
        
class SignUpPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        canvas = tk.Canvas(self, height = HEIGHT, width=WIDTH, bg = "#FFE174")
        canvas.pack()

        mainMenuMsg ="SignUp"+"\t"+ "Stop" +"\t" +"\n\r"
        logout = ttk.Button(self, text="Main Menu", command=lambda: controller.show_frame(StartPage))
        logout.place(relx = 0, rely = 0, relwidth = 0.1, relheight = 0.1)
        
        frame = tk.Frame(self, bg='#F9FF33', bd = 5)
        frame.place(relx = 0.5, rely = 0.05, relwidth = 0.75, relheight=0.1, anchor = 'n')
        
        username = tk.Entry(frame, font = NORM_FONT)
        username.place(relwidth = 0.65, relheight = 1)

        label1 = ttk.Label(frame, font = NORM_FONT, text ="Username")
        label1.configure(anchor="center")
        label1.place(relx =0.7, relwidth = 0.3, relheight=1)
        
        frame2 = tk.Frame(self, bg='#F9FF33', bd = 5)
        frame2.place(relx = 0.5, rely = 0.2, relwidth = 0.75, relheight=0.1, anchor = 'n')
        
        password = tk.Entry(frame2, font = NORM_FONT)
        password.place(relwidth = 0.65, relheight = 1)
        
        label2 = ttk.Label(frame2, font = NORM_FONT, text ="Password")
        label2.configure(anchor="center")
        label2.place(relx =0.7, relwidth = 0.3, relheight=1)
                            
        #signUpMsg = "SignUp"+"\t"+ "AccountMade" +"\t" +username.get()+"\t"+ password.get() +"\n\r"
        signUpB1 = ttk.Button(self, text="Sign Up", command=lambda: do_Both("SignUp"+"\t"+ "AccountMade" +"\t" +username.get()+"\t"+ password.get() +"\n\r", controller))
        signUpB1.place(relx = 0.35,rely = 0.75, relwidth = 0.3, relheight = 0.2)

        
class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        canvas = tk.Canvas(self, height = HEIGHT, width=WIDTH, bg = "#FFE174")
        canvas.pack()
        mainMenuMsg = "Login"+"\t"+ "Stop" +"\t" +"\n\r"
        Mainmenu = ttk.Button(self, text="Main Menu", command=lambda: controller.show_frame(StartPage))
        Mainmenu.place(relx = 0, rely = 0, relwidth = 0.1, relheight = 0.1)
        
        frame = tk.Frame(self, bg='#F9FF33', bd = 5)
        frame.place(relx = 0.5, rely = 0.05, relwidth = 0.75, relheight=0.1, anchor = 'n')
        
        username = tk.Entry(frame, font = 40)
        username.place(relwidth = 0.65, relheight = 1)

        label1 = ttk.Label(frame, font = NORM_FONT, text ="Username")
        label1.configure(anchor="center")
        label1.place(relx =0.7, relwidth = 0.3, relheight=1)
        
        frame2 = tk.Frame(self, bg='#F9FF33', bd = 5)
        frame2.place(relx = 0.5, rely = 0.2, relwidth = 0.75, relheight=0.1, anchor = 'n')
        
        password = tk.Entry(frame2, font = 40)
        password.place(relwidth = 0.65, relheight = 1)
        
        label2 = ttk.Label(frame2, font = NORM_FONT, text ="Password")
        label2.configure(anchor="center")
        label2.place(relx =0.7, relwidth = 0.3, relheight=1)
        
        #LoginMsg = "Login"+"\t"+ "Exist" + "\t" + username.get()+"\t"+ password.get() +"\n"
        button = ttk.Button(self, text="Login", command=lambda: do_Both("Login"+"\t"+ "Exist" + "\t" + username.get()+"\t"+ password.get() +"\n", controller))
        button.place(relx = 0.35,rely = 0.75, relwidth = 0.3, relheight = 0.2)
#sets up the time for gameplay: easy mode, medium mode, hard mode. Most time being easy and least time being hard
class SettingsPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)
        timeText = tk.StringVar()
        timeText.set("The Time is: "+ str(TimeToPlay/60) + " minutes")
        canvas = tk.Canvas(self, height = HEIGHT, width=WIDTH, bg = "#FFE174")
        canvas.place(relx = 0, rely = 0, relwidth = 1, relheight = 1)
        label = tk.Label(self, text = "Settings", font=LARGE_FONT)
        label.place(relx = 0, rely = 0, relwidth = 1, relheight = 0.2)
        timeShown = tk.Label(self, font=LARGE_FONT)
        timeShown["text"] = ("The Time is: "+ str(TimeToPlay/60) + " minutes")
        timeShown.place(relx = 0, rely = 0.55, relwidth = 0.3, relheight = 0.2)
        button1= ttk.Button(self, text="2:00", command= lambda: changeTime(1, timeShown, controller))
        button1.place(relx = 0.35, rely = 0.75, relwidth = 0.3, relheight = 0.1)
        button2= ttk.Button(self, text="3:00", command= lambda: changeTime(2, timeShown, controller))
        button2.place(relx = 0.35, rely = 0.55, relwidth = 0.3, relheight = 0.1)
        button2= ttk.Button(self, text="5:00", command= lambda: changeTime(3, timeShown, controller))
        button2.place(relx = 0.35, rely = 0.35, relwidth = 0.3, relheight = 0.1)
app = FamilyFued()
app.protocol("WM_DELETE_WINDOW", on_closing)


points = 0
guessed = []
HOST = 'localhost'
PORT = 12007

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
receive_thread.start()
app.mainloop()


        
