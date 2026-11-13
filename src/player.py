from constants import WINS, LOSSES, PUSHES


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
        # Takes the bet out of the bankroll; refuses bets that are <= 0 or more than the player has
        if amount <= 0 or amount > self.bankroll:
            return False
        self.bankroll -= amount
        return True

    def record_result(self, outcome, payout=0):
        # outcome is WINS, LOSSES, or PUSHES; payout is what goes back to the bankroll (bet + winnings)
        if outcome not in self.results:
            raise ValueError(f"Invalid outcome: {outcome}")
        self.results[outcome] += 1
        self.bankroll += payout

    def end_round(self):
        # Clear hands for the next round; bankroll and stats stay
        self.bankroll_history.append(self.bankroll)
        self.hands = []

    def is_broke(self):
        return self.bankroll <= 0

    def __repr__(self):
        return f"Player({self.name!r}, {self.bankroll!r})"

    def __str__(self):
        return f"{self.name}: ${self.bankroll}"

# test

p = Player("Alice", 100)
print(p.place_bet(150))         # False (more than bankroll)
print(p.place_bet(25))          # True
print(p.bankroll)               # 75
p.record_result(WINS, 50)       # bet 25 back + 25 winnings
p.end_round()
print(p.bankroll)               # 125
print(p.results)                # {'wins': 1, 'losses': 0, 'pushes': 0}
print(p.bankroll_history)       # [100, 125]
print(p.hands)                  # []
print(p.is_broke())             # False
