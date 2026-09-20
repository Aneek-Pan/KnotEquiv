import torch
from knot.seeds import trefoil, unknot, figure_eight
from model.gnn import prepare_graph_tensors, GraphEncoder, SimpleGCNLayer

def test_prepare_graph_tensors_shapes():
    x, edge_index = prepare_graph_tensors(trefoil())
    assert x.shape == (6, 4)
    assert edge_index.shape[0] == 2
    # 6 sequence + 3 pair = 9 unique edges, doubled for bidirectional = 18
    assert edge_index.shape[1] == 18

def test_prepare_graph_tensors_unknot_is_empty():
    x, edge_index = prepare_graph_tensors(unknot())
    assert x.shape == (0, 4)
    assert edge_index.shape == (2, 0)

def test_gcn_layer_output_shape():
    x, edge_index = prepare_graph_tensors(trefoil())
    layer = SimpleGCNLayer(in_dim=4, out_dim=8)
    out = layer(x, edge_index)
    assert out.shape == (6, 8)

def test_encoder_output_is_fixed_size_regardless_of_knot_size():
    encoder = GraphEncoder(node_feature_dim=4, embedding_dim=8)
    x1, e1 = prepare_graph_tensors(trefoil())
    x2, e2 = prepare_graph_tensors(figure_eight())
    out1 = encoder(x1, e1)
    out2 = encoder(x2, e2)
    assert out1.shape == (8,)
    assert out2.shape == (8,)  # same embedding size despite different crossing counts

def test_encoder_handles_unknot_without_crashing():
    encoder = GraphEncoder(node_feature_dim=4, embedding_dim=8)
    x, edge_index = prepare_graph_tensors(unknot())
    out = encoder(x, edge_index)
    assert out.shape == (8,)
    assert torch.all(out == 0)

def test_encoder_is_deterministic_given_fixed_weights():
    torch.manual_seed(0)
    encoder = GraphEncoder(node_feature_dim=4, embedding_dim=8)
    x, edge_index = prepare_graph_tensors(trefoil())
    out1 = encoder(x, edge_index)
    out2 = encoder(x, edge_index)
    assert torch.allclose(out1, out2)  # same weights, same input -> same output