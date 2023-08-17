import random
from .card import Card, suits, ranks

class Deck:
    def __init__(self) -> None:
      self._cards: list[Card] = []
      for suit in suits:
        for rank in ranks:
            self._cards.append(Card(suit, rank))
            
    def shuffle(self) -> None:
        random.shuffle(self._cards)
    
    def deal(self) -> Card:
        card = self._cards.pop()
        return card
