from typing import Dict, Set
from knot.structure import Knot

def build_interlacement_graph(knot: Knot) -> Dict[int, Set[int]]:
    """
    Build the interlacement graph on crossing labels: two labels are
    connected if their occurrences alternate around the cyclic sequence
    (a...b...a...b pattern) rather than nesting or sitting apart.
    This depends only on the crossing-label pattern, not on O/U or sign.
    """
    seq = knot.seq
    positions: Dict[int, list] = {}
    for idx, tok in enumerate(seq):
        positions.setdefault(tok[0], []).append(idx)

    labels = list(positions.keys())
    graph: Dict[int, Set[int]] = {l: set() for l in labels}

    for i in range(len(labels)):
        for j in range(i + 1, len(labels)):
            a, b = labels[i], labels[j]
            a1, a2 = positions[a]
            b1, b2 = positions[b]
            between = sum(1 for p in (b1, b2) if a1 < p < a2)
            if between == 1:
                graph[a].add(b)
                graph[b].add(a)

    return graph

def passes_gauss_parity_check(knot: Knot) -> bool:
    """
    NECESSARY (not sufficient) condition for planar realizability:
    every crossing must be interlaced with an even number of others.
    Returns False => definitely not realizable.
    Returns True  => passes this filter, but full realizability is
                     not yet verified (needs the fuller Lovász
                     trip-matrix test, not implemented here).
    """
    graph = build_interlacement_graph(knot)
    return all(len(neighbors) % 2 == 0 for neighbors in graph.values())