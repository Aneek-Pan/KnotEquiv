from dataclasses import dataclass

@dataclass
class TrainConfig:
    node_feature_dim: int = 4
    hidden_dim: int = 16
    embedding_dim: int = 8
    learning_rate: float = 1e-3
    num_epochs: int = 20
    dataset_dir: str = "dataset/datasets"
    checkpoint_path: str = "experiments/results/checkpoint.pt"
    seed: int = 0