from .action import ActionsEnum
from .card import Card
from .hand import Hand


class Dealer:
    def __init__(self) -> None:
        self._hand = Hand()
    
    def add_card(self, card: Card) -> None:
        self._hand.add_card(card)
    
    def action(self) -> ActionsEnum:
        if self._blackjack():
            return ActionsEnum.stand

        possible_actions = [
            ActionsEnum.hit,
            ActionsEnum.stand,
        ]
        
        if self._can_split():
            possible_actions.append(ActionsEnum.split)

        while True:
            try:
                a = int(input(f"Select your action [{', '.join(str(a) for a in possible_actions)}]: "))
                action = ActionsEnum(a)
            except ValueError:
                print("Invalid action!")    
            else:
                break
        
        return action
    
    def _blackjack(self) -> bool:
        return len(self._hands) > 0 and \
            self._hands[self._current_hand].blackjack()

    def _can_split(self) -> bool:
        return len(self._hands) == 1 and \
            self._hands[self._current_hand].can_split()
