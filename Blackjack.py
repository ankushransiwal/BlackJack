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

def show_some(player,dealer):
    print("\nDealer's hand : ")
    print('-',dealer.cards[1])
    print("- <Hidden Card>")
    print(f"Dealer's hand value : {values[dealer.cards[1].rank]} + ?")
    print("\nPlayer's hand : ",*player.cards, sep = '\n- ')
    player.hand_value("Player's")
    

def show_all(player,dealer):
    print("\nPlayer's hand : ",*player.cards, sep = '\n- ')
    player.hand_value("Player's")
    print("\nDealer's hand : ",*dealer.cards, sep = '\n- ')
    dealer.hand_value("Dealer's")

def player_busts(hand):
    if hand.value > 21:
        return True
    else:
        return False

def player_wins(chips):
    chips.win_bet()
    print("\nPlayer wins, Congratulations")

def dealer_wins(chips):
    chips.lose_bet()
    print("\nPlayer lost, Dealer wins. Better luck next time")
    
    
def who_wins(player_hand,dealer_hand,chips):
    if player_busts(player_hand):
        print("\nPlayer is busted! Total hand exceeded 21")
        dealer_wins(chips)
    elif dealer_busts(dealer_hand):
        print("\nDealer is busted! Total hand exceeded 21")
        player_wins(chips)
    elif dealer_hand.value < player_hand.value:
        player_wins(chips)
    elif dealer_hand.value > player_hand.value:
        dealer_wins(chips)
    else:
        push()

def dealer_busts(hand):
    if hand.value > 21:
        return True
    else:
        return False
        
def push():
    print("\nDealer and Player tied! It's a PUSH")


last_game_player_chips = 0
while True:
    # Print an opening statement
    print("\n ____________________________ ")
    print("|\t\t\t     |\n|  **Welcome to BlackJack**  |")
    print("|____________________________|\n")
    
    # Create & shuffle the deck, deal two cards to each player
    table_deck = Deck()
    table_deck.shuffle()
    player_hand = Hand()
    player_hand.add_card(table_deck.deal())
    player_hand.add_card(table_deck.deal())
    
    dealer_hand = Hand()
    dealer_hand.add_card(table_deck.deal())
    dealer_hand.add_card(table_deck.deal())  
        
    # Set up the Player's chips
    player_chips = Chips()
    player_chips.total += last_game_player_chips
    current_game_player_chips = player_chips.total
    print(f"Total chips available are {player_chips.total}")
    
    # Prompt the Player for their bet
    take_bet(player_chips)
    playing = True
    while playing:  # recall this variable from our hit_or_stand function
        
        # Show cards (but keep one dealer card hidden)
        show_some(player_hand,dealer_hand)  
        
        # Prompt for Player to Hit or Stand
        hit_or_stand(table_deck,player_hand)  
        
        if player_hand.value == 21:
            break
        
        # If player's hand exceeds 21, run player_busts() and break out of loop
        busted = False
        busted = player_busts(player_hand)
        if busted:
            break
    
    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if busted == False:
        while dealer_hand.value < 17:
            hit(table_deck,dealer_hand)
            dealer_hand.hand_value("Dealer's")

        # Show all cards
        show_all(player_hand,dealer_hand)
    
    # Run different winning scenarios
    who_wins(player_hand,dealer_hand,player_chips)    
    
    # Inform Player of their chips total 
    print(f"\nYou have now {player_chips.total} worth of chips")
    if current_game_player_chips > player_chips.total:
        last_game_player_chips -= player_chips.bet
    else:
        last_game_player_chips += player_chips.bet
        
    # Ask to play again
    again = input("Do you want to play again? 'Y' or 'N'")
    if again[0].lower() == 'n':
        break
    elif again[0].lower() == 'y':
        continue
    else:
        print("Invalid Choice, Quitting game")
        break
        
    