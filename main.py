import random

Suits = ['s', 'h', 'c', 'd']
CardNum = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'A', 'J', 'Q', 'K']

#Deck Builder
def deck_builder():
    deck = []
    for suits in Suits:
        for cardNum in CardNum:
            deck.append(format(cardNum) + '' + suits)
    random.shuffle(deck)
    return deck #Returns the whole deck

#Player Dealing
def PlayerDealing(deck):
    hand = []
    if len(deck) == 0:
        deck = deck_builder()
    
    for i in range(2):
        rand1 = random.randint(0, len(deck) - 1)
        hand.append(deck[rand1])
        deck.pop(rand1)
    
    return hand

#Bot Dealing
def BotDealing(deck):
    hand = []
    if len(deck) == 0:
        deck = deck_builder()
    
    rand1 = random.randint(0, len(deck) - 1)
    hand.append(deck[rand1])
    deck.pop(rand1)

    return hand


#Hand calculator

def handCalculator(handList):
    total = 0
    ace_count = 0
    for card in handList:
        value = card[:-1]  # Removes the suit
        if value in ['J', 'Q', 'K']:
            total += 10
        elif value == 'A':
            total += 11
            ace_count += 1
        else:
            total += int(value)  

    while total > 21 and ace_count > 0:
        total -= 10  
        ace_count -= 1 
    return total

def hit(deck, handList):
    rand = random.randint(0, len(deck) - 1)
    handList.append(deck[rand])
    deck.pop(rand)
    return handList


#Game logic

def runGame():
    deck = deck_builder()

    PlayerHand = PlayerDealing(deck)
    BotHand = BotDealing(deck)

    PlayerTurn = True
    BotTurn = False

    roundLost = False
    Dealerlost = False


    player_score = handCalculator(PlayerHand)
    bot_score = handCalculator(BotHand)
    print(f"Your current score: {player_score}")
    print(f"Current Dealer score: {bot_score}")

    while player_score < 21 and PlayerTurn and not roundLost:
        player_choice = str(input('hit or stand? ---> '))

        if player_choice == 'hit':

            PlayerHand = hit(deck , PlayerHand)
            print(PlayerHand)
            player_score = handCalculator(PlayerHand)
            print(f"Your current score: {player_score}")

            if player_score > 21:
                BotHand = hit(deck, BotHand)
                print(BotHand)
                roundLost = True
                BotTurn = True
            if player_score == 21:
                print("BLACKJACK !!!")
                print("Dealer's turn now!")
                BotHand = hit(deck, BotHand)
                print(f"dealer hand {BotHand}")
                bot_score = handCalculator(BotHand)
                print(bot_score)
                PlayerTurn = False
                BotTurn = True

        elif player_choice == 'stand':
            print("Dealer's turn now!")
            BotHand = hit(deck, BotHand)
            print(BotHand)
            bot_score = handCalculator(BotHand)
            print(bot_score)
            PlayerTurn = False
            BotTurn = True
            

        
    #Dealer strategy will be enhanced using Neural Network implementation in the future !!        
    while bot_score < 21 and BotTurn and not roundLost:
        if bot_score < 17:
            BotHand = hit(deck, BotHand)
            print(BotHand)
            bot_score = handCalculator(BotHand)
            print(f"Current Dealer score: {bot_score}")
            if bot_score > 21:
                Dealerlost = True
                break
        else:
            BotTurn = False

    
    #Checking who won
    if roundLost:
        print(f"You lost, score: {player_score} greater than 21")
    elif Dealerlost:
        print(f"Dealer lost, score: {bot_score} greater than 21")
    elif player_score > bot_score:
        print("You won this round")
    elif bot_score > player_score:
        print("Dealer won this round")
    else:
        print("Tie")      


runGame()
    