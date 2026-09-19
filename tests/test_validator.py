from knot.structure import Knot
from knot.validator import build_interlacement_graph, passes_gauss_parity_check

def trefoil():
    return Knot.from_tokens([
        (1, 'O', '+'), (2, 'O', '+'), (3, 'O', '+'),
        (1, 'U', '+'), (2, 'U', '+'), (3, 'U', '+'),
    ])

def figure_eight():
    return Knot.from_tokens([
        (1, 'O', '+'), (2, 'O', '-'), (3, 'O', '+'), (4, 'O', '-'),
        (2, 'U', '-'), (1, 'U', '+'), (4, 'U', '-'), (3, 'U', '+'),
    ])

def test_trefoil_passes_parity():
    assert passes_gauss_parity_check(trefoil()) is True

def test_trefoil_interlacement_graph_shape():
    graph = build_interlacement_graph(trefoil())
    assert set(graph.keys()) == {1, 2, 3}
    for label in graph:
        assert len(graph[label]) == 2

def test_classic_nonrealizable_1212_fails_parity():
    k = Knot.from_tokens([
        (1, 'O', '+'), (2, 'O', '+'), (1, 'U', '+'), (2, 'U', '+'),
    ])
    assert passes_gauss_parity_check(k) is False

def test_single_kink_passes_trivially():
    k = Knot.from_tokens([(1, 'O', '+'), (1, 'U', '+')])
    assert passes_gauss_parity_check(k) is True

def test_two_disjoint_kinks_pass():
    k = Knot.from_tokens([
        (1, 'O', '+'), (1, 'U', '+'), (2, 'O', '+'), (2, 'U', '+'),
    ])
    assert passes_gauss_parity_check(k) is True
    graph = build_interlacement_graph(k)
    assert graph[1] == set()
    assert graph[2] == set()

def test_figure_eight_passes_parity():
    assert passes_gauss_parity_check(figure_eight()) is True

def test_figure_eight_interlacement_graph_shape():
    graph = build_interlacement_graph(figure_eight())
    assert set(graph.keys()) == {1, 2, 3, 4}
    for label in graph:
        assert len(graph[label]) % 2 == 0