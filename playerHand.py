"""These classes should be enough to generate a players and corresponding hands.
Author: Anthony Rojas
Date Last Modified: May 1, 2023
 """
import random


#This class will generate a hand for each player based on the remaining cards in the deck
class playerHand:
    def __init__(self, playerName, firstCard, secondCard):
        self.playerName = playerName
        self.firstCard = firstCard
        self.secondCard = secondCard
 
    def getCards(self):
        return [self.firstCard, self.secondCard]
    
    def getName(self):
        return self.playerName
    
class HandGenerator:
    def __init__(self, numPlayers):
        self.numPlayers = numPlayers
        self.playerList = [f'P{x}' for x in range(1,self.numPlayers +1)]
        self.deck = ["As", "Ks", "Qs", "Js", "10s", "9s", "8s", "7s", "6s", "5s", "4s", "3s", "2s",
        "Ah", "Kh", "Qh", "Jh", "10h", "9h", "8h", "7h", "6h", "5h", "4h", "3h", "2h",
        "Ac", "Kc", "Qc", "Jc", "10c", "9c", "8c", "7c", "6c", "5c", "4c", "3c", "2c",
        "Ad", "Kd", "Qd", "Jd", "10d", "9d", "8d", "7d", "6d", "5d", "4d", "3d", "2d"]
        random.shuffle(self.deck)
        self.playerHandsDealt = {}

    def getnumPlayers(self):
        return f'There are {self.numPlayers} playing'
    
    def getPlayerList(self):
        return f'Player list: {self.playerList}'
    
    def dealCards(self):
        numCards = 2
        for player in self.playerList:
            self.playerHandsDealt[player] = [self.deck.pop() for _ in range(numCards)]
        print(f'The remaining cards are: {len(self.deck)}/52')
        return self.playerHandsDealt

        





        
        


