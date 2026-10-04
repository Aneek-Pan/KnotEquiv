from knot.structure import Knot

def unknot() -> Knot:
    """The trivial knot: a simple closed loop with no crossings."""
    return Knot.from_tokens([])

def trefoil() -> Knot:
    """3_1. Verified against Wikipedia's cited Gauss code "1,-2,3,-1,2,-3"."""
    return Knot.from_tokens([
        (1, 'O', '+'), (2, 'U', '+'), (3, 'O', '+'),
        (1, 'U', '+'), (2, 'O', '+'), (3, 'U', '+'),
    ])

def figure_eight() -> Knot:
    """4_1. Verified against a SageMath/KnotInfo gauss_notation() example,
    and independently cross-validated against SnapPy's own computed
    PD code + overstrands() + crossing signs (exact canonical match,
    no mirror needed -- see tests/test_canonical.py)."""
    return Knot.from_tokens([
        (1, 'U', '+'), (2, 'O', '-'), (3, 'U', '-'), (1, 'O', '+'),
        (4, 'U', '+'), (3, 'O', '-'), (2, 'U', '-'), (4, 'O', '+'),
    ])

def cinquefoil() -> Knot:
    """5_1. Verified against a SageMath docstring example whose computed
    DT code matches Wikipedia's independently cited Dowker notation."""
    return Knot.from_tokens([
        (1, 'O', '+'), (2, 'U', '+'), (3, 'O', '+'), (4, 'U', '+'), (5, 'O', '+'),
        (1, 'U', '+'), (2, 'O', '+'), (3, 'U', '+'), (4, 'O', '+'), (5, 'U', '+'),
    ])

def five_two() -> Knot:
    """5_2. Generated via SnapPy (snappy.Link('5_2')), using the method
    cross-validated against figure-eight. DT code magnitude set
    {2,4,6,8,10} independently confirmed against Wikipedia's cited
    Dowker notation for 5_2."""
    return Knot.from_tokens([
        (1, 'U', '+'), (2, 'O', '+'), (5, 'U', '+'), (4, 'O', '+'), (3, 'U', '+'),
        (1, 'O', '+'), (2, 'U', '+'), (3, 'O', '+'), (4, 'U', '+'), (5, 'O', '+'),
    ])

def six_one() -> Knot:
    """6_1. Generated via SnapPy. NOTE: unlike the other new seeds, this
    one rests on the SnapPy method alone -- no independent second-source
    DT code citation was found during research to cross-check against."""
    return Knot.from_tokens([
        (1, 'U', '-'), (6, 'O', '+'), (5, 'U', '+'), (4, 'O', '+'), (3, 'U', '+'),
        (1, 'O', '-'), (2, 'U', '-'), (3, 'O', '+'), (4, 'U', '+'), (5, 'O', '+'),
        (6, 'U', '+'), (2, 'O', '-'),
    ])

def six_two() -> Knot:
    """6_2. Generated via SnapPy. DT code magnitude set {2,4,6,8,10,12}
    independently confirmed against Wikipedia's cited Dowker notation."""
    return Knot.from_tokens([
        (1, 'U', '+'), (2, 'O', '+'), (3, 'U', '+'), (4, 'O', '+'), (5, 'U', '-'),
        (6, 'O', '-'), (4, 'U', '+'), (1, 'O', '+'), (2, 'U', '+'), (3, 'O', '+'),
        (6, 'U', '-'), (5, 'O', '-'),
    ])

def six_three() -> Knot:
    """6_3. Generated via SnapPy. DT code magnitude set {2,4,6,8,10,12}
    independently confirmed against Wikipedia's cited Dowker notation."""
    return Knot.from_tokens([
        (1, 'U', '-'), (5, 'O', '-'), (6, 'U', '-'), (1, 'O', '-'), (2, 'U', '+'),
        (3, 'O', '+'), (4, 'U', '+'), (2, 'O', '+'), (5, 'U', '-'), (6, 'O', '-'),
        (3, 'U', '+'), (4, 'O', '+'),
    ])

SEEDS = {
    'unknot': unknot,
    'trefoil': trefoil,
    'figure_eight': figure_eight,
    'cinquefoil': cinquefoil,
    'three_two': five_two,
    'six_one': six_one,
    'six_two': six_two,
    'six_three': six_three,
}

def get_seed(name: str) -> Knot:
    """Look up a seed knot by name, returning a fresh Knot instance."""
    if name not in SEEDS:
        raise KeyError(f"Unknown seed '{name}'. Available: {list(SEEDS.keys())}")
    return SEEDS[name]()