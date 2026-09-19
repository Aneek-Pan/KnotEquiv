from knot.structure import Knot
from knot.validator import passes_gauss_parity_check
from moves.r3 import find_r3_sites, apply_r3

def trefoil():
    return Knot.from_tokens([
        (1, 'O', '+'), (2, 'O', '+'), (3, 'O', '+'),
        (1, 'U', '+'), (2, 'U', '+'), (3, 'U', '+'),
    ])

def test_trefoil_has_exactly_two_r3_sites():
    sites = find_r3_sites(trefoil())
    assert set(sites) == {(0, 2, 4), (1, 3, 5)}

def test_apply_r3_preserves_crossing_count_and_signs():
    k = trefoil()
    moved, move = apply_r3(k, (0, 2, 4))
    assert len(moved) == len(k)
    assert move.kind == 'R3'

    orig_signs = {t[0]: t[2] for t in k.seq}
    new_signs = {t[0]: t[2] for t in moved.seq}
    assert orig_signs == new_signs  # R3 never changes crossing signs

def test_apply_r3_twice_is_involution():
    k = trefoil()
    once, _ = apply_r3(k, (0, 2, 4))
    twice, _ = apply_r3(once, (0, 2, 4))
    assert twice.seq == k.seq

def test_site_still_detectable_after_move():
    k = trefoil()
    moved, _ = apply_r3(k, (0, 2, 4))
    sites_after = find_r3_sites(moved)
    assert (0, 2, 4) in sites_after

def test_result_still_passes_parity_check():
    k = trefoil()
    moved, _ = apply_r3(k, (0, 2, 4))
    # necessary-condition check only — not a full correctness proof,
    # but a useful consistency signal
    assert passes_gauss_parity_check(moved) is True

def test_no_sites_on_too_short_sequence():
    k = Knot.from_tokens([(1, 'O', '+'), (1, 'U', '+')])
    assert find_r3_sites(k) == []

def test_no_sites_on_two_label_code():
    k = Knot.from_tokens([
        (1, 'O', '+'), (2, 'O', '+'), (1, 'U', '+'), (2, 'U', '+'),
    ])
    assert find_r3_sites(k) == []  # needs 3 distinct labels, only 2 present