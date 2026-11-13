# Shared game constants

# Cards
# Face cards = 10; Ace = 11 here, Hand drops it to 1 when 11 would bust
RANK_VALUES = {
    "2": 2, "3": 3, "4": 4, "5": 5,
    "6": 6, "7": 7, "8": 8, "9": 9,
    "10": 10, "J": 10, "Q": 10, "K": 10,
    "A": 11
}
SUITS = ("Diamonds", "Hearts", "Spades", "Clubs")

# Shoe
CARDS_PER_DECK = 52
# Deck penetration (fraction dealt before reshuffle), by number of decks
PENETRATION_RANGES = {
    1: (0.50, 0.70),   # single deck
    2: (0.50, 0.75),   # double deck
    6: (0.67, 0.83),   # 6-deck shoe
    8: (0.69, 0.81),   # 8-deck shoe
}

# Hand statuses
PLAYING = "playing"
STOOD = "stood"
BUST = "bust"
BLACKJACK = "blackjack"
SETTLED = "settled"

# Player results
WINS = "wins"
LOSSES = "losses"
PUSHES = "pushes"
