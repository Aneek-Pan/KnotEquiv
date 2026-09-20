from knot.structure import Knot

def crossing_count(knot: Knot) -> int:
    """
    Number of crossings in this specific diagram. NOT the knot's true
    minimal crossing number — a diagram can have extra crossings from
    un-simplified R1/R2 moves. Only meaningful as "crossings in this
    exact Gauss code," useful for tracking diagram complexity during
    a move sequence, not for comparing different diagrams of the same
    knot type.
    """
    return len(knot.seq) // 2


def writhe(knot: Knot) -> int:
    """
    Sum of all crossing signs. NOT a true knot invariant — it changes
    under R1 (each kink shifts writhe by +-1) and is only preserved
    under R2 and R3. Useful as a diagram-level sanity check (e.g.
    tracking how many net R1 moves have been applied), not as proof
    of equivalence or non-equivalence on its own.
    """
    seen = set()
    total = 0
    for label, ou, sign in knot.seq:
        if label in seen:
            continue
        seen.add(label)
        total += 1 if sign == '+' else -1
    return total