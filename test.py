import random

def play_blackjack(money):
    print("\nWelcome to Blackjack!")
    bet = money
    money -= bet  # Deduct bet first

    def deal_card():
        """Draws a random card (2-10, face cards = 10, Ace = 11)."""
        cards = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11]  # Face cards = 10, Ace = 11
        return random.choice(cards)

    def calculate_hand(hand):
        """Calculates hand value, converting Aces from 11 to 1 if needed."""
        total = sum(hand)
        aces = hand.count(11)
        while total > 21 and aces:
            total -= 10  # Convert Ace from 11 to 1
            aces -= 1
        return total

    def is_blackjack(hand):
        return len(hand) == 2 and calculate_hand(hand) == 21

    # Deal initial hands
    player_hand = [deal_card(), deal_card()]
    dealer_hand = [deal_card(), deal_card()]

    print(f"Your hand: {player_hand} (Total: {calculate_hand(player_hand)})")
    print(f"Dealer's face-up card: {dealer_hand[0]}")

    player_blackjack = is_blackjack(player_hand)
    dealer_blackjack = is_blackjack(dealer_hand)

    # **Check for Straight Blackjacks Before Player Moves**
    if player_blackjack and dealer_blackjack:
        print("Both you and the dealer have Blackjack! It's a tie, bet refunded.")
        money += bet  # Refund the bet
        win = None  # A tie does not affect win ratio
    elif player_blackjack:
        print("Blackjack! You win 1.5x your bet!")
        money += bet * 2.5  # Player walks away with 2.5x original bet
        win = True
    elif dealer_blackjack:
        print("Dealer has Blackjack! You lose.")
        win = False
    else:
        # **Continue game if no immediate Blackjack**
        while calculate_hand(player_hand) < 21:
            action = input("Do you want to hit or stand? (h/s): ").lower()
            if action == "h":
                player_hand.append(deal_card())
                print(f"Your new hand: {player_hand} (Total: {calculate_hand(player_hand)})")
            else:
                break

        player_total = calculate_hand(player_hand)

        if player_total > 21:
            print("You busted! Dealer wins.")
            win = False
        else:
            # **Dealer's turn**
            print(f"Dealer's hand: {dealer_hand} (Total: {calculate_hand(dealer_hand)})")
            while calculate_hand(dealer_hand) < 17:
                dealer_hand.append(deal_card())
                print(f"Dealer draws: {dealer_hand} (Total: {calculate_hand(dealer_hand)})")

            dealer_total = calculate_hand(dealer_hand)

            if dealer_total > 21 or player_total > dealer_total:
                print("You win!")
                money += bet * 2  # Standard win payout
                win = True
            elif player_total == dealer_total:
                print("It's a tie! Bet refunded.")
                money += bet
                win = None  # A tie does not affect win ratio
            else:
                print("Dealer wins!")
                win = False

    # **Update Win Ratio Only for Wins/Losses (Not Ties)**

    print(f"New balance: ${money:.2f}")
    return money

play_blackjack(100)