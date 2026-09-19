import pytest
from knot.structure import Knot
from moves.r1 import find_r1_sites, apply_r1_remove, apply_r1_add

def trefoil():
    return Knot.from_tokens([
        (1, 'O', '+'), (2, 'O', '+'), (3, 'O', '+'),
        (1, 'U', '+'), (2, 'U', '+'), (3, 'U', '+'),
    ])

def test_no_kink_sites_on_plain_trefoil():
    assert find_r1_sites(trefoil()) == []

def test_add_r1_creates_a_kink_site():
    k = trefoil()
    kinked, move = apply_r1_add(k, i=0, sign='+', order='OU')
    assert len(kinked) == len(k) + 2
    assert move.kind == 'R1'
    assert move.action == 'add'

    sites = find_r1_sites(kinked)
    assert len(sites) == 1

def test_add_then_remove_round_trips():
    k = trefoil()
    kinked, _ = apply_r1_add(k, i=0, sign='+', order='OU')
    sites = find_r1_sites(kinked)
    restored, move = apply_r1_remove(kinked, sites[0])
    assert restored.seq == k.seq
    assert move.kind == 'R1'
    assert move.action == 'remove'

def test_remove_fails_on_non_kink_position():
    k = trefoil()
    with pytest.raises(ValueError):
        apply_r1_remove(k, 0)  # positions 0,1 are different crossings

def test_add_r1_all_sign_order_combinations():
    k = trefoil()
    for sign in ('+', '-'):
        for order in ('OU', 'UO'):
            kinked, move = apply_r1_add(k, i=2, sign=sign, order=order)
            assert len(kinked) == len(k) + 2
            sites = find_r1_sites(kinked)
            assert len(sites) == 1
            restored, _ = apply_r1_remove(kinked, sites[0])
            assert restored.seq == k.seq

def test_next_label_increments_after_add():
    k = trefoil()
    kinked, move = apply_r1_add(k, i=0)
    assert move.params['label'] == 4  # trefoil uses labels 1,2,3
    assert kinked.next_label() == 5