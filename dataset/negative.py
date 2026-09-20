import random
from typing import List, Tuple
from knot.structure import Knot
from knot.invariants import crossing_count
from moves.move import Move
from dataset.positive import random_move


def random_walk(start: Knot, num_moves: int, rng: random.Random) -> Tuple[Knot, List[Move]]:
    current = start
    trace: List[Move] = []
    for _ in range(num_moves):
        current, move = random_move(current, rng)
        trace.append(move)
    return current, trace


def generate_negative_pair(
    seed_a: Knot,
    seed_b: Knot,
    num_moves: int,
    trials: int = 10,
    seed: int = None,
):
    """
    seed_a and seed_b MUST already be known-distinct knot types.
    Generates `trials` independent random-walk candidates for EACH knot
    separately, then searches the full cross product of (candidate_a,
    candidate_b) pairs to find the one minimizing crossing-count
    difference. This is O(trials^2) comparisons but each is cheap.
    """
    rng = random.Random(seed)

    candidates_a = [random_walk(seed_a, num_moves, rng) for _ in range(trials)]
    candidates_b = [random_walk(seed_b, num_moves, rng) for _ in range(trials)]

    best = None
    for end_a, trace_a in candidates_a:
        for end_b, trace_b in candidates_b:
            diff = abs(crossing_count(end_a) - crossing_count(end_b))
            if best is None or diff < best['diff']:
                best = {
                    'knot_a_start': seed_a, 'knot_a_end': end_a, 'moves_a': trace_a,
                    'knot_b_start': seed_b, 'knot_b_end': end_b, 'moves_b': trace_b,
                    'diff': diff, 'label': 'NOT_EQUIVALENT',
                }
            if best['diff'] == 0:
                return best  # can't do better; early exit from both loops

    return best