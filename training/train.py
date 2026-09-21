import torch
import torch.nn as nn
from typing import List, Dict, Any
from model.classifier import SiameseKnotClassifier
from model.gnn import prepare_graph_tensors
from dataset.serialize import load_jsonl, positive_pair_from_dict, negative_pair_from_dict
from training.config import TrainConfig


def load_examples(path: str) -> List[Dict[str, Any]]:
    """
    Load a JSONL dataset file and convert each record into a
    (knot_a, knot_b, label) triple ready for training. For positive
    pairs, knot_a/knot_b are the pair's two endpoints; for negative
    pairs, we use each knot's FINAL (post-walk) state, since that's
    the actual pair the model should learn to distinguish.
    """
    raw = load_jsonl(path)
    examples = []
    for record in raw:
        if record['label'] == 'EQUIVALENT':
            knot_a, knot_b, _ = positive_pair_from_dict(record)
            examples.append((knot_a, knot_b, 1.0))
        else:
            d = negative_pair_from_dict(record)
            examples.append((d['knot_a_end'], d['knot_b_end'], 0.0))
    return examples


def compute_loss(model, knot_a, knot_b, label: float, loss_fn) -> torch.Tensor:
    x_a, e_a = prepare_graph_tensors(knot_a)
    x_b, e_b = prepare_graph_tensors(knot_b)
    logit = model(x_a, e_a, x_b, e_b)
    target = torch.tensor([label])
    return loss_fn(logit, target)


def train_one_epoch(model, examples, optimizer, loss_fn) -> float:
    model.train()
    total_loss = 0.0
    for knot_a, knot_b, label in examples:
        optimizer.zero_grad()
        loss = compute_loss(model, knot_a, knot_b, label, loss_fn)
        loss.backward()
        optimizer.step()
        total_loss += loss.item()
    return total_loss / len(examples)


@torch.no_grad()
def evaluate(model, examples, loss_fn) -> Dict[str, float]:
    model.eval()
    total_loss = 0.0
    correct = 0
    for knot_a, knot_b, label in examples:
        loss = compute_loss(model, knot_a, knot_b, label, loss_fn)
        total_loss += loss.item()
        x_a, e_a = prepare_graph_tensors(knot_a)
        x_b, e_b = prepare_graph_tensors(knot_b)
        logit = model(x_a, e_a, x_b, e_b)
        pred = 1.0 if torch.sigmoid(logit).item() > 0.5 else 0.0
        if pred == label:
            correct += 1
    return {'loss': total_loss / len(examples), 'accuracy': correct / len(examples)}


def run_training(config: TrainConfig):
    torch.manual_seed(config.seed)

    train_examples = load_examples(f"{config.dataset_dir}/train/train.jsonl")
    val_examples = load_examples(f"{config.dataset_dir}/train/validation.jsonl")

    model = SiameseKnotClassifier(
        node_feature_dim=config.node_feature_dim,
        hidden_dim=config.hidden_dim,
        embedding_dim=config.embedding_dim,
    )
    optimizer = torch.optim.Adam(model.parameters(), lr=config.learning_rate)
    loss_fn = nn.BCEWithLogitsLoss()

    history = []
    for epoch in range(config.num_epochs):
        train_loss = train_one_epoch(model, train_examples, optimizer, loss_fn)
        val_metrics = evaluate(model, val_examples, loss_fn)
        history.append({'epoch': epoch, 'train_loss': train_loss, **val_metrics})
        print(f"Epoch {epoch}: train_loss={train_loss:.4f} "
              f"val_loss={val_metrics['loss']:.4f} val_acc={val_metrics['accuracy']:.3f}")

    torch.save(model.state_dict(), config.checkpoint_path)
    return model, history