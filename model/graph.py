# model/graph.py
import networkx as nx
from typing import Dict, List
from knot.structure import Knot


def knot_to_graph(knot: Knot) -> nx.MultiGraph:
    """
    Convert a Knot's Gauss code into a graph. Each token (one O or U pass
    through a crossing) is a node. Two edge kinds:
      - 'sequence': consecutive tokens in cyclic traversal order
      - 'pair': the two tokens sharing the same crossing label
    Node attributes: label (crossing id), tag ('O'/'U'), sign ('+'/'-').
    A MultiGraph is used since a 1-crossing knot can have both a
    sequence edge and a pair edge between the same two nodes.
    """
    seq = knot.seq
    n = len(seq)
    G = nx.MultiGraph()

    for idx, (label, tag, sign) in enumerate(seq):
        G.add_node(idx, label=label, tag=tag, sign=sign)

    for idx in range(n):
        G.add_edge(idx, (idx + 1) % n, kind='sequence')

    label_positions: Dict[int, List[int]] = {}
    for idx, (label, tag, sign) in enumerate(seq):
        label_positions.setdefault(label, []).append(idx)
    for label, positions in label_positions.items():
        if len(positions) == 2:
            i, j = positions
            G.add_edge(i, j, kind='pair')

    return G