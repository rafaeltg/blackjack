import pytest
from blackjack.core.card import Card
from blackjack.core.hand import Hand

class TestHand(object):
    def test_value(self) -> None:
        h = Hand()
        h.push(Card("Spades", "2"))
        h.push(Card("Hearts", "7"))
        assert h.value == 9
        
    def test_value_with_aces_not_bust(self) -> None:
        h = Hand()
        h.push(Card("Spades", "A"))
        h.push(Card("Hearts", "7"))
        assert h.value == 18
        
    def test_value_with_aces_bust(self) -> None:
        h = Hand()
        h.push(Card("Spades", "A"))
        h.push(Card("Hearts", "7"))
        h.push(Card("Hearts", "8"))
        assert h.value == 16

    def test_can_split(self) -> None:
        cases = [
            ([Card("Spades", "A")], False),
            ([Card("Spades", "A"), Card("Spades", "2")], False),
            ([Card("Spades", "A"), Card("Spades", "A")], True),
            ([Card("Spades", "J"), Card("Spades", "Q")], True),
            ([Card("Spades", "5"), Card("Spades", "5")], True),
        ]
        
        for tc in cases:
            h = Hand()
            for c in tc[0]:
                h.push(c)
            assert h.can_split() == tc[1]
    
    def test_can_double_down(self) -> None:
        cases = [
            ([Card("Spades", "A")], False),
            ([Card("Spades", "A"), Card("Spades", "2")], False),
            ([Card("Spades", "7"), Card("Spades", "2")], True),
            ([Card("Spades", "5"), Card("Spades", "5")], True),
            ([Card("Spades", "7"), Card("Spades", "4")], True),
        ]
        
        for tc in cases:
            h = Hand()
            for c in tc[0]:
                h.push(c)
            assert h.can_double_down() == tc[1]