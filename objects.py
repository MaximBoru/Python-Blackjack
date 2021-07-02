import random

class Card:
    def __init__(self, rank, suit, points):
        self.rank = rank
        self.suit = suit
        self.points = points
    def __str__(self):
        return self.rank + '' + self.suit + " "

class Deck:
    def __init__(self):
        self.deck = []
        self.buildDeck()
        self.shuffle()
    def buildDeck(self):
        values = {"2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "Jack": 10, "Queen": 10,
                  "King": 10, "Ace": 11}
        for suit in ["D", "H", "C", "S"]:
            for rank in ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]:
                self.deck.append(Card(rank, suit, values[rank]))
    def dealCard(self):
        return self.deck.pop()
    def shuffle(self):
        return random.shuffle(self.deck)
    def count(self):
        return len(self.deck)

class Hand:
    def __init__(self, deck):
        self.deck = deck
        self.hand = []
        self.__index = -1
    def __iter__(self):
        return self
    def __next__(self):
        if self.__index >= len(self.hand) - 1:
            raise StopIteration()
        self.__index += 1
        currCard = self.hand[self.__index]
        return currCard
    def addCard(self, deck):
        self.hand.append(deck.dealCard())
    def count(self):
        return len(self.hand)
    def isBlackjack(self):
        if (self.hand[0].points + self.hand[1].points == 21):
            return(True)
        else:
            return(False)
    def handTotal(self):
        total = 0
        i = 0
        while i < len(self.hand):
            total += self.hand[i].points
            i += 1
        return total

class Session:
    def __init__(self, sessionID, startTime, startMoney, stopTime, stopMoney):
        self.sessionID = sessionID
        self.startTime = startTime
        self.startMoney = startMoney
        self.stopTime = stopTime
        self.stopMoney = stopMoney