from .card import Card

card_values = {
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'T': 10,
    'J': 10,
    'Q': 10,
    'K': 10,
    'A': 11,
}

class Hand:
    def __init__(self):
        self.cards: list[Card] = []
        self._aces: int = 0
    
    @property
    def value(self) -> Card:
        value = 0
        
        for c in self.cards:
            value += card_values[c.rank]
        
        if self._aces:
            aces = self._aces
            # if we bust and we have aces, set each ace to 1 until get back under 21
            while value > 21 and aces:
                value -= 10
                aces -= 1
                
        return value

    def push(self, card: Card) -> None:
        """
        Add new card.

        Args:
            card (Card): new card
        """
        self.cards.append(card)
        self._aces += int(card.rank == 'A')
        
    def pop(self) -> Card:
        """
        Remove the last card of the hand.

        Returns:
            Card: removed card
        """
        card = self.cards.pop()
        self._aces -= int(card.rank == 'A')
        return card

    def can_split(self) -> bool:
        """
        You can split if you have two cards of the same value (eg, a pair of sevens, 10s, or a king and a jack and so on).

        Returns:
            bool: if the hand qualifies for a split or not
        """
        return len(self.cards) == 2 and \
            card_values[self.cards[0].rank] == card_values[self.cards[1].rank]
            
    def can_double_down(self) -> bool:
        """
        You can double down when your first two cards total 9, 10, or 11.

        Returns:
            bool: if the hand qualifies for a double down or not
        """
        value = self.value
        return len(self.cards) == 2 and \
            (value == 9 or value == 10 or value == 11)
    
    def __str__(self) -> str:
        return f"Hand(cards = [{', '.join(str(c) for c in self.cards)}], value = {self.value})"
