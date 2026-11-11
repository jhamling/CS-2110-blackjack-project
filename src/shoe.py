import random

from card import Card, RANK_VALUES, SUITS

CARDS_PER_DECK = 52
# Deck penetration (fraction dealt before reshuffle), by number of decks
PENETRATION_RANGES = {
    1: (0.50, 0.70),   # single deck
    2: (0.50, 0.75),   # double deck
    6: (0.67, 0.83),   # 6-deck shoe
    8: (0.69, 0.81),   # 8-deck shoe
}


def penetration_range(num_decks):
    # Use the closest listed format at or below num_decks (e.g. 4 decks -> double-deck range)
    key = max(k for k in PENETRATION_RANGES if k <= num_decks)
    return PENETRATION_RANGES[key]


class Shoe:

    def __init__(self, num_decks):
        if num_decks < 1:
            raise ValueError(f"num_decks must be at least 1, got {num_decks}")
        self.num_decks = num_decks
        self.cards = []
        self.cut_position = 0
        self.dealt = 0
        self.shuffle()

    def shuffle(self):
        # Rebuild the full shoe so dealt cards come back in
        self.cards = [Card(rank, suit)
                      for _ in range(self.num_decks)
                      for suit in SUITS
                      for rank in RANK_VALUES]
        random.shuffle(self.cards)
        low, high = penetration_range(self.num_decks)
        self.cut_position = int(len(self.cards) * random.uniform(low, high))
        self.dealt = 0

    def deal_out(self):
        # Returns None instead of crashing when the shoe is empty
        if not self.cards:
            return None
        self.dealt += 1
        return self.cards.pop()

    def cards_left(self):
        return len(self.cards)

    def decks_left(self):
        return self.cards_left() / CARDS_PER_DECK

    def needs_shuffle(self):
        return self.dealt >= self.cut_position

# test

shoe = Shoe(6)
print(shoe.cards_left())        # 312
print(shoe.decks_left())        # 6.0
print(shoe.cut_position)        # somewhere between 209 and 258 (67%-83%)

print(shoe.deal_out())          # e.g. K of Spades
print(shoe.cards_left())        # 311

while not shoe.needs_shuffle():
    shoe.deal_out()
print(shoe.cards_left())        # cards left behind the cut card

while shoe.cards_left() > 0:
    shoe.deal_out()
print(shoe.deal_out())          # None (empty shoe doesn't crash)

shoe.shuffle()
print(shoe.cards_left())        # 312 again
