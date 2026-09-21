import time
from dataset.generator import generate_split_datasets
from training.train import run_training, load_examples, evaluate
from training.config import TrainConfig
import torch.nn as nn

start = time.time()

generate_split_datasets(
    total_examples=3000,
    output_dir="dataset/datasets/train",
    move_range=(5, 20),
    seed=1,
)

config = TrainConfig(dataset_dir="dataset/datasets", num_epochs=20)
model, history = run_training(config)

elapsed = time.time() - start
print(f"\nTotal time: {elapsed:.1f} seconds")