from typing import Optional, Callable
from blackjack.core.card import Card
from blackjack.core.hand import Hand
from blackjack.core.deck import Deck


class Agent:
    def __init__(self, name: str):
        self.name = name
        self._hands: list[Hand] = []
        self._current_hand = -1
        self._action_callback: Optional[Callable[[Deck]]] = None
    
    @property
    def playing(self) -> bool:
        return self._action_callback is not None

    @property
    def hand(self) -> Optional[Hand]:
        return self._hands[self._current_hand] if self._current_hand >= 0 else None

    def action(self, deck: Deck):
        if self._action_callback is None:
            return

        self._log_turn()
        return self._action_callback(deck)

    def has_blackjack(self) -> bool:
        return len(self._hands) == 1 and len(self.hand.cards) == 2 and self.hand.value == 21

    def new_hand(self):
        self._hands.append(Hand())
        self._current_hand += 1

    def reset(self) -> list[Card]:
        cards = []
        for h in self._hands:
            cards.extend(h.cards)

        self._hands = []
        self._current_hand = -1
        return cards

    def hit(self, deck: Deck, face_up: bool = True):
        card = deck.deal()

        if face_up:
            self.log(f"Was dealt a {card}")
        else:
            self.log("Was dealt a card facing down")

        self.hand.push(card)
    
    def stand(self):
        self._action_callback = None

    def log(self, msg: str):
        print(f"[{self.name}] {msg}")

    def _log_turn(self):
        self.log("Turn")
        self.log(f"{self.hand}")
