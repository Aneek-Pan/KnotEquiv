# moves/r2.py
from typing import List, Tuple
from knot.structure import Knot
from moves.move import Move

def find_r2_removable(knot: Knot) -> List[Tuple[int, int]]:
    """Positions (i, j) where seq[i],seq[i+1] and seq[j],seq[j+1] form
    a removable R2 poke: same tag + opposite sign at each pair, with
    labels reversed between the two pairs."""
    seq, n = knot.seq, len(knot.seq)
    seen, results = set(), []
    for i in range(n):
        a, b = seq[i], seq[(i + 1) % n]
        if a[0] == b[0] or a[1] != b[1] or a[2] == b[2]:
            continue
        other_tag = 'U' if a[1] == 'O' else 'O'
        for j in range(n):
            if j == i:
                continue
            c, d = seq[j], seq[(j + 1) % n]
            if c[0] == b[0] and d[0] == a[0] and c[1] == other_tag and d[1] == other_tag:
                if len({i, (i + 1) % n, j, (j + 1) % n}) != 4:
                    continue  # overlapping positions, degenerate case
                key = frozenset({i, j})
                if key not in seen:
                    seen.add(key)
                    results.append(tuple(sorted((i, j))))
    return results

def apply_r2_remove(knot: Knot, i: int, j: int) -> Tuple[Knot, Move]:
    seq, n = knot.seq, len(knot.seq)
    i2, j2 = (i + 1) % n, (j + 1) % n
    positions = {i, i2, j, j2}
    if len(positions) != 4:
        raise ValueError("Overlapping positions; not a valid R2 site")
    a, b, c, d = seq[i], seq[i2], seq[j], seq[j2]
    valid = (c[0] == b[0] and d[0] == a[0] and a[1] == b[1] and c[1] == d[1]
             and a[1] != c[1] and a[2] != b[2])
    if not valid:
        raise ValueError(f"Positions {i},{j} do not form a valid R2 poke")
    new_seq = [t for idx, t in enumerate(seq) if idx not in positions]
    move = Move('R2', 'remove', {'labels': (a[0], b[0]), 'positions': (i, j)})
    return Knot.from_tokens(new_seq), move

def apply_r2_add(knot: Knot, i: int, j: int, sign_m: str = '+', order: str = 'OU') -> Tuple[Knot, Move]:
    """Insert a poke: gap i gets (m,O),(n,O); gap j gets (n,U),(m,U) —
    reversed label order, opposite crossing signs (a real geometric
    constraint, not a convention)."""
    if i == j:
        raise ValueError("i and j must be distinct insertion gaps")
    m = knot.next_label()
    n_ = m + 1
    sign_n = '-' if sign_m == '+' else '+'
    tagA, tagB = order[0], order[1]
    pair_first = [(m, tagA, sign_m), (n_, tagA, sign_n)]
    pair_second = [(n_, tagB, sign_n), (m, tagB, sign_m)]

    seq = knot.seq
    first_gap, second_gap = sorted([i, j])
    first_tokens = pair_first if i < j else pair_second
    second_tokens = pair_second if i < j else pair_first

    new_seq = (seq[:first_gap + 1] + first_tokens
               + seq[first_gap + 1:second_gap + 1] + second_tokens
               + seq[second_gap + 1:])
    move = Move('R2', 'add', {'labels': (m, n_), 'positions': (i, j), 'sign': sign_m})
    return Knot.from_tokens(new_seq), move

def apply_r2_add_local(knot: Knot, i: int, sign_m: str = '+', order: str = 'OU') -> Tuple[Knot, Move]:
    """
    Insert a local R2 'poke': both new crossings inserted together,
    contiguously, at a single gap. Always planar-realizable, since the
    new crossings can't interlace with anything outside the block.
    This is a restricted, always-safe form of R2 — it doesn't cover
    placing the two crossings far apart on different strands, which
    needs planar face info we don't have yet (see knot/faces.py, TBD).
    """
    m = knot.next_label()
    n_ = m + 1
    sign_n = '-' if sign_m == '+' else '+'
    tagA, tagB = order[0], order[1]
    block = [
        (m, tagA, sign_m), (n_, tagA, sign_n),
        (n_, tagB, sign_n), (m, tagB, sign_m),
    ]
    seq = knot.seq
    insert_at = (i + 1) % len(seq) if seq else 0
    new_seq = seq[:insert_at] + block + seq[insert_at:]
    move = Move('R2', 'add', {'labels': (m, n_), 'position': i, 'sign': sign_m, 'local': True})
    return Knot.from_tokens(new_seq), move