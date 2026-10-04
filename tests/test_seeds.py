import pytest
from knot.seeds import unknot, trefoil, figure_eight, cinquefoil, get_seed, five_two, six_one, six_two, six_three, SEEDS
from knot.validator import passes_gauss_parity_check

def test_unknot_has_zero_crossings():
    assert len(unknot()) == 0

def test_trefoil_has_three_crossings():
    assert len(trefoil()) == 6  # 3 crossings * 2 tokens each

def test_figure_eight_has_four_crossings():
    assert len(figure_eight()) == 8

def test_cinquefoil_has_five_crossings():
    assert len(cinquefoil()) == 10

def test_all_named_seeds_pass_parity_check():
    for name, factory in SEEDS.items():
        knot = factory()
        assert passes_gauss_parity_check(knot), f"{name} failed parity check"

def test_get_seed_returns_correct_knot():
    k = get_seed('trefoil')
    assert len(k) == 6

def test_get_seed_returns_fresh_copy_each_time():
    a = get_seed('trefoil')
    b = get_seed('trefoil')
    a.seq.append((99, 'O', '+'))  # mutate one
    assert len(b.seq) == 6  # other must be unaffected

def test_get_seed_unknown_name_raises():
    with pytest.raises(KeyError):
        get_seed('not_a_real_knot') 

def test_three_two_has_five_crossings():
    assert len(five_two()) == 10

def test_six_one_has_six_crossings():
    assert len(six_one()) == 12

def test_six_two_has_six_crossings():
    assert len(six_two()) == 12

def test_six_three_has_six_crossings():
    assert len(six_three()) == 12