from typing import List, NamedTuple, Union, Tuple
from knot.structure import Knot
from moves.r1 import find_r1_sites
from moves.r2 import find_r2_removable
from moves.r3 import find_r3_sites


class AvailableMove(NamedTuple):
    kind: str  # 'R1' | 'R2' | 'R3'
    site: Union[int, Tuple[int, int], Tuple[int, int, int]]


def find_all_moves(knot: Knot) -> List[AvailableMove]:
    """
    Scan a knot and return every currently applicable move-removal site,
    tagged by type. Note this only reports *removable* R1/R2 sites (moves
    that reduce crossing number) and R3 slide sites (crossing-neutral) —
    it does not enumerate possible R1/R2 *additions*, since those are
    unbounded (a kink or poke can be inserted almost anywhere).
    """
    moves: List[AvailableMove] = []

    for i in find_r1_sites(knot):
        moves.append(AvailableMove('R1', i))

    for i, j in find_r2_removable(knot):
        moves.append(AvailableMove('R2', (i, j)))

    for site in find_r3_sites(knot):
        moves.append(AvailableMove('R3', site))

    return moves


def count_moves_by_type(knot: Knot) -> dict:
    """Convenience summary: {'R1': n1, 'R2': n2, 'R3': n3}."""
    counts = {'R1': 0, 'R2': 0, 'R3': 0}
    for move in find_all_moves(knot):
        counts[move.kind] += 1
    return counts