import math
from knot.seeds import trefoil, unknot
from visualization.plot import compute_chord_layout, plot_knot

def test_layout_produces_one_chord_per_crossing():
    chords = compute_chord_layout(trefoil())
    assert len(chords) == 3
    labels = {c.label for c in chords}
    assert labels == {1, 2, 3}

def test_layout_empty_for_unknot():
    assert compute_chord_layout(unknot()) == []

def test_chord_points_lie_on_circle():
    chords = compute_chord_layout(trefoil(), radius=1.0)
    for c in chords:
        r_over = math.hypot(c.p_over.x, c.p_over.y)
        r_under = math.hypot(c.p_under.x, c.p_under.y)
        assert abs(r_over - 1.0) < 1e-9
        assert abs(r_under - 1.0) < 1e-9

def test_chord_signs_preserved():
    chords = compute_chord_layout(trefoil())
    for c in chords:
        assert c.sign == '+'  # trefoil is all-positive by construction

def test_plot_runs_without_error(tmp_path):
    save_path = tmp_path / "trefoil.png"
    plot_knot(trefoil(), save_path=str(save_path))
    assert save_path.exists()