from training.config import TrainConfig
from training.train import run_training, load_examples, evaluate
import torch.nn as nn

config = TrainConfig(dataset_dir="dataset/datasets", num_epochs=0, resume_from="experiments/results/checkpoint.pt")
model, _ = run_training(config)

test_examples = load_examples("dataset/datasets/train/test.jsonl")
test_metrics = evaluate(model, test_examples, nn.BCEWithLogitsLoss())
print(f"Test accuracy: {test_metrics['accuracy']:.3f}")