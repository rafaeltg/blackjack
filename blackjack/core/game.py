from .action import ActionsEnum
from .deck import Deck
from .dealer import Dealer
from .player import Player


class Game:
    def __init__(self, deck: Deck, players: list[Player]) -> None:
        self._deck = deck
        self._players = players
        self._dealer = Dealer()

    def start(self) -> None:
        self._deck.shuffle()
        
        while True:
            # take bets
            for p in self._players:
                p.new_round()
                p.bet()
            
            self._deal()
            
            # check if dealer has blackjack
            
            # players turn
            for p in self._players:
                while p.playing():
                    action = p.action()
                    
                    if action == ActionsEnum.hit:
                        p.add_card(self._deck.deal())
            
            # dealer turn
            
            # check results
    
    def _deal(self) -> None:
        for p in self._players:
            if p.playing():
                p.add_card(self._deck.deal())
        
        self._dealer.add_card(self._deck.deal())
        
        for p in self._players:
            if p.playing():
                p.add_card(self._deck.deal())
        
        self._dealer.add_card(self._deck.deal())
                
        
