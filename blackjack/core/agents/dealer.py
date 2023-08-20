from blackjack.core.card import Card
from blackjack.core.deck import Deck
from .agent import Agent


class Dealer(Agent):
    def __init__(self):
        super().__init__(name="Dealer")
        self._action_callback = self._on_playing

    def reset(self) -> list[Card]:
        self._action_callback = self._on_playing
        return super().reset()
    
    def _on_playing(self, deck: Deck):
        if self.hand.value < 17:
            self.hit(deck)
        else:
            if self.hand.value > 21:
                self.log("Bust!!")

            self.stand()
