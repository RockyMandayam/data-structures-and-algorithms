import pytest

from graphs.analysis.cycles.cycles import contains_cycle
from graphs.analysis.traversal_type import TraversalType
from graphs.graph import Graph
from graphs.graph_factory import GraphFactory


@pytest.mark.parametrize("traversal_type", (TraversalType.DFS, TraversalType.BFS))
def test_contains_cycle(traversal_type: TraversalType) -> None:
    g_complete = GraphFactory.create_complete_graph(4)
    assert contains_cycle(g_complete, traversal_type=traversal_type)

    g_spindly_tree = GraphFactory.create_spindly_tree(5)
    assert not contains_cycle(g_spindly_tree, traversal_type=traversal_type)

    g_combined = GraphFactory.concat_int_graphs((g_complete, g_spindly_tree))
    assert contains_cycle(g_combined, traversal_type=traversal_type)

    assert contains_cycle(
        GraphFactory.concat_int_graphs((g_complete, g_complete)),
        traversal_type=traversal_type,
    )
    assert contains_cycle(
        GraphFactory.concat_int_graphs((g_complete, g_spindly_tree)),
        traversal_type=traversal_type,
    )
    assert contains_cycle(
        GraphFactory.concat_int_graphs((g_spindly_tree, g_complete)),
        traversal_type=traversal_type,
    )
    assert not contains_cycle(
        GraphFactory.concat_int_graphs((g_spindly_tree, g_spindly_tree)),
        traversal_type=traversal_type,
    )
