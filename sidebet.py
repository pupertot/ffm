from utils import json_parsing
from constant import POSITION_MAP

class SideBet(object):    
    def __init__(self, data):
        self.positionList = None    #the positions included in the side bet
        self.winner = None          #the 'owner' who won the side bet
        self.payout = 0             #the amount of money that goes to the winner
        self.biggestLoser = None    #whichever idiot performed worst in the side bet
        self.creator = None         #The 'owner' who created the side bet
        self.participants = None    #'everyone' for league wide side bets.  otherwise, list of 'owners' involved.
        self.name = None

    def __repr__(self):
        return {'name': self.name}
    
    def __str__(self):
        return 'Name: ' + self.name