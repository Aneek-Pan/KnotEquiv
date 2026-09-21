import random
import itertools
from typing import List, Dict, Any
from knot.seeds import SEEDS, get_seed
from dataset.positive import generate_positive_pair
from dataset.negative import generate_negative_pair
from dataset.serialize import positive_pair_to_dict, negative_pair_to_dict, save_jsonl


def generate_dataset(
    num_examples: int,
    output_path: str,
    positive_ratio: float = 0.5,
    move_range: tuple = (5, 15),
    negative_trials: int = 10,
    seed: int = None,
) -> Dict[str, int]:
    """
    Generate a labeled dataset of positive (equivalent) and negative
    (non-equivalent) knot pairs, and save it as JSONL to output_path.

    positive_ratio: fraction of examples that are positive pairs (0.5 = 50/50).
    move_range: (min, max) inclusive range of Reidemeister moves per walk,
                randomized per example for variety.
    negative_trials: trials passed to generate_negative_pair's cross-product search.

    Returns a summary dict with counts actually generated.
    """
    rng = random.Random(seed)
    seed_names = list(SEEDS.keys())

    num_positive = round(num_examples * positive_ratio)
    num_negative = num_examples - num_positive

    # negative pairs need two DISTINCT seed knots; warn/fail loudly if the
    # seed pool can't support the requested variety, rather than silently
    # repeating the same seed pair over and over
    distinct_pairs = list(itertools.combinations(seed_names, 2))
    if not distinct_pairs:
        raise ValueError("Need at least 2 distinct seed knots to generate negative pairs")
    if num_negative > 0 and len(distinct_pairs) < 1:
        raise ValueError("No valid distinct-seed pairs available for negative generation")

    records: List[Dict[str, Any]] = []

    for _ in range(num_positive):
        seed_name = rng.choice(seed_names)
        num_moves = rng.randint(*move_range)
        start = get_seed(seed_name)
        walk_seed = rng.randrange(2**31)
        s, e, trace = generate_positive_pair(start, num_moves=num_moves, seed=walk_seed)
        records.append(positive_pair_to_dict(s, e, trace))

    for _ in range(num_negative):
        name_a, name_b = rng.choice(distinct_pairs)
        num_moves = rng.randint(*move_range)
        walk_seed = rng.randrange(2**31)
        result = generate_negative_pair(
            get_seed(name_a), get_seed(name_b),
            num_moves=num_moves, trials=negative_trials, seed=walk_seed,
        )
        records.append(negative_pair_to_dict(result))

    rng.shuffle(records)  # interleave positive/negative rather than blocks of each
    save_jsonl(records, output_path)

    return {
        'total': len(records),
        'positive': num_positive,
        'negative': num_negative,
    }

def generate_split_datasets(
    total_examples: int,
    output_dir: str,
    train_frac: float = 0.7,
    val_frac: float = 0.15,
    # remaining goes to test
    **generate_kwargs,
) -> Dict[str, Dict[str, int]]:
    """
    Generate three separate datasets (train/validation/test) with
    independent, non-overlapping random seeds, so no example can leak
    across splits. Saves to {output_dir}/train.jsonl, etc.
    """
    import os
    n_train = round(total_examples * train_frac)
    n_val = round(total_examples * val_frac)
    n_test = total_examples - n_train - n_val

    base_seed = generate_kwargs.pop('seed', 0) or 0
    os.makedirs(output_dir, exist_ok=True)

    summaries = {}
    summaries['train'] = generate_dataset(
        n_train, f"{output_dir}/train.jsonl", seed=base_seed + 1, **generate_kwargs
    )
    summaries['validation'] = generate_dataset(
        n_val, f"{output_dir}/validation.jsonl", seed=base_seed + 2, **generate_kwargs
    )
    summaries['test'] = generate_dataset(
        n_test, f"{output_dir}/test.jsonl", seed=base_seed + 3, **generate_kwargs
    )
    return summaries