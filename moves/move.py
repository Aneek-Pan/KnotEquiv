# moves/move.py
from dataclasses import dataclass, field

@dataclass
class Move:
    kind: str      # 'R1' | 'R2' | 'R3'
    action: str    # 'add' | 'remove'
    params: dict = field(default_factory=dict)

    def __repr__(self):
        return f"{self.kind}-{self.action}({self.params})"