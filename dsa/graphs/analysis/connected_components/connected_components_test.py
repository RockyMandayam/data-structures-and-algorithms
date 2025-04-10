import pytest

from dsa.graphs.analysis.connected_components.connected_components import (
    get_connected_components,
    get_strongly_connected_components,
)
from dsa.graphs.analysis.traversal_type import TraversalType
from dsa.graphs.digraph import Digraph
from dsa.graphs.graph_factory import GraphFactory


@pytest.mark.parametrize(
    "traversal_type", (TraversalType.DFS, TraversalType.BFS, TraversalType.DIJKSTRA)
)
def test_get_connected_components(traversal_type: TraversalType) -> None:
    g_complete = GraphFactory.create_complete_graph(4)
    ccs = get_connected_components(g_complete, traversal_type=traversal_type)
    assert ccs == [list(range(4))]

    g_spindly_tree = GraphFactory.create_spindly_tree(5)
    ccs = get_connected_components(g_spindly_tree, traversal_type=traversal_type)
    assert ccs == [list(range(5))]

    ccs = get_connected_components(
        GraphFactory.concat_int_graphs((g_complete, g_complete)),
        traversal_type=traversal_type,
    )
    assert ccs == [list(range(4)), list(range(4, 8))]
    ccs = get_connected_components(
        GraphFactory.concat_int_graphs((g_complete, g_spindly_tree)),
        traversal_type=traversal_type,
    )
    assert ccs == [list(range(4)), list(range(4, 9))]
    ccs = get_connected_components(
        GraphFactory.concat_int_graphs((g_spindly_tree, g_complete)),
        traversal_type=traversal_type,
    )
    assert ccs == [list(range(5)), list(range(5, 9))]
    ccs = get_connected_components(
        GraphFactory.concat_int_graphs((g_spindly_tree, g_spindly_tree)),
        traversal_type=traversal_type,
    )
    assert ccs == [list(range(5)), list(range(5, 10))]


def test_get_strongly_connected_components() -> None:
    dg = Digraph(
        nodes="ABCDEFGHIJKL",
        edges=(
            ("A", "B"),
            ("B", "C"),
            ("B", "D"),
            ("B", "E"),
            ("C", "F"),
            ("E", "B"),
            ("E", "F"),
            ("E", "G"),
            ("F", "C"),
            ("F", "H"),
            ("G", "H"),
            ("G", "J"),
            ("H", "K"),
            ("I", "G"),
            ("J", "I"),
            ("K", "L"),
            ("L", "J"),
        ),
    )
    sccs = get_strongly_connected_components(dg)
    sccs = set(tuple(scc) for scc in sccs)
    exp_sccs = [
        set(("G", "H", "I", "J", "K", "L")),
        set(("C", "F")),
        set(("B", "E")),
        set(("D",)),
        set(("A",)),
    ]
    for scc in sccs:
        assert set(scc) in exp_sccs
