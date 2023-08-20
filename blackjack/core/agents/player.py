from typing import Optional
from enum import Enum
from blackjack.core.card import Card
from blackjack.core.chips import Chips, InvalidBetAmount
from blackjack.core.deck import Deck
from blackjack.core.hand import Hand
from .agent import Agent
from .dealer import Dealer


class ActionsEnum(Enum):
    hit = 'hit'
    stand = 'stand'
    double_down = 'double down'
    split = 'split'
    
    def __str__(self) -> str:
        return f"{self.value}"


class Player(Agent):
    def __init__(self, id: int, stack: int):
        super().__init__(name=f"Player {id}")
        self.chips = Chips(total=stack)
        self._bets: list[int] = []
        self._action_callback = None
        
    @property
    def bet(self) -> Optional[int]:
        return self._bets[self._current_hand] if self._current_hand >= 0 else None

    def reset(self) -> list[Card]:
        self._bets = []
        self._action_callback = None
        return super().reset()

    def _log_turn(self):
        super()._log_turn()
        self.log(f"Balance {self.chips.total}")
    
    def take_bet(self) -> bool:
        while True:
            try:
                bet = int(input(f"[{self.name}] Enter the bet amount (enter '0' to skip the round): "))
                if bet == 0:
                    return False
                
                self._bet(bet)
                self.new_hand()
                self._action_callback = self._on_playing_first_hand
                return True
            except ValueError:
                self.log("Value must be an integer!")
            except InvalidBetAmount as e:
                print(e)
    
    def _bet(self, amount: int) -> None:
        self.chips.bet(amount)
        self._bets.append(amount)

    def blackjack(self):
        self.chips.add(self.bet * 2.5)

    def win(self):
        self.chips.add(self.bet * 2)
        
    def tie(self):
        self.chips.add(self.bet)

    def _on_playing_first_hand(self, deck: Deck):
        if self.hand.value == 21:
            self.log("Blackjack!!")
            self.blackjack() # Dealer does not have blackjack
            self.stand()
            return
            
        possible_actions = [ActionsEnum.hit, ActionsEnum.stand]

        # If you have balance to double your initial bet, 
        # you may be able to split or double down
        if self.chips.can_bet(self.bet):
            if self.hand.can_split():
                possible_actions.append(ActionsEnum.split)

            if self.hand.can_double_down():
                possible_actions.append(ActionsEnum.double_down)
            
        action = self._ask_action(possible_actions)
            
        if action == ActionsEnum.hit:
            self.hit(deck)
            self._action_callback = self._on_playing
        elif action == ActionsEnum.stand:
            self.stand()
        elif action == ActionsEnum.split:
            self._split()
        else:
            self._double_down()

    def _split(self):
        self._hands.append(Hand())
        self._hands[-1].push(self.hand.pop())
        self._bet(self.bet)

        if self.hand.cards[0].rank == 'A':
            self._action_callback = self._on_playing_split_aces
        else:
            self._action_callback = self._on_playing_split
    
    def _double_down(self):
        self.chips.bet(self.bet)
        self._bets[self._current_hand] *= 2
        self._action_callback = self._on_playing_double_down
    
    def _on_playing(self, deck: Deck):        
        if self.hand.value > 21:
            self.log("Bust!!")
            self.stand()
            return

        possible_actions = [ActionsEnum.hit, ActionsEnum.stand]
        action = self._ask_action(possible_actions)
            
        if action == ActionsEnum.hit:
            self.hit(deck)
        else:
            self.stand()

    def _on_playing_split_aces(self, deck: Deck):        
        self.hit(deck)
        if self._current_hand == 0:
            self._current_hand = 1
        else:
            self.stand()

    def _on_playing_split(self, deck: Deck):
        self._on_playing(deck)

        if not self.playing and self._current_hand == 0:
            # play the second hand
            self._current_hand = 1
            self._action_callback = self._on_playing

    def _on_playing_double_down(self, deck: Deck):
        self.hit(deck, face_up=False)
        self.stand()
    
    def _ask_action(self, possible_actions: list[ActionsEnum]) -> ActionsEnum:
        actions_str = ', '.join([f"{i} ({a})" for i, a in enumerate(possible_actions)])
        msg = f"[{self.name}] Select your action [{actions_str}]: "
        
        while True:
            try:
                a = int(input(msg))
                if a >= 0 and a < len(possible_actions):
                    return possible_actions[a]
                else:
                    self.log("Invalid action!")
            except ValueError:
                self.log("Invalid action!")

    def check_result(self, dealer: Dealer):
        dealer_value = dealer.hand.value
        
        for i in range(len(self._hands)):
            player_value = self._hands[i].value
            if player_value > 21:
                continue

            if dealer_value > 21 or player_value > dealer_value:
                self.log(f"Win! (player = {player_value}, dealer = {dealer_value})")
                self.win()
            elif player_value == dealer_value:
                # no chips are paid out or collected
                self.log(f"Tie! (player = {player_value}, dealer = {dealer_value})")
                self.tie()
            else:
                self.log(f"Lose! (player = {player_value}, dealer = {dealer_value})")
