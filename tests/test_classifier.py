import torch
from knot.seeds import trefoil, figure_eight
from model.gnn import prepare_graph_tensors
from model.classifier import SiameseKnotClassifier

def test_classifier_forward_returns_single_logit():
    torch.manual_seed(0)
    model = SiameseKnotClassifier(node_feature_dim=4)
    x_a, e_a = prepare_graph_tensors(trefoil())
    x_b, e_b = prepare_graph_tensors(figure_eight())
    logit = model(x_a, e_a, x_b, e_b)
    assert logit.shape == (1,)

def test_classifier_same_knot_twice_gives_symmetric_style_output():
    # not asserting equivalence => any specific score here, just that
    # feeding the same knot as both inputs runs cleanly and deterministically
    torch.manual_seed(0)
    model = SiameseKnotClassifier(node_feature_dim=4)
    x, e = prepare_graph_tensors(trefoil())
    out1 = model(x, e, x, e)
    out2 = model(x, e, x, e)
    assert torch.allclose(out1, out2)

def test_gradients_flow_through_classifier():
    torch.manual_seed(0)
    model = SiameseKnotClassifier(node_feature_dim=4)
    x_a, e_a = prepare_graph_tensors(trefoil())
    x_b, e_b = prepare_graph_tensors(figure_eight())

    logit = model(x_a, e_a, x_b, e_b)
    target = torch.tensor([1.0])
    loss = torch.nn.functional.binary_cross_entropy_with_logits(logit, target)
    loss.backward()

    # confirm at least one parameter actually received a gradient
    grads_exist = any(p.grad is not None and p.grad.abs().sum() > 0 for p in model.parameters())
    assert grads_exist

def test_classifier_is_order_invariant():
    torch.manual_seed(0)
    model = SiameseKnotClassifier(node_feature_dim=4)
    x_a, e_a = prepare_graph_tensors(trefoil())
    x_b, e_b = prepare_graph_tensors(figure_eight())

    out_ab = model(x_a, e_a, x_b, e_b)
    out_ba = model(x_b, e_b, x_a, e_a)
    assert torch.allclose(out_ab, out_ba, atol=1e-6)