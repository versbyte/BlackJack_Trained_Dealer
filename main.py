import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

# Constants
Suits = ['s', 'h', 'c', 'd']
CardNum = [2, 3, 4, 5, 6, 7, 8, 9, 10, 'A', 'J', 'Q', 'K']

# Global variables
deck = []
PlayerHand = []
BotHand = []
PlayerTurn = True
BotTurn = False
roundLost = False
Dealerlost = False
player_score = 0
bot_score = 0

win_count = 0
loss_count = 0


# GUI elements
greenColor = '#006700'

root = tk.Tk()
root.title("Blackjack")
root.geometry("800x550")
root.config(bg = greenColor)
root.resizable(0, 0)
label_player = tk.Label(root, text="Your Score: 0", bg=greenColor, fg = 'white')
label_bot = tk.Label(root, text="Dealer Score: 0", bg=greenColor, fg = 'white')
player_card_frame = tk.Frame(root)
bot_card_frame = tk.Frame(root)
hit_button = tk.Button(root, text="Hit",bg = 'white', command=lambda: player_hit())
stand_button = tk.Button(root, text="Stand",bg = 'white', command=lambda: player_stand())
label_win_count = tk.Label(root, text=f"Wins: {win_count}", bg=greenColor, fg = 'white')
label_loss_count = tk.Label(root, text=f"Losses: {loss_count}", bg=greenColor, fg = 'white')

# Deck Builder
def deck_builder():
    global deck
    deck = []
    for suits in Suits:
        for cardNum in CardNum:
            deck.append(f"{cardNum}{suits}")  # Format: e.g., "2s", "Ah", "Kd"
    random.shuffle(deck)

# Player Dealing
def PlayerDealing():
    global deck, PlayerHand
    PlayerHand = []
    for i in range(2):
        if len(deck) == 0:  # If the deck is empty, rebuild it
            deck_builder()
        rand1 = random.randint(0, len(deck) - 1)
        PlayerHand.append(deck[rand1])
        deck.pop(rand1)

# Bot Dealing
def BotDealing():
    global deck, BotHand
    BotHand = []
    if len(deck) == 0:  # If the deck is empty, rebuild it
        deck_builder()
    rand1 = random.randint(0, len(deck) - 1)
    BotHand.append(deck[rand1])
    deck.pop(rand1)

# Hand calculator
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

def hit(handList):
    global deck
    if len(deck) == 0:  # If the deck is empty, rebuild it
        deck_builder()
    rand = random.randint(0, len(deck) - 1)
    handList.append(deck[rand])
    deck.pop(rand)
    return handList

def display_cards(hand, frame):
    
    for widget in frame.winfo_children():
        widget.destroy()  # Clear previous cards

    for card in hand:
        # Load the card image from the "Cards/" folder
        image_path = f"Cards/{card}.png"  # Ensure the card filenames match the format
        try:
            image = Image.open(image_path)
            image = image.resize((100, 150), Image.Resampling.LANCZOS)  # Updated resampling method
            photo = ImageTk.PhotoImage(image)
            label = tk.Label(frame, image=photo)
            label.image = photo  
            label.pack(side=tk.LEFT)
        except FileNotFoundError:
            print(f"Image not found: {image_path}")

def start_new_round():
    global PlayerHand, BotHand, PlayerTurn, BotTurn, roundLost, Dealerlost, player_score, bot_score
    PlayerDealing()
    BotDealing()
    PlayerTurn = True
    BotTurn = False
    roundLost = False
    Dealerlost = False

    # Update scores
    player_score = handCalculator(PlayerHand)
    bot_score = handCalculator(BotHand)

    # Update GUI
    label_player.config(text=f"Your Score: {player_score}")
    label_bot.config(text=f"Dealer Score: {bot_score}")
    display_cards(PlayerHand, player_card_frame)
    display_cards(BotHand, bot_card_frame)

def player_hit():
    global PlayerHand, player_score, PlayerTurn, BotTurn, roundLost
    if PlayerTurn and not roundLost:
        PlayerHand = hit(PlayerHand)
        player_score = handCalculator(PlayerHand)
        label_player.config(text=f"Your Score: {player_score}")
        display_cards(PlayerHand, player_card_frame)

        if player_score > 21:
            roundLost = True
            PlayerTurn = False
            BotTurn = True
            dealer_turn()
        elif player_score == 21:
            PlayerTurn = False
            BotTurn = True
            dealer_turn()

def player_stand():
    global PlayerTurn, BotTurn
    if PlayerTurn and not roundLost:
        PlayerTurn = False
        BotTurn = True
        dealer_turn()

def dealer_turn():
    global BotHand, bot_score, BotTurn, roundLost, Dealerlost
    while bot_score < 21 and BotTurn and not roundLost:
        if bot_score < 17:
            BotHand = hit(BotHand)
            bot_score = handCalculator(BotHand)
            label_bot.config(text=f"Dealer Score: {bot_score}")
            display_cards(BotHand, bot_card_frame)
            if bot_score > 21:
                Dealerlost = True
                break
        else:
            BotTurn = False

    check_winner()

def check_winner():
    global roundLost, Dealerlost, player_score, bot_score, loss_count, win_count
    if roundLost:
        #messagebox.showinfo("Game Over", f"You lost, score: {player_score} greater than 21")
        loss_count += 1
        label_loss_count.config(text=f"Losses: {loss_count}")
    elif Dealerlost:
        #messagebox.showinfo("Game Over", f"Dealer lost, score: {bot_score} greater than 21")
        win_count += 1
        label_win_count.config(text=f"Wins: {win_count}")
    elif player_score > bot_score:
        #messagebox.showinfo("Game Over", "You won this round")
        win_count += 1
        label_win_count.config(text=f"Wins: {win_count}")
    elif bot_score > player_score:
        #messagebox.showinfo("Game Over", "Dealer won this round")
        loss_count += 1
        label_loss_count.config(text=f"Losses: {loss_count}")
    else:
        #messagebox.showinfo("Game Over", "Tie")
        print("Tie")

    root.after(1000, start_new_round)  # Wait 1 second before starting the next round

# Initialize the game
def initialize_game():
    global label_player, label_bot, player_card_frame, bot_card_frame, hit_button, stand_button
    label_bot.pack(pady = 10)
    bot_card_frame.pack(padx = 5, pady= 10)
    player_card_frame.pack(padx = 5, pady= 10)
    label_player.pack(pady = 10)
    hit_button.pack(padx = 5, pady= 10)
    stand_button.pack(padx = 5, pady= 10)
    label_win_count.place(x = 10, y = 10)
    label_loss_count.place(x = 10, y = 35)
    deck_builder()
    start_new_round()

# Run the game

initialize_game()
root.mainloop()