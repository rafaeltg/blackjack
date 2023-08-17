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
        self.value: int = 0
        self.aces: int = 0
    
    def add_card(self, card: Card) -> None:
        self.cards.append(card)
        self.value += card_values[card.rank]
        self.aces += int(card.rank == 'A')

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1
    
    def blackjack(self) -> bool:
        return self.value == 21
    
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
        You can double down if you have two cards of any value.

        Returns:
            bool: if the hand qualifies for a split or not
        """
        return len(self.cards) == 2 and \
            card_values[self.cards[0].rank] == card_values[self.cards[1].rank]
    
    def __str__(self) -> str:
        return f"Hand(cards = [{', '.join(str(c) for c in self.cards)}], value = {self.value})"