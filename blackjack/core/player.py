from .action import ActionsEnum
from .card import Card
from .chips import Chips, InvalidBetAmount
from .hand import Hand


class Player:
    def __init__(self, stack: int):
        self._hands: list[Hand] = [Hand()]
        self._hands_bet: list[int] = [0]
        self._current_hand = 0
        self.chips = Chips(total=stack)
    
    def add_card(self, card: Card) -> None:
        self._hands[self._current_hand].add_card(card)
    
    def bet(self) -> None:
        while True:
            try:
                bet = int(input('Enter the bet amount (enter "0" to skip the round): '))
                if bet > 0:
                    self._new_round()
                    self._bet(bet)
            except ValueError:
                print("The bet value must be an integer!")
            except InvalidBetAmount as e:
                print(e)
            else:
                break
    
    def _bet(self, amount: int) -> None:
        self.chips.bet(amount=amount)
        self._hands_bet.append(amount)
        
    def _new_round(self) -> None:
        self._hands = [Hand()]
        self._hands_bet = []
        self._current_hand = 0
        
    def action(self) -> ActionsEnum:
        if self._blackjack():
            return ActionsEnum.stand

        possible_actions = [
            ActionsEnum.hit,
            ActionsEnum.stand,
        ]
        
        if self._can_double_down():
            possible_actions.append(ActionsEnum.double_down)

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
            
        if action == ActionsEnum.split:
            new_hand = Hand()
            new_hand.add_card(self._hands[self._current_hand].cards.pop())
            self._hands.append(new_hand)
            self._bet(self._hands_bet[self._current_hand])
        elif action == ActionsEnum.double_down:
            self.chips.bet(amount=self._hands_bet[self._current_hand])
            self._hands_bet[self._current_hand] *= 2            
        
        return action
    
    def playing(self) -> bool:
        return True
    
    def _blackjack(self) -> bool:
        return self._hands[self._current_hand].blackjack()

    def _can_split(self) -> bool:
        """
        If the hand qualifies for split and your chips balance is sufficient for the additional bet, you can split.

        Returns:
            bool: if you can split or not
        """
        return len(self._hands) == 1 and \
            self._hands[self._current_hand].can_split() and \
            self.chips.total >= self._hands_bet[self._current_hand]
            
    def _can_double_down(self) -> bool:
        """
        If the hand qualifies for split and your chips balance is sufficient for the additional bet, you can split.

        Returns:
            bool: if you can split or not
        """
        return len(self._hands) == 1 and \
            self._hands[self._current_hand].can_double_down() and \
            self.chips.total >= self._hands_bet[self._current_hand]
