import random

def play_roulette(money):
   print("\nWelcome to Roulette!")
   bet = money
   money -= bet  # Deduct bet first to ensure losses are accounted for
   valid_bets = ["red", "black", "even", "odd", "1-18", "19-36", "1st12", "2nd12", "3rd12", "0"]


   # Add single number bets 0-36
   for i in range(37):
       valid_bets.append(str(i))


   while True:
       bet_type = input("Place your bet (red / black / even / odd / 1-18 "
                        "/ 19-36 / 1st12 / 2nd12 / 3rd12 / 0-36): ").lower()
       if bet_type in valid_bets:
           break
       print("Invalid bet. Please choose a valid option.")


   result = 24
   red_numbers = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
   color = "red" if result in red_numbers else "black"
   win = False
   payout = 0


   if bet_type.isdigit():
       bet_type = int(bet_type)
       if bet_type == result:
           payout = bet * 36  # Pays 35x winnings plus the original bet
           win = True
   elif bet_type == "red" and color == "red":
       payout = bet * 2
       win = True
   elif bet_type == "black" and color == "black":
       payout = bet * 2
       win = True
   elif bet_type == "even" and result % 2 == 0 and result != 0:
       payout = bet * 2
       win = True
   elif bet_type == "odd" and result % 2 != 0:
       payout = bet * 2
       win = True
   elif bet_type == "1-18" and 1 <= result <= 18:
       payout = bet * 2
       win = True
   elif bet_type == "19-36" and 19 <= result <= 36:
       payout = bet * 2
       win = True
   elif bet_type == "1st12" and 1 <= result <= 12:
       payout = bet * 3
       win = True
   elif bet_type == "2nd12" and 13 <= result <= 24:
       payout = bet * 3
       win = True
   elif bet_type == "3rd12" and 25 <= result <= 36:
       payout = bet * 3
       win = True


   if win:
       money += payout  # Add winnings to balance


   print(f"Roulette spun: {result} ({color if result != 0 else 'green'})")
   print(f"{'You won!' if win else 'You lost!'} New balance: ${money:.2f}")
   return money

play_roulette(100)