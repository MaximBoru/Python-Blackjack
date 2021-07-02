import tkinter as tk
from tkinter import ttk
import locale
from datetime import datetime, time
import objects
import db

class blackjackGUI(ttk.Frame):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent, padding="10 10 10 10")
        self.result = ""
        self.parent = parent
        self.playHand = ""
        self.playerHand = ""
        self.dealHand = ""
        self.dealerHand = ""
        self.deck = ""
        self.playerIt = 2
        self.dealerIt = 1
        self.isBlackjack = False
        self.isBust = False
        db.connect()
        db.create_session()
        self.session = db.get_last_session()
        self.sessionID = self.session[0] + 1
        self.startMoney = self.session[4]
        self.dollars = self.session[4]
        result = locale.setlocale(locale.LC_ALL, '')
        if result == 'C':
            locale.setlocale(locale.LC_ALL, 'en_US')
        else: #default
            locale.setlocale(locale.LC_ALL, 'en_US')
        #maybe reference locale in ui.py
        self.startMoneyText = tk.StringVar()
        self.betText = tk.StringVar()
        self.dealerCardsText = tk.StringVar()
        self.dealerPointsText = tk.StringVar()
        self.playerCardsText = tk.StringVar()
        self.playerPointsText = tk.StringVar()
        self.resultText = tk.StringVar()
        #init comps
        self.initComponents()

    def initComponents(self):
        self.pack(fill=tk.BOTH, expand=True)
        ttk.Label(self, text="Money:").grid(column=0, row=0, sticky=tk.E)
        ttk.Entry(self, width = 25, textvariable=self.startMoneyText, state="readonly").grid(column=1, row=0, sticky=tk.W)
        self.startMoneyText.set(locale.currency(self.dollars))
        #Bet
        ttk.Label(self, text="Bet:").grid(column=0, row=1, sticky=tk.E)
        ttk.Entry(self, width=25, textvariable=self.betText).grid(column=1, row=1, sticky=tk.W)
        #Dealer
        ttk.Label(self, text="DEALER").grid(column=0, row=2, sticky=tk.E)
        ttk.Label(self, text="Cards:").grid(column=0, row=3, sticky=tk.E)
        ttk.Entry(self, width=50, textvariable=self.dealerCardsText, state="readonly").grid(column=1, row=3, sticky=tk.W)
        ttk.Label(self, text="Points:").grid(column=0, row=4, sticky=tk.E)
        ttk.Entry(self, width=25, textvariable=self.dealerPointsText, state="readonly").grid(column=1, row=4, sticky=tk.W)
        #Player
        ttk.Label(self, text="YOU").grid(column=0, row=5, sticky=tk.E)
        ttk.Label(self, text="Cards:").grid(column=0, row=6, sticky=tk.E)
        ttk.Entry(self, width=50, textvariable=self.playerCardsText, state="readonly").grid(column=1, row=6, sticky=tk.W)
        ttk.Label(self, text="Points:").grid(column=0, row=7, sticky=tk.E)
        ttk.Entry(self, width=25, textvariable=self.playerPointsText, state="readonly").grid(column=1, row=7, sticky=tk.W)
        #Result
        ttk.Label(self, text="Results:").grid(column=0, row=9, sticky=tk.E)
        ttk.Entry(self, width=50, textvariable=self.resultText, state="readonly").grid(column=1, row=9, sticky=tk.W)
        self.resultText.set(self.result)  # get the value from the database of start money and put here

        self.makeButtons()
        for child in self.winfo_children():
            child.grid_configure(padx=5, pady=3)

    def makeButtons(self):
        #Button frame to store the hit and stand buttons
        buttonFrame = ttk.Frame(self, padding="0 0 155 0")
        buttonFrame.grid(column=0, row=8, columnspan=2, sticky=tk.E)

        ttk.Button(buttonFrame, text="Hit", state="disabled").grid(column=0, row=0, sticky=tk.W)
        ttk.Button(buttonFrame, text="Stand", state="disabled").grid(column=1, row=0, sticky=tk.W)  # command hit and stand
        #frame for second set of buttons
        buttonFrame2 = ttk.Frame(self, padding="0 0 155 0")
        buttonFrame2.grid(column=0, row=10, columnspan=2, sticky=tk.E)
        ttk.Button(buttonFrame2, text="Play", command=self.playButton).grid(column=0, row=0, sticky=tk.W)
        ttk.Button(buttonFrame2, text="Exit", command=self.parent.destroy).grid(column=1, row=0, sticky=tk.W)
        if self.dollars <= 0:
            buttonFrame2 = ttk.Frame(self, padding="0 0 160 0")
            buttonFrame2.grid(column=0, row=10, columnspan=2, sticky=tk.E)
            ttk.Button(buttonFrame2, text="Play", state="disabled").grid(column=0, row=0, sticky=tk.W)
            ttk.Button(buttonFrame2, text="Exit", command=self.parent.destroy).grid(column=1, row=0, sticky=tk.W)
            self.resultText.set("You have insufficient money to play")

    def playButton(self):
        try:
            if float(self.betText.get()) > 0:
                ttk.Label(self, text="Bet:").grid(column=0, row=1, sticky=tk.E, padx="5")
                ttk.Entry(self, width=25, textvariable=self.betText, state="readonly").grid(column=1, row=1, sticky=tk.W, padx="5")
                self.deck = objects.Deck()
                self.resultText.set("")
                self.isBlackjack = False
                self.isBust = False
                self.playerIt = 2
                self.dealerIt = 1
                buttonFrame = ttk.Frame(self, padding="0 0 160 0")
                buttonFrame.grid(column=0, row=8, columnspan=2, sticky=tk.E)
                ttk.Button(buttonFrame, text="Hit", state="enabled", command=self.hitButton).grid(column=0, row=0, sticky=tk.W)
                ttk.Button(buttonFrame, text="Stand", state="enabled", command=self.standButton).grid(column=1, row=0, sticky=tk.W)
                #Creating deck and starting hands
                self.playerHand = objects.Hand(self.deck)
                self.playerHand.addCard(self.deck)
                self.playerHand.addCard(self.deck)
                self.dealerHand = objects.Hand(self.deck)
                self.dealerHand.addCard(self.deck)
                #player
                self.playHand = (str(self.playerHand.hand[0]) + str(self.playerHand.hand[1]))
                self.playerCardsText.set(self.playHand)
                self.playerPointsText.set(self.playerHand.handTotal())
                #dealer
                self.dealHand = (str(self.dealerHand.hand[0]))
                self.dealerCardsText.set(self.dealHand)
                self.dealerPointsText.set(self.dealerHand.handTotal())
                buttonFrame2 = ttk.Frame(self, padding="0 0 160 0")
                buttonFrame2.grid(column=0, row=10, columnspan=2, sticky=tk.E)
                ttk.Button(buttonFrame2, text="Play", state="disabled").grid(column=0, row=0, sticky=tk.W)
                ttk.Button(buttonFrame2, text="Exit", state="disabled").grid(column=1, row=0, sticky=tk.W)
                if self.playerHand.handTotal() == 21:
                    ttk.Button(buttonFrame, text="Hit", state="disabled").grid(column=0, row=0, sticky=tk.W)
                    ttk.Button(buttonFrame, text="Stand", state="disabled").grid(column=1, row=0, sticky=tk.W)
                    self.isBlackjack = True
                    self.updateMoney()
                if self.playerHand.handTotal() > 21: #for double ace
                    print("bust")
                    self.resultText.set("Bust, you lose")
                    self.isBust = True
                    ttk.Button(buttonFrame, text="Hit", state="disabled").grid(column=0, row=0, sticky=tk.W)
                    ttk.Button(buttonFrame, text="Stand", state="disabled").grid(column=1, row=0, sticky=tk.W)
                    self.updateMoney()
            else:
                self.resultText.set("You must place a valid bet to play (>0)")
        except ValueError:
            self.resultText.set("You must place a valid numerical bet to play")

    def hitButton(self):
        self.resultText.set("")
        buttonFrame = ttk.Frame(self, padding="0 0 160 0")
        buttonFrame.grid(column=0, row=8, columnspan=2, sticky=tk.E)
        ttk.Button(buttonFrame, text="Hit", state="enabled", command=self.hitButton).grid(column=0, row=0, sticky=tk.W)
        ttk.Button(buttonFrame, text="Stand", state="enabled", command=self.standButton).grid(column=1, row=0, sticky=tk.W)

        self.playerHand.addCard(self.deck)
        self.playHand = self.playHand + str(self.playerHand.hand[self.playerIt])
        self.playerIt += 1
        #print(self.playHand)
        self.playerCardsText.set(self.playHand)
        self.playerPointsText.set(self.playerHand.handTotal())

        if self.playerHand.handTotal() > 21:
            #print("bust")
            self.resultText.set("Bust, you lose")
            self.isBust = True
            ttk.Button(buttonFrame, text="Hit", state="disabled").grid(column=0, row=0, sticky=tk.W)
            ttk.Button(buttonFrame, text="Stand", state="disabled").grid(column=1, row=0, sticky=tk.W)
            self.updateMoney()

    def standButton(self): #this is the dealers turn and game resolution
        buttonFrame = ttk.Frame(self, padding="0 0 160 0")
        buttonFrame.grid(column=0, row=8, columnspan=2, sticky=tk.E)
        ttk.Button(buttonFrame, text="Hit", state="disabled").grid(column=0, row=0, sticky=tk.W)
        ttk.Button(buttonFrame, text="Stand", state="disabled").grid(column=1, row=0, sticky=tk.W)
        while self.dealerHand.handTotal() < 17:
            self.dealerHand.addCard(self.deck)
            self.dealHand = self.dealHand + str(self.dealerHand.hand[self.dealerIt])
            self.dealerIt += 1
            #print(self.dealHand)
            self.dealerCardsText.set(self.dealHand)
            self.dealerPointsText.set(self.dealerHand.handTotal())
        self.updateMoney()




    def updateMoney(self):
        #function for updating money, jump to this function when a game ends and update the values
        bet = float(self.betText.get())
        buttonFrame2 = ttk.Frame(self, padding="0 0 160 0")
        buttonFrame2.grid(column=0, row=10, columnspan=2, sticky=tk.E)
        if self.isBlackjack == True:
            bet = bet * 1.5
            self.dollars = (self.dollars + bet)
            self.startMoneyText.set(locale.currency(self.dollars))
            self.resultText.set("***Blackjack!!*** 3:2 payout")
        elif self.isBust == True:
            self.dollars = (self.dollars - bet)
            self.startMoneyText.set(locale.currency(self.dollars))
        elif self.playerHand.handTotal() > self.dealerHand.handTotal() or self.dealerHand.handTotal() > 21:
            self.dollars = (self.dollars + bet)
            self.startMoneyText.set(locale.currency(self.dollars))
            self.resultText.set("Congratz, you win!!")
        elif self.playerHand.handTotal() > self.dealerHand.handTotal():
            self.resultText.set("Draw, chips returned")
        else:
            self.dollars = (self.dollars - bet)
            self.startMoneyText.set(locale.currency(self.dollars))
            self.resultText.set("Sorry, you lose..")
        if self.dollars <= 0:
            ttk.Button(buttonFrame2, text="Play", state="disabled").grid(column=0, row=0, sticky=tk.W)
            ttk.Button(buttonFrame2, text="Exit", command=self.parent.destroy).grid(column=1, row=0, sticky=tk.W)
            self.resultText.set("You have insufficient money to play")
        ttk.Label(self, text="Bet:").grid(column=0, row=1, sticky=tk.E, padx="5")
        ttk.Entry(self, width=25, textvariable=self.betText).grid(column=1, row=1, sticky=tk.W, padx="5")
        ttk.Button(buttonFrame2, text="Play", state="enabled", command=self.playButton).grid(column=0, row=0, sticky=tk.W)
        ttk.Button(buttonFrame2, text="Exit", state="enabled", command=self.parent.destroy).grid(column=1, row=0, sticky=tk.W)

if __name__ == "__main__":
    startTime = (datetime.now())
    window = tk.Tk()
    window.title("Blackjack")
    bGame = blackjackGUI(window)
    window.mainloop()
    stopTime = (datetime.now())
    #getting components to make the object in objects.py
    sessionID = bGame.sessionID
    startMoney = bGame.startMoney
    stopMoney = bGame.dollars
    #making the object
    sessionObj = objects.Session(sessionID, startTime, startMoney, stopTime, stopMoney)
    #print(sessionObj.sessionID)
    #print(sessionObj.startTime)
    #print(sessionObj.startMoney)
    #print(sessionObj.stopTime)
    #print(sessionObj.stopMoney)
    db.add_session(sessionObj)

