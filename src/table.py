from betting import remove_broke_players
from constants import MIN_BET, PLAYING, SETTLED, BOT_STANDS_ON
from dealer import Dealer
from shoe import Shoe


class Table:
    # Runs rounds for a set of seats. Each method is one step the UI can call on its own:
    # take_bets -> deal -> check_dealer_blackjack -> player turn (hit/stand/split)
    # -> bot_step -> dealer_step -> settle -> end_round (reshuffle check)

    def __init__(self, players, num_decks=6):
        self.players = players
        self.shoe = Shoe(num_decks)
        self.dealer = Dealer()

    def seated(self):
        # Players in the current round (they placed a bet)
        return [player for player in self.players if player.hands]

    def deal_to(self, hand):
        card = self.shoe.deal_out()
        hand.add_card(card)
        return card

    # 1. Bets
    def take_bets(self, bets):
        # bets = {player: amount} for human seats; bots bet the table minimum.
        # Returns the players whose bet was refused (they sit this round out)
        refused = []
        for player in self.players:
            amount = MIN_BET if player.is_bot else bets.get(player)
            if amount is None or not player.place_bet(amount):
                refused.append(player)
        return refused

    # 2. Deal: 1 card to each seat, dealer up card, 2nd card to each seat, dealer hole card
    def deal(self):
        for _ in range(2):
            for player in self.seated():
                self.deal_to(player.hands[0])
            self.dealer.take_card(self.shoe)

    # 3. Dealer blackjack check
    def check_dealer_blackjack(self):
        # Dealer blackjack settles every hand now (player blackjacks push) and returns True.
        # Otherwise player blackjacks are paid 3:2 right away so they aren't compared again.
        dealer_blackjack = self.dealer.hand.is_blackjack()
        if dealer_blackjack:
            self.dealer.reveal_hole_card()
        for player in self.seated():
            for hand in player.hands:
                if dealer_blackjack or hand.is_blackjack():
                    player.settle_hand(hand, self.dealer.hand)
        return dealer_blackjack

    # 4. Player turn (also used by bots)
    def current_hand(self, player):
        # The hand waiting on a decision, or None when the player is done
        for hand in player.hands:
            if hand.status == PLAYING:
                return hand
        return None

    def hit(self, player, hand):
        # One card; a bust loses and is settled immediately. Hitting 21 auto-stands (Hand.add_card)
        card = self.deal_to(hand)
        if hand.is_bust():
            player.settle_hand(hand, self.dealer.hand)
        return card

    def stand(self, hand):
        hand.stand()

    def split(self, player, hand):
        # Splits and deals a second card to each hand; False if not allowed
        if not player.split_hand(hand):
            return False
        new_hand = player.hands[player.hands.index(hand) + 1]
        self.deal_to(hand)
        self.deal_to(new_hand)
        return True

    # 5. Bot turns
    def bot_step(self, bot):
        # One bot decision per call; returns False once the bot has no hands left to play
        hand = self.current_hand(bot)
        if hand is None:
            return False
        if hand.get_value() < BOT_STANDS_ON:
            self.hit(bot, hand)
        else:
            self.stand(hand)
        return True

    # 6. Dealer turn
    def dealer_should_play(self):
        # Skip the dealer if every hand is already settled (all busts / blackjacks)
        return any(hand.status != SETTLED for player in self.seated() for hand in player.hands)

    def dealer_step(self):
        # First call reveals the hole card, then one hit per call; False when the dealer is done
        if not self.dealer.hole_revealed:
            self.dealer.reveal_hole_card()
            return True
        if self.dealer.should_hit():
            self.dealer.take_card(self.shoe)
            return True
        return False

    # 7. Settle
    def settle(self):
        # Compares every hand that isn't settled yet against the dealer
        self.dealer.reveal_hole_card()
        for player in self.seated():
            for hand in player.hands:
                if hand.status != SETTLED:
                    player.settle_hand(hand, self.dealer.hand)

    # 8. End of round + reshuffle check
    def end_round(self):
        # Clears hands, drops broke seats; returns True if the shoe was reshuffled
        for player in self.players:
            player.end_round()
        self.dealer.clear_hand()
        self.players = remove_broke_players(self.players)
        if self.shoe.needs_shuffle():
            self.shoe.shuffle()
            return True
        return False


# Terminal version of a full round (python table.py)

if __name__ == "__main__":
    from betting import is_valid_bet
    from constants import MAX_BET
    from player import Player

    you = Player("You", 100)
    table = Table([you, Player("Bot 1", 100, is_bot=True), Player("Bot 2", 100, is_bot=True)])

    while you in table.players:
        print(f"\n===== New round =====  {', '.join(str(p) for p in table.players)}")
        bet = input(f"Your bet ({MIN_BET}-{min(MAX_BET, you.bankroll)}, q to quit): ").strip()
        if bet == "q":
            break
        if not bet.isdigit() or not is_valid_bet(int(bet), you.bankroll):
            print("Invalid bet")
            continue

        table.take_bets({you: int(bet)})
        table.deal()
        for player in table.seated():
            print(f"{player.name}: {player.hands[0]}")
        print(f"Dealer: {table.dealer}")

        if table.check_dealer_blackjack():
            print(f"Dealer has blackjack! {table.dealer}")
        else:
            while (hand := table.current_hand(you)) is not None:
                print(f"\nYour hand: {hand}   Dealer shows: {table.dealer.get_up_card()}")
                action = input("(h)it, (s)tand, s(p)lit: ").strip()
                if action == "h":
                    print(f"You draw {table.hit(you, hand)} -> {hand}")
                elif action == "s":
                    table.stand(hand)
                elif action == "p":
                    if not table.split(you, hand):
                        print("Can't split that hand")
                else:
                    print("Unknown action")

            for bot in [p for p in table.seated() if p.is_bot]:
                while table.bot_step(bot):
                    pass
                print(f"{bot.name}: {' | '.join(str(h) for h in bot.hands)}")

            if table.dealer_should_play():
                while table.dealer_step():
                    print(f"Dealer: {table.dealer}")
            else:
                print("Every hand is settled, dealer doesn't play")

        table.settle()
        print(f"\nDealer final: {table.dealer}")
        for player in table.seated():
            for hand in player.hands:
                print(f"  {player.name}: {hand} -> {hand.outcome}")

        if table.end_round():
            print("Cut card reached, shoe reshuffled")
        if you not in table.players:
            print("You're broke and leave the table")

    print(f"\nFinal: {you}  results {you.results}  history {you.bankroll_history}")
