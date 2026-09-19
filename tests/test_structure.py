import pytest
from knot.structure import Knot

def test_valid_trefoil():
    k = Knot.from_tokens([
        (1, 'O', '+'), (2, 'O', '+'), (3, 'O', '+'),
        (1, 'U', '+'), (2, 'U', '+'), (3, 'U', '+'),
    ])
    assert len(k) == 6

def test_next_label():
    k = Knot.from_tokens([
        (1, 'O', '+'), (2, 'O', '+'),
        (1, 'U', '+'), (2, 'U', '+'),
    ])
    assert k.next_label() == 3

def test_rejects_missing_pass():
    with pytest.raises(ValueError):
        Knot.from_tokens([(1, 'O', '+'), (2, 'O', '+'), (1, 'U', '+')])

def test_rejects_triplicate_label():
    with pytest.raises(ValueError):
        Knot.from_tokens([
            (1, 'O', '+'), (1, 'U', '+'), (1, 'O', '+'),
            (2, 'O', '+'), (2, 'U', '+'),
        ])

def test_rejects_inconsistent_sign():
    with pytest.raises(ValueError):
        Knot.from_tokens([(1, 'O', '+'), (1, 'U', '-')])