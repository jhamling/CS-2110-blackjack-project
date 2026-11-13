from constants import RANK_VALUES, SUITS


class Card:

    # Basic card values as integers
    # Follows normal blackjack convention Face cards = 10
    # Important to remember that A can equal 1 if 10 would bust the player *handle in counting logic*

    def __init__(self, rank, suit):
        if rank not in RANK_VALUES:
            raise ValueError(f"Invalid rank: {rank}")
        self.rank = rank

        if suit not in SUITS:
            raise ValueError(f"Invalid suit: {suit}")
        self.suit = suit

    def get_value(self):
        return RANK_VALUES[self.rank]

    def get_suit(self):
        return self.suit

    # checks if A is important for counting logic
    def is_ace(self):
        return self.rank == "A"
    
    def __repr__(self):
        return f"Card({self.rank!r}, {self.suit!r})"   # Card('K', 'Spades')

    def __str__(self):
        return f"{self.rank} of {self.suit}"           # K of Spades

# test

# card1 = Card("K", "Spades")
# card2 = Card("9", "Hearts")
#
# print(card1.get_value())
# print(card1.get_value() > card2.get_value())
