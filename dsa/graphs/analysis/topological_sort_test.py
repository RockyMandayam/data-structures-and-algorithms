import pytest

from dsa.graphs.analysis.topological_sort import topological_sort
from dsa.graphs.analysis.traversal_type import TraversalType
from dsa.graphs.digraph import Digraph
from dsa.utils import get_key_to_index


@pytest.mark.parametrize("traversal_type", (TraversalType.DFS, TraversalType.BFS))
def test_topological_sort(traversal_type: TraversalType) -> None:
    dg = Digraph(
        nodes="ABCDEFGHIJKL",
        edges=(
            ("A", "B"),
            ("B", "C"),
            ("B", "D"),
            ("B", "E"),
            ("C", "F"),
            # ("E", "B"),
            ("E", "F"),
            ("E", "G"),
            # ("F", "C"),
            ("F", "H"),
            ("G", "H"),
            ("G", "J"),
            ("H", "K"),
            # ("I", "G"),
            # ("J", "I"),
            ("K", "L"),
            # ("L", "J"),
        ),
    )
    sorted_nodes = topological_sort(dg, traversal_type=traversal_type)
    # key->index to faster checks
    sorted_node_to_index = get_key_to_index(sorted_nodes)
    for u, v in dg.get_edges():
        assert sorted_node_to_index[u] < sorted_node_to_index[v]

    dg.add_edge(("E", "B"))
    with pytest.raises(ValueError):
        topological_sort(dg, traversal_type=traversal_type)

    dg.remove_edge(("E", "B"))
    dg.add_edge(("L", "J"))
    sorted_nodes = topological_sort(dg, traversal_type=traversal_type)
    sorted_node_to_index = get_key_to_index(sorted_nodes)
    for u, v in dg.get_edges():
        assert sorted_node_to_index[u] < sorted_node_to_index[v]
    dg.add_edges((("I", "G"), ("G", "I")))
    with pytest.raises(ValueError):
        topological_sort(dg, traversal_type=traversal_type)
