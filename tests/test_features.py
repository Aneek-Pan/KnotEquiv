from knot.seeds import trefoil, unknot
from model.graph import knot_to_graph
from model.features import (
    node_features, edge_index_and_features,
    NODE_FEATURE_DIM, EDGE_FEATURE_DIM,
    TAG_ENCODING, SIGN_ENCODING, EDGE_KIND_ENCODING,
)


def test_node_features_correct_count_and_dim():
    G = knot_to_graph(trefoil())
    feats = node_features(G)
    assert len(feats) == 6
    for vec in feats:
        assert len(vec) == NODE_FEATURE_DIM

def test_node_features_match_encoding_tables():
    G = knot_to_graph(trefoil())
    feats = node_features(G)
    for idx in sorted(G.nodes):
        data = G.nodes[idx]
        expected = TAG_ENCODING[data['tag']] + SIGN_ENCODING[data['sign']]
        assert feats[idx] == expected

def test_no_raw_label_leaks_into_features():
    # crossing labels are arbitrary under relabeling -- confirm the
    # feature dimension is exactly 4, not accidentally 5+ (which would
    # suggest the label snuck in somewhere)
    G = knot_to_graph(trefoil())
    feats = node_features(G)
    assert all(len(vec) == 4 for vec in feats)

def test_unknot_features_are_empty():
    G = knot_to_graph(unknot())
    assert node_features(G) == []
    edges, feats = edge_index_and_features(G)
    assert edges == []
    assert feats == []

def test_edge_features_correct_dim_and_count():
    G = knot_to_graph(trefoil())
    edges, feats = edge_index_and_features(G)
    assert len(edges) == len(feats)
    assert len(edges) == G.number_of_edges()
    for vec in feats:
        assert len(vec) == EDGE_FEATURE_DIM

def test_edge_features_match_kind():
    G = knot_to_graph(trefoil())
    edges, feats = edge_index_and_features(G)
    for (u, v), vec in zip(edges, feats):
        # find the corresponding edge data kind directly from the graph
        kinds_between = [d['kind'] for k, d in G[u][v].items()]
        assert EDGE_KIND_ENCODING[kinds_between[0]] == vec or vec in [EDGE_KIND_ENCODING[k] for k in kinds_between]

def test_sequence_and_pair_edges_get_distinct_encodings():
    assert EDGE_KIND_ENCODING['sequence'] != EDGE_KIND_ENCODING['pair']

def test_tag_and_sign_encodings_are_distinct():
    assert TAG_ENCODING['O'] != TAG_ENCODING['U']
    assert SIGN_ENCODING['+'] != SIGN_ENCODING['-']