from knot.structure import Knot

def unknot() -> Knot:
    """The trivial knot: a simple closed loop with no crossings."""
    return Knot.from_tokens([])

def trefoil() -> Knot:
    """3_1, the simplest nontrivial knot. Torus knot T(2,3)."""
    return Knot.from_tokens([
        (1, 'O', '+'), (2, 'O', '+'), (3, 'O', '+'),
        (1, 'U', '+'), (2, 'U', '+'), (3, 'U', '+'),
    ])

def figure_eight() -> Knot:
    """4_1, the figure-eight knot. Amphichiral (equal to its own mirror)."""
    return Knot.from_tokens([
        (1, 'O', '+'), (2, 'O', '-'), (3, 'O', '+'), (4, 'O', '-'),
        (2, 'U', '-'), (1, 'U', '+'), (4, 'U', '-'), (3, 'U', '+'),
    ])

def cinquefoil() -> Knot:
    """5_1, the cinquefoil / Solomon's seal knot. Torus knot T(2,5),
    built as the n=5 case of the general T(2,n) pattern 1..n,1..n."""
    return Knot.from_tokens([
        (1, 'O', '+'), (2, 'O', '+'), (3, 'O', '+'), (4, 'O', '+'), (5, 'O', '+'),
        (1, 'U', '+'), (2, 'U', '+'), (3, 'U', '+'), (4, 'U', '+'), (5, 'U', '+'),
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