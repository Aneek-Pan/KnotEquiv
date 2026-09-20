from typing import List, Tuple
import networkx as nx

# Fixed, documented encoding order -- must stay consistent between
# featurization calls, since a GNN cares about which index means what.
TAG_ENCODING = {'O': [1, 0], 'U': [0, 1]}
SIGN_ENCODING = {'+': [1, 0], '-': [0, 1]}
EDGE_KIND_ENCODING = {'sequence': [1, 0], 'pair': [0, 1]}

NODE_FEATURE_DIM = 4   # 2 (tag) + 2 (sign)
EDGE_FEATURE_DIM = 2   # 2 (kind)


def node_features(G: nx.MultiGraph) -> List[List[float]]:
    """
    Build a feature vector per node, in node-index order (0..n-1).
    Deliberately excludes the raw crossing label: labels are arbitrary
    under relabeling (see canonical_gauss_form), so including them risks
    the model learning spurious structure tied to arbitrary numbering
    rather than genuine topology.
    """
    features = []
    for idx in sorted(G.nodes):
        data = G.nodes[idx]
        vec = TAG_ENCODING[data['tag']] + SIGN_ENCODING[data['sign']]
        features.append(vec)
    return features


def edge_index_and_features(G: nx.MultiGraph) -> Tuple[List[Tuple[int, int]], List[List[float]]]:
    """
    Build the edge list and matching per-edge feature vectors, in a
    fixed, consistent order (each edge appears once here; downstream
    GNN code can duplicate as (u,v) and (v,u) if an undirected/both-
    directions format is needed -- kept as one direction here to avoid
    ambiguity about ordering).
    """
    edge_index = []
    edge_feats = []
    for u, v, key, data in G.edges(keys=True, data=True):
        edge_index.append((u, v))
        edge_feats.append(EDGE_KIND_ENCODING[data['kind']])
    return edge_index, edge_feats