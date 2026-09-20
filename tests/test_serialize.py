import json
from knot.seeds import trefoil, figure_eight
from dataset.positive import generate_positive_pair
from dataset.negative import generate_negative_pair
from dataset.serialize import (
    knot_to_dict, knot_from_dict,
    move_to_dict, move_from_dict,
    positive_pair_to_dict, positive_pair_from_dict,
    negative_pair_to_dict, negative_pair_from_dict,
    save_jsonl, load_jsonl,
)

def test_knot_round_trip():
    k = trefoil()
    restored = knot_from_dict(knot_to_dict(k))
    assert restored.seq == k.seq

def test_knot_round_trip_preserves_tuples_not_lists():
    k = trefoil()
    restored = knot_from_dict(knot_to_dict(k))
    for token in restored.seq:
        assert isinstance(token, tuple)

def test_move_round_trip():
    from moves.move import Move
    m = Move('R1', 'add', {'label': 4, 'sign': '+'})
    restored = move_from_dict(move_to_dict(m))
    assert restored.kind == m.kind
    assert restored.action == m.action
    assert restored.params == m.params

def test_positive_pair_round_trip():
    start, end, trace = generate_positive_pair(trefoil(), num_moves=10, seed=1)
    d = positive_pair_to_dict(start, end, trace)

    json_str = json.dumps(d)
    d_reloaded = json.loads(json_str)

    r_start, r_end, r_trace = positive_pair_from_dict(d_reloaded)
    assert r_start.seq == start.seq
    assert r_end.seq == end.seq
    assert len(r_trace) == len(trace)

    for original, restored in zip(trace, r_trace):
        assert original.kind == restored.kind
        assert original.action == restored.action
        # params may contain tuples that become lists after a JSON round
        # trip -- that's an inherent JSON limitation, not a bug, so
        # compare params structurally rather than via strict equality
        assert _params_equal(original.params, restored.params)

def test_negative_pair_round_trip():
    result = generate_negative_pair(trefoil(), figure_eight(), num_moves=8, trials=5, seed=2)
    d = negative_pair_to_dict(result)

    json_str = json.dumps(d)
    d_reloaded = json.loads(json_str)

    r = negative_pair_from_dict(d_reloaded)
    assert r['knot_a_end'].seq == result['knot_a_end'].seq
    assert r['knot_b_end'].seq == result['knot_b_end'].seq
    assert r['diff'] == result['diff']
    assert r['label'] == 'NOT_EQUIVALENT'

def test_save_and_load_jsonl_file(tmp_path):
    start, end, trace = generate_positive_pair(trefoil(), num_moves=5, seed=3)
    record = positive_pair_to_dict(start, end, trace)

    path = str(tmp_path / "test_dataset.jsonl")
    save_jsonl([record, record], path)  # two identical records

    loaded = load_jsonl(path)
    assert len(loaded) == 2
    r_start, r_end, r_trace = positive_pair_from_dict(loaded[0])
    assert r_start.seq == start.seq
    assert r_end.seq == end.seq

def test_jsonl_file_is_one_json_object_per_line(tmp_path):
    start, end, trace = generate_positive_pair(trefoil(), num_moves=3, seed=4)
    record = positive_pair_to_dict(start, end, trace)

    path = str(tmp_path / "test.jsonl")
    save_jsonl([record], path)

    with open(path) as f:
        lines = f.readlines()
    assert len(lines) == 1
    json.loads(lines[0])  # should not raise

def _params_equal(a, b) -> bool:
    """Compare two params dicts treating tuples and lists as equivalent
    (since JSON serialization can't distinguish them)."""
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(_params_equal(x, y) for x, y in zip(a, b))
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(_params_equal(a[k], b[k]) for k in a)
    return a == b