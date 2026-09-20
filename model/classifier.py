import torch
import torch.nn as nn
from model.gnn import GraphEncoder


class SiameseKnotClassifier(nn.Module):
    """
    Siamese architecture: the SAME GraphEncoder (shared weights) encodes
    both input knots independently, so the model learns one consistent
    notion of 'knot embedding' rather than two separate ones for
    'first knot' vs 'second knot'. The two embeddings are concatenated
    and passed through a small MLP head to produce a single logit.
    """
    def __init__(self, node_feature_dim: int, hidden_dim: int = 16, embedding_dim: int = 8):
        super().__init__()
        self.encoder = GraphEncoder(node_feature_dim, hidden_dim, embedding_dim)
        self.classifier_head = nn.Sequential(
            nn.Linear(embedding_dim * 2, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, 1),
        )

    def forward(self, x_a, edge_index_a, x_b, edge_index_b) -> torch.Tensor:
        emb_a = self.encoder(x_a, edge_index_a)
        emb_b = self.encoder(x_b, edge_index_b)
        combined = torch.cat([emb_a + emb_b, torch.abs(emb_a - emb_b)], dim=0)
        return self.classifier_head(combined)