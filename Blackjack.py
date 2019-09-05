import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}

playing = True

class Card:
    
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return self.rank +' of ' +self.suit

class Deck:
    
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank)) # Build Card objects and add them to the list
    
    def __str__(self):
        deck_value = ''
        for card in self.deck:
            deck_value += '\n '+card.__str__()
        return ' The deck has :\n' + deck_value

    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        single_card = self.deck.pop()
        return single_card

class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces
        
    
    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]
        
    
    def hand_value(self,name = 'Current'):
        for card in self.cards:
            if card.rank == 'Ace' and self.value >21:
                self.value -= 10
        print (f"{name} Hand value : {self.value}")
    
    def adjust_for_ace(self):
        pass

class Chips:
    
    def __init__(self):
        self.total = 200  # This can be set to a default value or supplied by a user input
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet

def take_bet(chips):
    
    while True:
        try:
            chips.bet = int(input("How much money do you wanna bet?"))
        except TypeError:
            print("Please enter a number, Please try again")
        else:
            if chips.bet > chips.total:
                print(f"You only have {chips.value} worth of chips, Please try again")
                continue
            else:
                break

def hit(deck,hand):
    hand.add_card(deck.deal())
    #hand.hand_value()

def hit_or_stand(deck,hand):
    global playing  # to control an upcoming while loop
    while True:
        res = input("\nDo you want to hit or stand? Enter 'h' or 's'")
        if res[0].lower() == 'h':
            hit(deck,hand)
            break
        elif res[0].lower() == 's':
            print("\nPlayer stands. Dealer is playing")
            playing = False
            break
        else:
            print("\n Please enter either 's' or 'h'")
            continue