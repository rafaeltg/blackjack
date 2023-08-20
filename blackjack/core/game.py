from .card import Card
from .deck import Deck
from .agents import Dealer, Player

class Game:
    def __init__(self, num_players: int) -> None:
        self._deck = Deck()
        self._discard_cards: list[Card] = []
        self._players = [Player(id=i, stack=1000) for i in range(num_players)]
        self._dealer = Dealer()

    def start(self) -> None:
        while True:
            self._deck.shuffle()

            while True:                
                if self._wagering() == 0:
                    break

                self._dealing()
                
                if self._dealer_peek():
                    continue
                
                self._players_turn()
                self._dealer_turn()
                self._check_results()
                
                if len(self._deck) < (2*len(self._players) + 2):
                    self._deck.reload(self._discard_cards)
                    self._deck.shuffle()
                    self._discard_cards = []
                
            if not self._keep_playing():
                break
            
            self._deck.reload(self._discard_cards)
            self._discard_cards = []
            
    def _wagering(self):
        print("\n")

        num_players = 0
        for p in self._players:
            num_players += int(p.chips.total > 0 and p.take_bet())

        return num_players

    def _dealing(self):
        print("\n")

        for p in self._players:
            if p.playing:
                p.hit(deck=self._deck, face_up=True)
        
        self._dealer.new_hand()
        self._dealer.hit(deck=self._deck, face_up=True)

        for p in self._players:
            if p.playing:
                p.hit(deck=self._deck, face_up=True)

        self._dealer.hit(deck=self._deck, face_up=False)

    def _dealer_peek(self) -> bool:
        if not self._dealer.has_blackjack():
            return False

        self._dealer.log(f"\n\nBlackjack!! {self._dealer.hand}")
        
        for p in self._players:
            if p.has_blackjack():
                p.log(f"Blackjack!! {p.hand}")
                p.tie()

        return True
    
    def _players_turn(self):
        for p in self._players:
            print("\n")
            while p.playing:
                p.action(deck=self._deck)
    
    def _dealer_turn(self):
        print("\n")

        while self._dealer.playing:
            self._dealer.action(deck=self._deck)
    
    def _check_results(self):
        print("\n")

        for p in self._players:
            p.check_result(self._dealer)
            self._discard_cards.extend(p.reset())
                
        self._discard_cards.extend(self._dealer.reset())

    def _keep_playing(self):
        print("\n")
        while True:
            v = input(f"Keep playing? (y)es or (n)o: ").lower()
            if v == "y":
                return True
            
            if v == "n":
                print("Bye!")
                return False
            
            print("Invalid value!")

