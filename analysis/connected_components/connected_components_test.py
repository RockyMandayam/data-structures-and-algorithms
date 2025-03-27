import pytest

from graphs.analysis.connected_components.connected_components import (
    get_connected_components,
)
from graphs.analysis.traversal_type import TraversalType
from graphs.graph_factory import GraphFactory


@pytest.mark.parametrize("traversal_type", (TraversalType.DFS, TraversalType.BFS))
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
