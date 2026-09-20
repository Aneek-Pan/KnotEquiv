import os
from dataset.generator import generate_dataset
from dataset.serialize import load_jsonl

def test_generates_correct_total_count(tmp_path):
    path = str(tmp_path / "test.jsonl")
    summary = generate_dataset(num_examples=20, output_path=path, seed=1)
    assert summary['total'] == 20
    loaded = load_jsonl(path)
    assert len(loaded) == 20

def test_respects_positive_ratio(tmp_path):
    path = str(tmp_path / "test.jsonl")
    summary = generate_dataset(num_examples=20, output_path=path, positive_ratio=0.7, seed=2)
    assert summary['positive'] == 14
    assert summary['negative'] == 6

def test_labels_match_expected_counts(tmp_path):
    path = str(tmp_path / "test.jsonl")
    generate_dataset(num_examples=30, output_path=path, positive_ratio=0.5, seed=3)
    loaded = load_jsonl(path)
    labels = [r['label'] for r in loaded]
    assert labels.count('EQUIVALENT') == 15
    assert labels.count('NOT_EQUIVALENT') == 15

def test_reproducible_with_seed(tmp_path):
    path1 = str(tmp_path / "a.jsonl")
    path2 = str(tmp_path / "b.jsonl")
    generate_dataset(num_examples=10, output_path=path1, seed=42)
    generate_dataset(num_examples=10, output_path=path2, seed=42)

    loaded1 = load_jsonl(path1)
    loaded2 = load_jsonl(path2)
    assert loaded1 == loaded2

def test_different_seeds_produce_different_datasets(tmp_path):
    path1 = str(tmp_path / "a.jsonl")
    path2 = str(tmp_path / "b.jsonl")
    generate_dataset(num_examples=10, output_path=path1, seed=1)
    generate_dataset(num_examples=10, output_path=path2, seed=2)

    loaded1 = load_jsonl(path1)
    loaded2 = load_jsonl(path2)
    assert loaded1 != loaded2

def test_records_are_shuffled_not_blocked(tmp_path):
    path = str(tmp_path / "test.jsonl")
    generate_dataset(num_examples=20, output_path=path, positive_ratio=0.5, seed=5)
    loaded = load_jsonl(path)
    labels = [r['label'] for r in loaded]
    # if unshuffled, all EQUIVALENT would come first -- check it's NOT
    # in two clean blocks (weak but honest check; true randomness can't
    # be asserted with certainty from one sample)
    first_half_labels = set(labels[:10])
    assert len(first_half_labels) == 2, "records appear to be unshuffled (blocked by label)"

def test_move_range_is_respected(tmp_path):
    path = str(tmp_path / "test.jsonl")
    generate_dataset(num_examples=10, output_path=path, move_range=(3, 3), seed=6)
    loaded = load_jsonl(path)
    for r in loaded:
        if r['label'] == 'EQUIVALENT':
            assert len(r['moves']) == 3
        else:
            assert len(r['moves_a']) == 3
            assert len(r['moves_b']) == 3