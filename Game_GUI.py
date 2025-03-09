import tkinter as tk
from tkinter import messagebox
import random
from Casino_Game import load_profile, save_profile, play_blackjack  # Removed play_roulette import

# Load player profile
profile = load_profile()

# Global Styles
FONT_TITLE = ("Arial", 32, "bold")
FONT_SUBTITLE = ("Arial", 20)
FONT_LABEL = ("Arial", 18)
FONT_BUTTON = ("Arial", 18)
FONT_ENTRY = ("Arial", 16)

# Button Styling
BTN_STYLE = {
    "font": FONT_BUTTON,
    "bg": "#4CAF50",  # Green by default
    "fg": "white",
    "activebackground": "#45A049",
    "activeforeground": "white",
    "padx": 20,
    "pady": 10,
    "bd": 2,
    "relief": "raised"
}

# Function to update balance display
def update_balance():
    balance_label.config(text=f"Balance: ${profile['balance']:.2f}")


# Function for exiting the game
def exit_game():
    save_profile(profile)
    root.quit()


# Function to show stats
def view_stats():
    messagebox.showinfo("Player Stats",
                        f"Total Games Played: {profile['games_played']}\nBalance: ${profile['balance']:.2f}\nWin Ratio: {profile['win_ratio'] * 100:.2f}%")
    update_balance()

# Function to play roulette inside the GUI
def open_roulette_window():
    roulette_window = tk.Toplevel(root)
    roulette_window.title("Roulette Game")
    roulette_window.geometry("1000x600")

    tk.Label(roulette_window, text="Welcome to Roulette!", font=("Arial", 16, "bold")).pack(pady=10)
    tk.Label(roulette_window, text="Place your bet below:", font=("Arial", 12)).pack(pady=5)

    bet_entry = tk.Entry(roulette_window)
    bet_entry.pack()

    tk.Label(roulette_window, text="Choose a bet type:", font=("Arial", 12)).pack(pady=5)
    bet_type_var = tk.StringVar(value="red")  # Default bet type
    bet_options = ["red", "black", "even", "odd", "1-18", "19-36", "0"]
    bet_menu = tk.OptionMenu(roulette_window, bet_type_var, *bet_options)
    bet_menu.pack()

    result_label = tk.Label(roulette_window, text="", font=("Arial", 12))
    result_label.pack(pady=5)

    def spin_roulette():
        try:
            bet = float(bet_entry.get())
            if bet <= 0 or bet > profile["balance"]:
                messagebox.showerror("Invalid Bet", "Enter a valid bet amount.")
                return

            profile["balance"] -= bet  # Deduct bet first
            result = random.randint(0, 36)  # Spin the wheel
            red_numbers = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
            color = "red" if result in red_numbers else "black"
            win = False
            payout = 0

            # Determine if the player wins
            chosen_bet = bet_type_var.get()
            if chosen_bet == "red" and color == "red":
                payout = bet * 2
                win = True
            elif chosen_bet == "black" and color == "black":
                payout = bet * 2
                win = True
            elif chosen_bet == "even" and result % 2 == 0 and result != 0:
                payout = bet * 2
                win = True
            elif chosen_bet == "odd" and result % 2 != 0:
                payout = bet * 2
                win = True
            elif chosen_bet == "1-18" and 1 <= result <= 18:
                payout = bet * 2
                win = True
            elif chosen_bet == "19-36" and 19 <= result <= 36:
                payout = bet * 2
                win = True
            elif chosen_bet == "0" and result == 0:
                payout = bet * 36
                win = True

            if win:
                profile["balance"] += payout
                result_label.config(
                    text=f"Roulette spun: {result} ({color})\nYou won! New Balance: ${profile['balance']:.2f}",
                    fg="green")
            else:
                result_label.config(
                    text=f"Roulette spun: {result} ({color})\nYou lost! New Balance: ${profile['balance']:.2f}",
                    fg="red")

            update_balance()
            save_profile(profile)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a numerical value.")

    spin_button = tk.Button(roulette_window, text="Spin Roulette", command=spin_roulette)
    spin_button.pack(pady=5)

    back_button = tk.Button(roulette_window, text="Return to Main Menu", command=roulette_window.destroy)
    back_button.pack(pady=5)


# Function to open Blackjack window
def start_blackjack():
    profile["balance"] = play_blackjack(profile["balance"], profile)
    update_balance()


# Function to open Slots window
def open_slots_window():
    slots_window = tk.Toplevel(root)
    slots_window.title("Slots Game")
    slots_window.geometry("1000x600")

    tk.Label(slots_window, text="Welcome to Slots!", font=("Arial", 32, "bold")).pack(pady=30)
    tk.Label(slots_window, text="Place your bet below:", font=("Arial", 20)).pack(pady=15)

    bet_entry = tk.Entry(slots_window, font=("Arial", 20), width=10)
    bet_entry.pack()

    highlight_var = tk.BooleanVar()
    highlight_checkbox = tk.Checkbutton(slots_window, text="Highlight Winning Paylines", variable=highlight_var,
                                        font=("Arial", 18))
    highlight_checkbox.pack(pady=15)

    result_label = tk.Label(slots_window, text="", font=("Arial", 28), justify="center")
    result_label.pack(pady=20)

    def spin_slots():
        try:
            bet = float(bet_entry.get())
            if bet <= 0 or bet > profile["balance"]:
                messagebox.showerror("Invalid Bet", "Enter a valid bet amount.")
                return

            profile["balance"] -= bet  # Deduct bet first
            symbols = ["🍒", "🍋", "🔔", "💎", "🍉", "🍀", "🎰", "🔥", "👑", "💰"]  # 10 emoji symbols
            slot_result = [[random.choice(symbols) for _ in range(5)] for _ in range(3)]  # 5 reels, 3 rows

            paylines = [
                [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0)],  # Top row
                [(0, 1), (1, 1), (2, 1), (3, 1), (4, 1)],  # Middle row
                [(0, 2), (1, 2), (2, 2), (3, 2), (4, 2)],  # Bottom row
                [(0, 0), (1, 1), (2, 2), (3, 1), (4, 0)],  # V-shape down
                [(0, 2), (1, 1), (2, 0), (3, 1), (4, 2)],  # V-shape up
                [(0, 0), (1, 1), (2, 2), (3, 1), (4, 2)],  # X-shape diagonal top-left to bottom-right
                [(0, 2), (1, 1), (2, 0), (3, 1), (4, 0)]  # X-shape diagonal bottom-left to top-right
            ]

            win = False
            payout = 0
            winning_positions = []

            for line in paylines:
                line_symbols = [slot_result[y][x] for x, y in line]
                if line_symbols.count(line_symbols[0]) == 5:  # All match
                    payout += bet * 10  # Jackpot multiplier
                    win = True
                    winning_positions.extend(line)
                elif line_symbols.count(line_symbols[0]) == 4:  # 4 matches
                    payout += bet * 5
                    win = True
                    winning_positions.extend(line)
                elif line_symbols.count(line_symbols[0]) == 3:  # 3 matches
                    payout += bet * 2
                    win = True
                    winning_positions.extend(line)

            slot_display = "\n".join(["      ".join(
                [f"[{symbol}]" if (col_idx, row_idx) in winning_positions and highlight_var.get() else symbol for
                 col_idx, symbol in enumerate(row)]) for row_idx, row in enumerate(slot_result)])

            if win:
                profile["balance"] += payout
                result_label.config(text=f"{slot_display}\n\nJackpot! You won! New Balance: ${profile['balance']:.2f}",
                                    fg="green")
            else:
                result_label.config(text=f"{slot_display}\n\nYou lost! New Balance: ${profile['balance']:.2f}",
                                    fg="red")

            update_balance()
            save_profile(profile)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a numerical value.")

    spin_button = tk.Button(slots_window, text="Spin Slots", command=spin_slots)
    spin_button.pack(pady=5)

    back_button = tk.Button(slots_window, text="Return to Main Menu", command=slots_window.destroy)
    back_button.pack(pady=20)

# Initialize Tkinter window
root = tk.Tk()
root.title("Casino Game")
root.geometry("1000x600")

# Title Label
title_label = tk.Label(root, text="Welcome to the Casino!", font=("Arial", 16, "bold"))
title_label.pack(pady=10)

# Balance Label
balance_label = tk.Label(root, text=f"Balance: ${profile['balance']:.2f}", font=("Arial", 14))
balance_label.pack()

# Buttons to select games and actions
roulette_button = tk.Button(root, text="Play Roulette", command=open_roulette_window)
roulette_button.pack(pady=5)

blackjack_button = tk.Button(root, text="Play Blackjack", command=start_blackjack)
blackjack_button.pack(pady=5)

slots_button = tk.Button(root, text="Play Slots", command=open_slots_window)
slots_button.pack(pady=5)

stats_button = tk.Button(root, text="View Stats", command=view_stats)
stats_button.pack(pady=5)

exit_button = tk.Button(root, text="Exit", command=exit_game)
exit_button.pack(pady=5)

# Run the Tkinter event loop
root.mainloop()
