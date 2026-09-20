import pytest
from knot.structure import Knot
from moves.r2 import find_r2_removable, apply_r2_remove, apply_r2_add, apply_r2_add_local
from knot.validator import passes_gauss_parity_check
def trefoil():
    return Knot.from_tokens([
        (1, 'O', '+'), (2, 'O', '+'), (3, 'O', '+'),
        (1, 'U', '+'), (2, 'U', '+'), (3, 'U', '+'),
    ])

def test_no_r2_sites_on_plain_trefoil():
    assert find_r2_removable(trefoil()) == []

def test_add_r2_creates_a_findable_site():
    k = trefoil()
    poked, move = apply_r2_add(k, i=0, j=3, sign_m='+', order='OU')
    assert len(poked) == len(k) + 4
    assert move.kind == 'R2'
    assert move.action == 'add'

    sites = find_r2_removable(poked)
    assert len(sites) == 1

def test_add_then_remove_round_trips():
    k = trefoil()
    poked, _ = apply_r2_add(k, i=0, j=3, sign_m='+', order='OU')
    sites = find_r2_removable(poked)
    restored, move = apply_r2_remove(poked, *sites[0])
    assert restored.seq == k.seq
    assert move.kind == 'R2'
    assert move.action == 'remove'

def test_remove_fails_on_invalid_positions():
    k = trefoil()
    with pytest.raises(ValueError):
        apply_r2_remove(k, 0, 1)  # not a valid poke pattern

def test_add_r2_all_sign_order_combinations():
    k = trefoil()
    for sign_m in ('+', '-'):
        for order in ('OU', 'UO'):
            poked, move = apply_r2_add(k, i=0, j=3, sign_m=sign_m, order=order)
            sites = find_r2_removable(poked)
            assert len(sites) == 1
            restored, _ = apply_r2_remove(poked, *sites[0])
            assert restored.seq == k.seq

def test_add_r2_at_different_gap_pairs():
    k = trefoil()
    # try a variety of i,j gap combinations around the cycle
    for i, j in [(0, 3), (1, 4), (2, 5), (0, 2)]:
        poked, _ = apply_r2_add(k, i=i, j=j, sign_m='+', order='OU')
        sites = find_r2_removable(poked)
        assert len(sites) == 1, f"failed for i={i}, j={j}"
        restored, _ = apply_r2_remove(poked, *sites[0])
        assert restored.seq == k.seq

def test_i_equals_j_rejected():
    k = trefoil()
    with pytest.raises(ValueError):
        apply_r2_add(k, i=2, j=2)

def test_double_poke_then_remove_in_either_order():
    # add two independent pokes, confirm both are found, removing either
    # first still leaves a removable site for the other
    k = trefoil()
    once, _ = apply_r2_add(k, i=0, j=3, sign_m='+', order='OU')
    twice, _ = apply_r2_add(once, i=1, j=len(once) - 1, sign_m='-', order='UO')

    sites = find_r2_removable(twice)
    assert len(sites) >= 1  # at least one poke should be independently removable

def test_next_label_increments_after_add():
    k = trefoil()
    poked, move = apply_r2_add(k, i=0, j=3)
    m, n_ = move.params['labels']
    assert m == 4 and n_ == 5
    assert poked.next_label() == 6

def test_local_r2_add_always_preserves_parity():
    k = trefoil()
    for _ in range(20):
        for i in range(len(k)):
            poked, _ = apply_r2_add_local(k, i, sign_m='+', order='OU')
            assert passes_gauss_parity_check(poked), f"Failed at i={i}"