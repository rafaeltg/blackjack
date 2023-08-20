import pytest
from blackjack.core.chips import Chips, InvalidBetAmount

class TestChips(object):
    def test_add(self) -> None:
        c = Chips(total=10)
        c.add(1)
        assert c.total == 11
        
    def test_bet_zero(self) -> None:
        c = Chips(total=10)
        with pytest.raises(InvalidBetAmount):
            c.bet(0)
    
    def test_bet_negative(self) -> None:
        c = Chips(total=10)
        with pytest.raises(InvalidBetAmount):
            c.bet(-1)
            
    def test_bet_positive(self) -> None:
        c = Chips(total=10)
        c.bet(1)
        assert c.total == 9
        
    def test_can_bet(self) -> None:
        c = Chips(total=10)
        assert c.can_bet(9)
        assert not c.can_bet(11)
