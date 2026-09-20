import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import List, Tuple
from knot.structure import Knot
from model.graph import knot_to_graph
from model.features import node_features, edge_index_and_features


def to_bidirectional(edge_index: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """Duplicate each edge in both directions, needed for undirected message passing."""
    bidir = []
    for u, v in edge_index:
        bidir.append((u, v))
        bidir.append((v, u))
    return bidir


def prepare_graph_tensors(knot: Knot) -> Tuple[torch.Tensor, torch.Tensor]:
    """Convert a Knot all the way to (node_features, edge_index) torch tensors."""
    G = knot_to_graph(knot)
    feats = node_features(G)
    edges, _ = edge_index_and_features(G)

    if not feats:
        return torch.zeros((0, 4)), torch.zeros((2, 0), dtype=torch.long)

    x = torch.tensor(feats, dtype=torch.float)
    bidir_edges = to_bidirectional(edges)
    edge_index = torch.tensor(bidir_edges, dtype=torch.long).t().contiguous()
    return x, edge_index


class SimpleGCNLayer(nn.Module):
    """
    A minimal graph convolution layer, hand-written in plain PyTorch
    (deliberately avoiding torch_geometric's fragile version-matched
    install requirements). For each node: mean-aggregate neighbor
    features, concatenate with the node's own features, apply a linear
    transform + ReLU.
    """
    def __init__(self, in_dim: int, out_dim: int):
        super().__init__()
        self.linear = nn.Linear(in_dim * 2, out_dim)

    def forward(self, x: torch.Tensor, edge_index: torch.Tensor) -> torch.Tensor:
        num_nodes = x.size(0)
        if num_nodes == 0:
            return torch.zeros((0, self.linear.out_features), device=x.device)

        src, dst = edge_index[0], edge_index[1]
        agg = torch.zeros_like(x)
        agg.index_add_(0, dst, x[src])
        degree = torch.zeros(num_nodes, device=x.device)
        degree.index_add_(0, dst, torch.ones(src.size(0), device=x.device))
        degree = degree.clamp(min=1).unsqueeze(1)
        agg = agg / degree

        combined = torch.cat([x, agg], dim=1)
        return F.relu(self.linear(combined))


class GraphEncoder(nn.Module):
    """
    Encodes a full knot graph into one fixed-size embedding vector via
    stacked SimpleGCNLayers + mean pooling over all nodes. Explicitly
    handles the zero-node (unknot) case by returning a zero vector,
    since there's nothing to pool.
    """
    def __init__(self, node_feature_dim: int, hidden_dim: int = 16,
                 embedding_dim: int = 8, num_layers: int = 2):
        super().__init__()
        self.embedding_dim = embedding_dim
        dims = [node_feature_dim] + [hidden_dim] * (num_layers - 1) + [embedding_dim]
        self.layers = nn.ModuleList([
            SimpleGCNLayer(dims[i], dims[i + 1]) for i in range(len(dims) - 1)
        ])

    def forward(self, x: torch.Tensor, edge_index: torch.Tensor) -> torch.Tensor:
        if x.size(0) == 0:
            return torch.zeros(self.embedding_dim)
        h = x
        for layer in self.layers:
            h = layer(h, edge_index)
        return h.mean(dim=0)