from constants import DEALER_STANDS_ON
from hand import Hand


class Dealer:

    def __init__(self):
        self.hand = Hand()
        self.hole_revealed = False    # second card stays face down until the players are done

    def take_card(self, shoe):
        # Deals exactly one card so the UI can show each hit; returns the card (None if the shoe is empty)
        card = shoe.deal_out()
        if card is not None:
            self.hand.add_card(card)
        return card

    def get_up_card(self):
        # The face-up card players can see
        return self.hand.cards[0] if self.hand.cards else None

    def reveal_hole_card(self):
        self.hole_revealed = True

    def should_hit(self):
        # Hits on 16 or less, stands on all 17s
        return self.hand.get_value() < DEALER_STANDS_ON

    def clear_hand(self):
        # Fresh hand for the next round
        self.hand = Hand()
        self.hole_revealed = False

    def __str__(self):
        if self.hole_revealed or len(self.hand.cards) < 2:
            return str(self.hand)
        return f"{self.get_up_card()}, [hidden]"

# test

from shoe import Shoe

shoe = Shoe(6)
dealer = Dealer()
dealer.take_card(shoe)
dealer.take_card(shoe)
print(dealer)                   # e.g. K of Spades, [hidden]
print(dealer.get_up_card())     # K of Spades

dealer.reveal_hole_card()
print(dealer)                   # e.g. K of Spades, 5 of Hearts (15)
while dealer.should_hit():
    print("Dealer hits:", dealer.take_card(shoe))   # one card per step
print(dealer)                   # final hand, 17 or more (or bust)

dealer.clear_hand()
print(dealer.hand.cards)        # []
