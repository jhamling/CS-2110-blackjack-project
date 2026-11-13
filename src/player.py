from betting import is_valid_bet, get_outcome, payout
from constants import WINS, LOSSES, PUSHES, BLACKJACK, MIN_BET
from hand import Hand


class Player:

    def __init__(self, name, bankroll):
        if bankroll < 0:
            raise ValueError(f"Bankroll can't be negative, got {bankroll}")
        self.name = name
        self.bankroll = bankroll
        self.hands = []                                       # Hand objects for the current round
        self.results = {WINS: 0, LOSSES: 0, PUSHES: 0}
        self.bankroll_history = [bankroll]                    # starting bankroll, then one entry per round

    def place_bet(self, amount):
        # Takes the bet out of the bankroll and starts a hand for it; False if the bet isn't valid
        if not is_valid_bet(amount, self.bankroll):
            return False
        self.bankroll -= amount
        self.hands.append(Hand(bet=amount))
        return True

    def split_hand(self, hand):
        # Split needs a second bet equal to the first; False if the hand can't split or bankroll can't cover it
        if not hand.can_split() or hand.bet > self.bankroll:
            return False
        self.bankroll -= hand.bet
        new_hand = hand.split()
        self.hands.insert(self.hands.index(hand) + 1, new_hand)   # play it right after the original
        return True

    def settle_hand(self, hand, dealer_hand):
        # Pays out one hand against the dealer and records the result; returns the outcome
        outcome = get_outcome(hand, dealer_hand)
        self.record_result(WINS if outcome == BLACKJACK else outcome, payout(hand.bet, outcome))
        hand.settle()
        return outcome

    def record_result(self, outcome, amount=0):
        # outcome is WINS, LOSSES, or PUSHES; amount is what goes back to the bankroll (bet + winnings)
        if outcome not in self.results:
            raise ValueError(f"Invalid outcome: {outcome}")
        self.results[outcome] += 1
        self.bankroll += amount

    def end_round(self):
        # Clear hands for the next round; bankroll and stats stay
        self.bankroll_history.append(self.bankroll)
        self.hands = []

    def is_broke(self):
        # Broke = can't cover the table minimum
        return self.bankroll < MIN_BET

    def __repr__(self):
        return f"Player({self.name!r}, {self.bankroll!r})"

    def __str__(self):
        return f"{self.name}: ${self.bankroll}"

# test

# p = Player("Alice", 100)
# print(p.place_bet(150))         # False (more than bankroll)
# print(p.place_bet(25))          # True
# print(p.bankroll)               # 75
# print(p.hands[0].bet)           # 25
# p.record_result(WINS, 50)       # bet 25 back + 25 winnings
# p.end_round()
# print(p.bankroll)               # 125
# print(p.results)                # {'wins': 1, 'losses': 0, 'pushes': 0}
# print(p.bankroll_history)       # [100, 125]
# print(p.hands)                  # []
# print(p.is_broke())             # False
