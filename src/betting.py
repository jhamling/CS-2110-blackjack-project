from constants import MIN_BET, MAX_BET, BLACKJACK_PAYOUT, WINS, LOSSES, PUSHES, BLACKJACK


def is_valid_bet(amount, bankroll):
    # min <= bet <= min(max bet, bankroll)
    return MIN_BET <= amount <= min(MAX_BET, bankroll)


def get_outcome(hand, dealer_hand):
    # Returns WINS, LOSSES, PUSHES, or BLACKJACK (a natural that beats the dealer, paid 3:2)
    if hand.is_bust():
        return LOSSES                     # player busts lose even if the dealer busts too
    if hand.is_blackjack() and dealer_hand.is_blackjack():
        return PUSHES
    if hand.is_blackjack():
        return BLACKJACK
    if dealer_hand.is_blackjack():
        return LOSSES
    if dealer_hand.is_bust():
        return WINS
    if hand.get_value() > dealer_hand.get_value():
        return WINS
    if hand.get_value() < dealer_hand.get_value():
        return LOSSES
    return PUSHES


def payout(bet, outcome):
    # What goes back to the bankroll (the bet was already taken out when placed)
    if outcome == BLACKJACK:
        return bet + bet * BLACKJACK_PAYOUT   # 3:2
    if outcome == WINS:
        return bet * 2                        # 1:1
    if outcome == PUSHES:
        return bet                            # bet back
    return 0                                  # loss


def remove_broke_players(players):
    # Seats that can't cover the minimum bet leave the table
    return [player for player in players if not player.is_broke()]

# test

# from card import Card
# from hand import Hand
#
# print(is_valid_bet(5, 100))     # False (under min)
# print(is_valid_bet(50, 40))     # False (more than bankroll)
# print(is_valid_bet(25, 100))    # True
#
# bj = Hand(); bj.add_card(Card("A", "Spades")); bj.add_card(Card("K", "Hearts"))
# twenty = Hand(); twenty.add_card(Card("K", "Clubs")); twenty.add_card(Card("Q", "Clubs"))
# print(get_outcome(bj, twenty))  # blackjack
# print(payout(10, BLACKJACK))    # 25.0
# print(payout(10, WINS))         # 20
# print(payout(10, PUSHES))       # 10
# print(payout(10, LOSSES))       # 0
