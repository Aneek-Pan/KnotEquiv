from knot.seeds import trefoil, unknot, figure_eight
from model.graph import knot_to_graph


def test_node_count_matches_sequence_length():
    G = knot_to_graph(trefoil())
    assert G.number_of_nodes() == 6


def test_unknot_graph_is_empty():
    G = knot_to_graph(unknot())
    assert G.number_of_nodes() == 0
    assert G.number_of_edges() == 0


def test_sequence_edges_form_full_cycle():
    G = knot_to_graph(trefoil())
    seq_edges = [(u, v) for u, v, k, d in G.edges(keys=True, data=True) if d['kind'] == 'sequence']
    assert len(seq_edges) == 6


def test_pair_edges_count_matches_crossing_count():
    G = knot_to_graph(trefoil())
    pair_edges = [(u, v) for u, v, k, d in G.edges(keys=True, data=True) if d['kind'] == 'pair']
    assert len(pair_edges) == 3


def test_pair_edges_connect_same_label_nodes():
    G = knot_to_graph(figure_eight())
    for u, v, k, d in G.edges(keys=True, data=True):
        if d['kind'] == 'pair':
            assert G.nodes[u]['label'] == G.nodes[v]['label']


def test_node_attributes_match_original_tokens():
    k = trefoil()
    G = knot_to_graph(k)
    for idx, (label, tag, sign) in enumerate(k.seq):
        assert G.nodes[idx]['label'] == label
        assert G.nodes[idx]['tag'] == tag
        assert G.nodes[idx]['sign'] == sign


def test_every_node_has_degree_at_least_two():
    # each token connects to 2 sequence neighbors + 1 pair partner,
    # except possibly in tiny degenerate cases -- for a real knot
    # (3+ crossings) every node should have exactly degree 3
    G = knot_to_graph(trefoil())
    for node in G.nodes:
        assert G.degree(node) == 3