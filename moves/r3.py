from typing import List, Tuple
from knot.structure import Knot
from moves.move import Move

def find_r3_sites(knot: Knot) -> List[Tuple[int, int, int]]:
    """
    Find triangle sites for R3: three pairwise-disjoint adjacent-token
    edges (i, i+1) whose crossing-label pairs form exactly the 3 edges
    of a triangle on 3 distinct labels {a,b}, {b,c}, {a,c}.
    Returns a list of (i1, i2, i3) start-index triples.
    """
    seq = knot.seq
    n = len(seq)
    if n < 6:
        return []

    edges = []
    for i in range(n):
        a, b = seq[i], seq[(i + 1) % n]
        if a[0] != b[0]:  # skip R1 kinks; not a valid triangle edge
            edges.append((i, a[0], b[0]))

    sites, seen = [], set()
    m = len(edges)
    for x in range(m):
        for y in range(x + 1, m):
            for z in range(y + 1, m):
                e1, e2, e3 = edges[x], edges[y], edges[z]
                idxs = {e1[0], (e1[0] + 1) % n, e2[0], (e2[0] + 1) % n, e3[0], (e3[0] + 1) % n}
                if len(idxs) != 6:
                    continue
                pairs = [frozenset((e1[1], e1[2])), frozenset((e2[1], e2[2])), frozenset((e3[1], e3[2]))]
                labels = set().union(*pairs)
                if len(labels) != 3 or len(set(pairs)) != 3:
                    continue
                a, b, c = sorted(labels)
                if set(pairs) != {frozenset((a, b)), frozenset((b, c)), frozenset((a, c))}:
                    continue
                key = frozenset([e1[0], e2[0], e3[0]])
                if key in seen:
                    continue
                seen.add(key)
                sites.append((e1[0], e2[0], e3[0]))
    return sites

def apply_r3(knot: Knot, site: Tuple[int, int, int]) -> Tuple[Knot, Move]:
    """Reverse each of the three adjacent pairs at the given site, simultaneously."""
    n = len(knot.seq)
    seq = list(knot.seq)
    for i in site:
        j = (i + 1) % n
        seq[i], seq[j] = seq[j], seq[i]
    move = Move('R3', 'slide', {'positions': site})
    return Knot.from_tokens(seq), move