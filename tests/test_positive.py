from knot.seeds import trefoil, unknot
from knot.validator import passes_gauss_parity_check
from dataset.positive import generate_positive_pair, random_move

MOVE_DELTA = {'R1': 2, 'R2': 4, 'R3': 0}  # crossing-token count change per add; remove is negative

def test_generate_positive_pair_returns_correct_trace_length():
    start, end, trace = generate_positive_pair(trefoil(), num_moves=10, seed=42)
    assert len(trace) == 10

def test_generate_positive_pair_is_reproducible_with_seed():
    _, end1, trace1 = generate_positive_pair(trefoil(), num_moves=15, seed=7)
    _, end2, trace2 = generate_positive_pair(trefoil(), num_moves=15, seed=7)
    assert end1.seq == end2.seq
    assert [str(m) for m in trace1] == [str(m) for m in trace2]

def test_different_seeds_can_diverge():
    _, end1, _ = generate_positive_pair(trefoil(), num_moves=15, seed=1)
    _, end2, _ = generate_positive_pair(trefoil(), num_moves=15, seed=2)
    # not a hard guarantee they must differ, but overwhelmingly likely;
    # flags a bug if the RNG seed isn't actually being used
    assert end1.seq != end2.seq

def test_every_intermediate_knot_passes_parity_check():
    rng_seed = 99
    current = trefoil()
    import random
    rng = random.Random(rng_seed)
    for _ in range(20):
        current, move = random_move(current, rng)
        assert passes_gauss_parity_check(current), f"Failed after move {move}"

def test_crossing_count_matches_expected_deltas():
    start = trefoil()
    start_len = len(start)
    _, end, trace = generate_positive_pair(start, num_moves=25, seed=123)

    expected_len = start_len
    for move in trace:
        delta = MOVE_DELTA[move.kind]
        if move.action == 'remove':
            expected_len -= delta
        elif move.action == 'add':
            expected_len += delta
        # R3 'slide' has delta 0, no-op either way

    assert len(end) == expected_len

def test_works_starting_from_unknot():
    start, end, trace = generate_positive_pair(unknot(), num_moves=10, seed=5)
    assert len(trace) == 10
    assert passes_gauss_parity_check(end)