import math
from typing import List, Dict, NamedTuple
from knot.structure import Knot

class ChordPoint(NamedTuple):
    x: float
    y: float

class Chord(NamedTuple):
    label: int
    sign: str
    p_over: ChordPoint   # position of the 'O' occurrence on the circle
    p_under: ChordPoint  # position of the 'U' occurrence on the circle


def compute_chord_layout(knot: Knot, radius: float = 1.0) -> List[Chord]:
    """
    Place each token in the Gauss code sequence at an equally spaced
    point around a circle, then pair up each label's O and U occurrence
    into a Chord. Pure geometry, no drawing — fully unit-testable.
    """
    seq = knot.seq
    n = len(seq)
    if n == 0:
        return []

    positions: Dict[int, ChordPoint] = {}
    ou_positions: Dict[int, Dict[str, ChordPoint]] = {}

    for idx, (label, ou, sign) in enumerate(seq):
        angle = 2 * math.pi * idx / n
        point = ChordPoint(radius * math.cos(angle), radius * math.sin(angle))
        ou_positions.setdefault(label, {})[ou] = point

    chords = []
    seen = set()
    for label, ou, sign in seq:
        if label in seen:
            continue
        seen.add(label)
        pts = ou_positions[label]
        chords.append(Chord(label=label, sign=sign, p_over=pts['O'], p_under=pts['U']))

    return chords


def plot_knot(knot: Knot, title: str = "", save_path: str = None, ax=None):
    """
    Draw the chord diagram for a knot using matplotlib.
    If save_path is given, saves to file instead of (or as well as) showing.
    """
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches

    chords = compute_chord_layout(knot)
    n = len(knot.seq)

    created_fig = ax is None
    if created_fig:
        fig, ax = plt.subplots(figsize=(6, 6))

    circle = patches.Circle((0, 0), 1.0, fill=False, color='lightgray', linewidth=1)
    ax.add_patch(circle)

    for label, ou, sign in knot.seq:
        pass  # points are implicitly drawn via chords below

    for chord in chords:
        color = 'tab:blue' if chord.sign == '+' else 'tab:red'
        ax.plot(
            [chord.p_over.x, chord.p_under.x],
            [chord.p_over.y, chord.p_under.y],
            color=color, linewidth=1.5, alpha=0.8
        )
        ax.plot(*chord.p_over, 'o', color='black', markersize=4)
        ax.plot(*chord.p_under, 's', color='black', markersize=4)

        # place label near the O endpoint, offset slightly outward,
        # instead of at the midpoint (avoids collisions when chords
        # pass through a shared center point)
        label_x = chord.p_over.x * 0.85
        label_y = chord.p_over.y * 0.85
        ax.annotate(str(chord.label), (label_x, label_y), fontsize=8, alpha=0.8,
                    ha='center', va='center')

    ax.set_xlim(-1.3, 1.3)
    ax.set_ylim(-1.3, 1.3)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(title or f"Chord diagram ({n // 2} crossings)")

    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches='tight')
    if created_fig:
        return ax.figure