RANK_VALUES = {
    "2": 2, "3": 3, "4": 4, "5": 5,
    "6": 6, "7": 7, "8": 8, "9": 9,
    "10": 10, "J": 10, "Q": 10, "K": 10,
    "A": 11
}

SUITS = ("Diamonds", "Hearts", "Spades", "Clubs")

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

    def getValue(self):
        return RANK_VALUES[self.rank]

    def getSuit(self):
        return self.suit

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
# print(card1.getValue())
# print(card1.getValue() > card2.getValue())
