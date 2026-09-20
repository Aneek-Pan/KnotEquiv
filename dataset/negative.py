import random
from typing import List, Tuple
from knot.structure import Knot
from knot.invariants import crossing_count
from moves.move import Move
from dataset.positive import random_move


def random_walk(start: Knot, num_moves: int, rng: random.Random) -> Tuple[Knot, List[Move]]:
    """Apply num_moves random Reidemeister moves to a single knot, independently."""
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
    Generate a negative (non-equivalent) pair. seed_a and seed_b MUST be
    two knots already known to be genuinely different knot types (e.g.
    two different named seeds from knot/seeds.py) — non-equivalence here
    rests on that external fact, NOT on any invariant computed in this
    codebase. Reidemeister moves never change knot type, so no move
    sequence applied here can ever make the two equivalent, regardless
    of how close their diagrams end up looking.

    Runs `trials` independent attempts, each performing an independent
    random walk of `num_moves` on each knot, and keeps whichever trial
    minimizes the crossing-count difference between the two results.
    This is a coarse, cheap closeness metric — matched crossing count
    does NOT imply the diagrams look alike, only that they're similarly
    complex. Good enough as a first version; can be swapped for a
    richer structural metric later if needed.

    Returns a dict with both knots' start/end states, move traces, and
    the final crossing-count difference achieved.
    """
    rng = random.Random(seed)
    best = None

    for _ in range(trials):
        end_a, trace_a = random_walk(seed_a, num_moves, rng)
        end_b, trace_b = random_walk(seed_b, num_moves, rng)
        diff = abs(crossing_count(end_a) - crossing_count(end_b))

        if best is None or diff < best['diff']:
            best = {
                'knot_a_start': seed_a,
                'knot_a_end': end_a,
                'moves_a': trace_a,
                'knot_b_start': seed_b,
                'knot_b_end': end_b,
                'moves_b': trace_b,
                'diff': diff,
                'label': 'NOT_EQUIVALENT',
            }

        if best['diff'] == 0:
            break  # can't do better than an exact crossing-count match

    return best