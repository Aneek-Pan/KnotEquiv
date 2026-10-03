from knot.structure import Knot

def unknot() -> Knot:
    """The trivial knot: a simple closed loop with no crossings."""
    return Knot.from_tokens([])

def trefoil() -> Knot:
    """3_1, the simplest nontrivial knot. Torus knot T(2,3).
    Verified against Wikipedia's cited Gauss code "1,-2,3,-1,2,-3"
    (Gauss notation article) -- O/U alternates as you traverse,
    matching the standard alternating diagram."""
    return Knot.from_tokens([
        (1, 'O', '+'), (2, 'U', '+'), (3, 'O', '+'),
        (1, 'U', '+'), (2, 'O', '+'), (3, 'U', '+'),
    ])

def figure_eight() -> Knot:
    """4_1, the figure-eight knot. Amphichiral (equal to its own mirror).
    Verified against a SageMath/KnotInfo gauss_notation() example
    ([-1, 2, -3, 1, -4, 3, -2, 4]) for a knot independently confirmed
    to have crossing number 4 and be fully amphicheiral -- matching
    figure-eight's known properties."""
    return Knot.from_tokens([
        (1, 'U', '+'), (2, 'O', '-'), (3, 'U', '-'), (1, 'O', '+'),
        (4, 'U', '+'), (3, 'O', '-'), (2, 'U', '-'), (4, 'O', '+'),
    ])

def cinquefoil() -> Knot:
    """5_1, the cinquefoil / Solomon's seal knot. Torus knot T(2,5).
    Verified against a SageMath docstring example whose computed DT
    code ([6, 8, 10, 2, 4]) exactly matches Wikipedia's independently
    cited Dowker notation for 5_1."""
    return Knot.from_tokens([
        (1, 'O', '+'), (2, 'U', '+'), (3, 'O', '+'), (4, 'U', '+'), (5, 'O', '+'),
        (1, 'U', '+'), (2, 'O', '+'), (3, 'U', '+'), (4, 'O', '+'), (5, 'U', '+'),
    ])

SEEDS = {
    'unknot': unknot,
    'trefoil': trefoil,
    'figure_eight': figure_eight,
    'cinquefoil': cinquefoil,
}

def get_seed(name: str) -> Knot:
    """Look up a seed knot by name, returning a fresh Knot instance."""
    if name not in SEEDS:
        raise KeyError(f"Unknown seed '{name}'. Available: {list(SEEDS.keys())}")
    return SEEDS[name]()