# moves/r1.py
from typing import List, Tuple
from knot.structure import Knot
from moves.move import Move

def find_r1_sites(knot: Knot) -> List[int]:
    seq, n = knot.seq, len(knot.seq)
    return [i for i in range(n) if seq[i][0] == seq[(i + 1) % n][0]]

def apply_r1_remove(knot: Knot, i: int) -> Tuple[Knot, Move]:
    seq, n = knot.seq, len(knot.seq)
    a, b = seq[i], seq[(i + 1) % n]
    if a[0] != b[0]:
        raise ValueError(f"No R1 kink at position {i}")
    new_seq = [t for idx, t in enumerate(seq) if idx not in {i, (i + 1) % n}]
    return Knot.from_tokens(new_seq), Move('R1', 'remove', {'label': a[0], 'position': i})

def apply_r1_add(knot: Knot, i: int, sign: str = '+', order: str = 'OU') -> Tuple[Knot, Move]:
    label = knot.next_label()
    tok1, tok2 = (label, order[0], sign), (label, order[1], sign)
    seq = knot.seq
    insert_at = (i + 1) % len(seq) if seq else 0
    new_seq = seq[:insert_at] + [tok1, tok2] + seq[insert_at:]
    return Knot.from_tokens(new_seq), Move('R1', 'add', {'label': label, 'position': i, 'sign': sign})