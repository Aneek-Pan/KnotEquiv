from knot.structure import Knot
from knot.seeds import trefoil, figure_eight, cinquefoil, unknot
from knot.canonical import canonical_gauss_form, knots_equal


def test_identical_knot_equals_itself():
    k = trefoil()
    assert knots_equal(k, k)

def test_rotation_invariance():
    seq = trefoil().seq
    rotated = Knot.from_tokens(seq[2:] + seq[:2])
    assert knots_equal(trefoil(), rotated)

def test_reversal_invariance():
    seq = trefoil().seq
    reversed_knot = Knot.from_tokens(seq[::-1])
    assert knots_equal(trefoil(), reversed_knot)

def test_relabeling_invariance():
    # swap labels 1 and 2 throughout -- should still be recognized as the same diagram
    seq = trefoil().seq
    swapped = Knot.from_tokens([
        (2 if l == 1 else (1 if l == 2 else l), ou, sign) for l, ou, sign in seq
    ])
    assert knots_equal(trefoil(), swapped)

def test_different_knots_not_equal():
    assert not knots_equal(trefoil(), figure_eight())
    assert not knots_equal(trefoil(), cinquefoil())
    assert not knots_equal(figure_eight(), cinquefoil())

def test_unknot_equals_itself():
    assert knots_equal(unknot(), unknot())

def test_mirror_not_equal_by_default():
    # flipping all signs on the trefoil gives its mirror image (chiral knot)
    mirrored_seq = [(l, ou, '+' if s == '-' else '-') for l, ou, s in trefoil().seq]
    mirrored = Knot.from_tokens(mirrored_seq)
    assert not knots_equal(trefoil(), mirrored, allow_mirror=False)

def test_mirror_equal_when_allowed():
    mirrored_seq = [(l, ou, '+' if s == '-' else '-') for l, ou, s in trefoil().seq]
    mirrored = Knot.from_tokens(mirrored_seq)
    assert knots_equal(trefoil(), mirrored, allow_mirror=True)

def test_snappy_derived_figure_eight_matches_our_seed():
    # regression test locking in the real cross-validation we just did
    # by hand against SnapPy's output
    snappy_fig8 = Knot.from_tokens([
        (1, 'U', '-'), (2, 'O', '-'), (3, 'U', '+'), (4, 'O', '+'),
        (2, 'U', '-'), (1, 'O', '-'), (4, 'U', '+'), (3, 'O', '+'),
    ])
    assert knots_equal(figure_eight(), snappy_fig8)