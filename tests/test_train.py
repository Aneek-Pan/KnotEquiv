import os
import torch
from knot.seeds import trefoil, figure_eight, unknot
from dataset.generator import generate_dataset
from training.train import load_examples, train_one_epoch, evaluate, run_training
from training.config import TrainConfig
from model.classifier import SiameseKnotClassifier


def test_load_examples_produces_correct_labels(tmp_path):
    path = str(tmp_path / "mini.jsonl")
    generate_dataset(num_examples=10, output_path=path, seed=1)
    examples = load_examples(path)
    assert len(examples) == 10
    for knot_a, knot_b, label in examples:
        assert label in (0.0, 1.0)

def test_train_one_epoch_runs_and_loss_is_finite(tmp_path):
    path = str(tmp_path / "mini.jsonl")
    generate_dataset(num_examples=10, output_path=path, seed=2)
    examples = load_examples(path)

    torch.manual_seed(0)
    model = SiameseKnotClassifier(node_feature_dim=4)
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    loss_fn = torch.nn.BCEWithLogitsLoss()

    avg_loss = train_one_epoch(model, examples, optimizer, loss_fn)
    assert avg_loss == avg_loss  # not NaN
    assert avg_loss > 0

def test_evaluate_returns_loss_and_accuracy(tmp_path):
    path = str(tmp_path / "mini.jsonl")
    generate_dataset(num_examples=10, output_path=path, seed=3)
    examples = load_examples(path)

    torch.manual_seed(0)
    model = SiameseKnotClassifier(node_feature_dim=4)
    loss_fn = torch.nn.BCEWithLogitsLoss()
    metrics = evaluate(model, examples, loss_fn)

    assert 0.0 <= metrics['accuracy'] <= 1.0
    assert metrics['loss'] > 0

def test_full_training_run_end_to_end(tmp_path):
    dataset_dir = tmp_path / "datasets"
    (dataset_dir / "train").mkdir(parents=True)

    from dataset.generator import generate_dataset
    generate_dataset(20, str(dataset_dir / "train" / "train.jsonl"), seed=10)
    generate_dataset(6, str(dataset_dir / "train" / "validation.jsonl"), seed=11)

    checkpoint_path = str(tmp_path / "checkpoint.pt")
    config = TrainConfig(
        num_epochs=2,
        dataset_dir=str(dataset_dir),
        checkpoint_path=checkpoint_path,
        seed=0,
    )
    model, history = run_training(config)

    assert len(history) == 2
    assert os.path.exists(checkpoint_path)