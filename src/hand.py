PLAYING = "playing"
STOOD = "stood"
BUST = "bust"
BLACKJACK = "blackjack"
SETTLED = "settled"


class Hand:

    def __init__(self, bet=0, is_split=False):
        self.cards = []
        self.bet = bet
        self.is_split = is_split    # split hands can't be a natural blackjack
        self.status = PLAYING

    def add_card(self, card):
        self.cards.append(card)
        if self.is_bust():
            self.status = BUST
        elif self.is_blackjack():
            self.status = BLACKJACK

    def _value_and_soft(self):
        # Count every ace as 11, then drop aces to 1 one at a time while busting
        total = sum(card.getValue() for card in self.cards)
        soft_aces = sum(1 for card in self.cards if card.is_ace())
        while total > 21 and soft_aces > 0:
            total -= 10
            soft_aces -= 1
        return total, soft_aces > 0

    def get_value(self):
        return self._value_and_soft()[0]

    def is_soft(self):
        # True when an ace is still being counted as 11
        return self._value_and_soft()[1]

    def is_bust(self):
        return self.get_value() > 21

    def is_blackjack(self):
        return len(self.cards) == 2 and self.get_value() == 21 and not self.is_split

    def can_split(self):
        return len(self.cards) == 2 and self.cards[0].rank == self.cards[1].rank

    def split(self):
        # Moves the second card into a new hand with the same bet; returns the new hand
        if not self.can_split():
            raise ValueError("Hand can't be split")
        new_hand = Hand(self.bet, is_split=True)
        new_hand.cards.append(self.cards.pop())
        self.is_split = True
        return new_hand

    def stand(self):
        if self.status == PLAYING:
            self.status = STOOD

    def settle(self):
        self.status = SETTLED

    def __str__(self):
        return ", ".join(str(card) for card in self.cards) + f" ({self.get_value()})"


# test

# from card import Card
#
# hand = Hand(bet=10)
# hand.add_card(Card("A", "Spades"))
# hand.add_card(Card("K", "Hearts"))
# print(hand)                     # A of Spades, K of Hearts (21)
# print(hand.is_blackjack())      # True
# print(hand.status)              # blackjack
#
# soft = Hand()
# soft.add_card(Card("A", "Spades"))
# soft.add_card(Card("6", "Hearts"))
# print(soft.get_value(), soft.is_soft())   # 17 True
# soft.add_card(Card("9", "Clubs"))
# print(soft.get_value(), soft.is_soft())   # 16 False
#
# pair = Hand(bet=25)
# pair.add_card(Card("8", "Spades"))
# pair.add_card(Card("8", "Hearts"))
# print(pair.can_split())         # True
# second = pair.split()
# print(pair, "|", second, "|", second.bet)  # 8 of Spades (8) | 8 of Hearts (8) | 25
#
# split_bj = Hand(is_split=True)
# split_bj.add_card(Card("A", "Spades"))
# split_bj.add_card(Card("K", "Hearts"))
# print(split_bj.is_blackjack())  # False (split hand)
#
# bust = Hand()
# for rank in ("K", "Q", "5"):
#     bust.add_card(Card(rank, "Diamonds"))
# print(bust.is_bust(), bust.status)  # True bust
