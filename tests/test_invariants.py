from knot.seeds import unknot, trefoil, figure_eight, cinquefoil
from knot.invariants import crossing_count, writhe
from moves.r1 import apply_r1_add
from moves.r2 import apply_r2_add_local
from moves.r3 import apply_r3, find_r3_sites

def test_crossing_count_matches_seed_definitions():
    assert crossing_count(unknot()) == 0
    assert crossing_count(trefoil()) == 3
    assert crossing_count(figure_eight()) == 4
    assert crossing_count(cinquefoil()) == 5

def test_writhe_trefoil_is_three_all_positive_crossings():
    assert writhe(trefoil()) == 3

def test_writhe_figure_eight_is_zero_two_plus_two_minus():
    # figure-eight code has signs +,-,+,-  -> should cancel to 0
    assert writhe(figure_eight()) == 0

def test_writhe_unknot_is_zero():
    assert writhe(unknot()) == 0

def test_r1_add_changes_writhe_by_exactly_the_new_signs_value():
    k = trefoil()
    w_before = writhe(k)
    kinked, move = apply_r1_add(k, i=0, sign='+', order='OU')
    assert writhe(kinked) == w_before + 1

    kinked_neg, move_neg = apply_r1_add(k, i=0, sign='-', order='OU')
    assert writhe(kinked_neg) == w_before - 1

def test_r2_local_add_preserves_writhe():
    # the two new crossings always have opposite signs by construction,
    # so they should cancel and leave writhe unchanged
    k = trefoil()
    w_before = writhe(k)
    poked, _ = apply_r2_add_local(k, i=0, sign_m='+', order='OU')
    assert writhe(poked) == w_before

def test_r3_preserves_writhe():
    k = trefoil()
    w_before = writhe(k)
    site = find_r3_sites(k)[0]
    moved, _ = apply_r3(k, site)
    assert writhe(moved) == w_before

def test_r2_local_add_increases_crossing_count_by_two():
    k = trefoil()
    poked, _ = apply_r2_add_local(k, i=0, sign_m='+', order='OU')
    assert crossing_count(poked) == crossing_count(k) + 2

def test_r3_preserves_crossing_count():
    k = trefoil()
    site = find_r3_sites(k)[0]
    moved, _ = apply_r3(k, site)
    assert crossing_count(moved) == crossing_count(k)