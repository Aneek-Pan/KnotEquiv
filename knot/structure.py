# knot/structure.py
from dataclasses import dataclass, field
from typing import List, Tuple
from collections import Counter

Token = Tuple[int, str, str]  # (label, 'O'/'U', '+'/'-')

@dataclass
class Knot:
    seq: List[Token] = field(default_factory=list)

    @staticmethod
    def from_tokens(tokens: List[Token]) -> "Knot":
        k = Knot(seq=list(tokens))
        k.validate()
        return k

    def validate(self) -> None:
        counts = Counter(t[0] for t in self.seq)
        for label, n in counts.items():
            if n != 2:
                raise ValueError(f"Crossing {label} appears {n} times, expected 2")
        for label in counts:
            passes = [t for t in self.seq if t[0] == label]
            tags = {t[1] for t in passes}
            signs = {t[2] for t in passes}
            if tags != {'O', 'U'}:
                raise ValueError(f"Crossing {label} missing O or U pass: {tags}")
            if len(signs) != 1:
                raise ValueError(f"Crossing {label} has inconsistent sign: {signs}")

    def next_label(self) -> int:
        used = {t[0] for t in self.seq}
        return max(used, default=0) + 1

    def copy(self) -> "Knot":
        return Knot(seq=list(self.seq))

    def __len__(self):
        return len(self.seq)