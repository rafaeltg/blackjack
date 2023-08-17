
class InvalidBetAmount(Exception):
    def __init__(self, max_amount):
        self.max_amount = max_amount
        super().__init__(f"Your bet should not exceeds {max_amount} chips!")


class Chips:
    def __init__(self, total: int):
        self.total = total
        
    def add(self, amount: int) -> None:
        self.total += amount
    
    def bet(self, amount: int) -> None:
        if amount > self.total:
            raise InvalidBetAmount(self.total)
        self.total -= amount