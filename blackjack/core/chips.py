
class InvalidBetAmount(Exception):
    pass


class Chips:
    def __init__(self, total: int):
        self.total = total
        
    def add(self, amount: int) -> None:
        self.total += amount
    
    def bet(self, amount: int) -> None:
        if amount <= 0:
            raise InvalidBetAmount(f"Bet amount should be a positive value!")
        if amount > self.total:
            raise InvalidBetAmount(f"Your bet should not exceeds {self.total} chips!")
        self.total -= amount
        
    def can_bet(self, amount: int) -> bool:
        return amount <= self.total