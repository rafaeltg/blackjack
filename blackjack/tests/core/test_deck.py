import pytest
from blackjack.core.deck import Deck

class TestDeck(object):
    def test_len(self) -> None:
        d = Deck()
        assert len(d) == 52
        
    def test_deal(self) -> None:
        d = Deck()
        card = d.deal()
        assert card
        assert len(d) == 51
        
    def test_deal_52_cards(self) -> None:
        d = Deck()
        for i in range(52):
            c = d.deal()
            assert c
        
        c = d.deal()
        assert c is None
        assert len(d) == 0
