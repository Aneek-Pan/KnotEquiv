import random
from typing import List, Tuple
from knot.structure import Knot
from moves.move import Move
from moves.r1 import find_r1_sites, apply_r1_add, apply_r1_remove
from moves.r2 import find_r2_removable, apply_r2_add_local, apply_r2_remove
from moves.r3 import find_r3_sites, apply_r3


def random_move(knot: Knot, rng: random.Random) -> Tuple[Knot, Move]:
    """
    Pick and apply one random available move on the given knot.
    Additions (R1, R2) are always offered as options since they can be
    inserted almost anywhere; removals/slides are only offered when the
    detector finds an actual applicable site.
    """
    n = len(knot.seq)
    options = ['r1_add', 'r2_add']   # r2_add is now always safe, even for n=0
    if find_r1_sites(knot):
        options.append('r1_remove')
    if find_r2_removable(knot):
        options.append('r2_remove')
    if find_r3_sites(knot):
        options.append('r3')

    choice = rng.choice(options)

    if choice == 'r1_add':
        i = rng.randrange(n) if n > 0 else 0
        sign = rng.choice(['+', '-'])
        order = rng.choice(['OU', 'UO'])
        return apply_r1_add(knot, i, sign=sign, order=order)

    if choice == 'r1_remove':
        i = rng.choice(find_r1_sites(knot))
        return apply_r1_remove(knot, i)

    if choice == 'r2_add':
        i = rng.randrange(n) if n > 0 else 0
        sign_m = rng.choice(['+', '-'])
        order = rng.choice(['OU', 'UO'])
        return apply_r2_add_local(knot, i, sign_m=sign_m, order=order)

    if choice == 'r2_remove':
        i, j = rng.choice(find_r2_removable(knot))
        return apply_r2_remove(knot, i, j)

    if choice == 'r3':
        site = rng.choice(find_r3_sites(knot))
        return apply_r3(knot, site)

    raise RuntimeError(f"Unhandled move choice: {choice}")


def generate_positive_pair(
    start: Knot, num_moves: int, seed: int = None
) -> Tuple[Knot, Knot, List[Move]]:
    """
    Perform a random walk of `num_moves` Reidemeister moves starting from
    `start`. Returns (start_knot, end_knot, move_trace) — a verified
    equivalence pair, since every intermediate step is a legal move.
    """
    rng = random.Random(seed)
    current = start
    trace: List[Move] = []

    for _ in range(num_moves):
        current, move = random_move(current, rng)
        trace.append(move)

    return start, current, trace