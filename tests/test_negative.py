from knot.seeds import trefoil, figure_eight, unknot
from knot.invariants import crossing_count
from dataset.negative import generate_negative_pair, random_walk

def test_returns_correct_trace_lengths():
    result = generate_negative_pair(trefoil(), figure_eight(), num_moves=5, trials=3, seed=1)
    assert len(result['moves_a']) == 5
    assert len(result['moves_b']) == 5

def test_reproducible_with_seed():
    r1 = generate_negative_pair(trefoil(), figure_eight(), num_moves=8, trials=5, seed=42)
    r2 = generate_negative_pair(trefoil(), figure_eight(), num_moves=8, trials=5, seed=42)
    assert r1['knot_a_end'].seq == r2['knot_a_end'].seq
    assert r1['knot_b_end'].seq == r2['knot_b_end'].seq
    assert r1['diff'] == r2['diff']

def test_label_is_always_not_equivalent():
    result = generate_negative_pair(trefoil(), unknot(), num_moves=6, trials=4, seed=3)
    assert result['label'] == 'NOT_EQUIVALENT'

def test_more_trials_never_makes_diff_worse():
    # with a fixed seed, more trials should only ever match or beat fewer trials,
    # since it's a strict best-of search over independent attempts
    few = generate_negative_pair(trefoil(), figure_eight(), num_moves=10, trials=2, seed=99)
    many = generate_negative_pair(trefoil(), figure_eight(), num_moves=10, trials=20, seed=99)
    assert many['diff'] <= few['diff']

def test_diff_matches_actual_crossing_counts():
    result = generate_negative_pair(trefoil(), figure_eight(), num_moves=5, trials=5, seed=7)
    actual_diff = abs(crossing_count(result['knot_a_end']) - crossing_count(result['knot_b_end']))
    assert result['diff'] == actual_diff

def test_random_walk_returns_correct_trace_length():
    import random
    rng = random.Random(11)
    end, trace = random_walk(trefoil(), num_moves=7, rng=rng)
    assert len(trace) == 7