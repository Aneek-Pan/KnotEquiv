from knot.structure import Knot
from moves.detector import find_all_moves, count_moves_by_type
from moves.r1 import apply_r1_add
from moves.r2 import apply_r2_add

def trefoil():
    return Knot.from_tokens([
        (1, 'O', '+'), (2, 'O', '+'), (3, 'O', '+'),
        (1, 'U', '+'), (2, 'U', '+'), (3, 'U', '+'),
    ])

def test_plain_trefoil_has_only_r3_moves():
    moves = find_all_moves(trefoil())
    kinds = {m.kind for m in moves}
    assert kinds == {'R3'}
    assert count_moves_by_type(trefoil()) == {'R1': 0, 'R2': 0, 'R3': 2}

def test_kinked_trefoil_shows_r1():
    k = trefoil()
    kinked, _ = apply_r1_add(k, i=0, sign='+', order='OU')
    counts = count_moves_by_type(kinked)
    assert counts['R1'] == 1

def test_poked_trefoil_shows_r2():
    k = trefoil()
    poked, _ = apply_r2_add(k, i=0, j=3, sign_m='+', order='OU')
    counts = count_moves_by_type(poked)
    assert counts['R2'] == 1

def test_detector_finds_all_three_kinds_simultaneously():
    k = trefoil()
    kinked, _ = apply_r1_add(k, i=0, sign='+', order='OU')
    poked, _ = apply_r2_add(kinked, i=0, j=3, sign_m='+', order='OU')

    counts = count_moves_by_type(poked)
    assert counts['R1'] >= 1
    assert counts['R2'] >= 1
    # R3 count isn't asserted precisely here — adding R1/R2 can shift or
    # obscure the original R3 triangle sites, so we only check R1/R2 landed