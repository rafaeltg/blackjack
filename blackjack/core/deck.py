import random
from typing import Optional
from .card import Card, suits, ranks

class Deck:
    def __init__(self) -> None:
      self._cards: list[Card] = []      
      for suit in suits:
        for rank in ranks:
            self._cards.append(Card(suit, rank))
    
    def __len__(self) -> int:
        return len(self._cards)

    def shuffle(self):
        random.shuffle(self._cards)

    def deal(self) -> Optional[Card]:
        return self._cards.pop() if len(self._cards) > 0 else None
    
    def reload(self, cards: list[Card]):
        self._cards.extend(cards)
        
