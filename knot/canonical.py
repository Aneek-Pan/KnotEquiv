from typing import Tuple
from knot.structure import Knot, Token


def canonical_gauss_form(knot: Knot, allow_mirror: bool = False) -> Tuple[Token, ...]:
    """
    Compute a canonical representative of a knot's Gauss code, invariant
    under the symmetries that don't change the underlying diagram:
      - choice of starting point (cyclic rotation)
      - direction of traversal (sequence reversal)
      - arbitrary crossing relabeling (first-occurrence renumbering)
    If allow_mirror=True, also identifies a diagram with its mirror
    image (all crossing signs flipped) -- use this when comparing
    against a knot known to be amphichiral, or when mirror identity
    doesn't matter for the comparison at hand.

    Returns a tuple of tokens (hashable, comparable) that is identical
    for any two Knot objects representing the same diagram up to the
    symmetries above. This is diagram-level equality, NOT full isotopy
    equivalence -- it does not account for Reidemeister moves.
    """
    seq = knot.seq
    n = len(seq)
    if n == 0:
        return tuple()

    def relabel(s):
        mapping, next_id, out = {}, 1, []
        for label, ou, sign in s:
            if label not in mapping:
                mapping[label] = next_id
                next_id += 1
            out.append((mapping[label], ou, sign))
        return out

    def flip_sign(s):
        return [(l, ou, '+' if sign == '-' else '-') for l, ou, sign in s]

    base_seqs = [seq, seq[::-1]]
    if allow_mirror:
        base_seqs = base_seqs + [flip_sign(s) for s in base_seqs]

    variants = []
    for s in base_seqs:
        for i in range(n):
            rotated = s[i:] + s[:i]
            variants.append(tuple(relabel(rotated)))

    return min(variants)


def knots_equal(knot_a: Knot, knot_b: Knot, allow_mirror: bool = False) -> bool:
    """
    True iff knot_a and knot_b represent the same diagram up to
    rotation, reversal, and relabeling (and mirror, if allow_mirror).
    Diagram-level equality only -- see canonical_gauss_form's docstring.
    """
    return canonical_gauss_form(knot_a, allow_mirror) == canonical_gauss_form(knot_b, allow_mirror)