from graphs.analysis.cycles.cycles import contains_cycle
from graphs.graph import Graph
from graphs.graph_factory import GraphFactory


def test_contains_cycle() -> None:
    g_complete = GraphFactory.create_complete_graph(4)
    assert contains_cycle(g_complete)

    g_spindly_tree = GraphFactory.create_spindly_tree(5)
    assert not contains_cycle(g_spindly_tree)

    g_combined = GraphFactory.concat_int_graphs((g_complete, g_spindly_tree))
    assert contains_cycle(g_combined)

    assert contains_cycle(GraphFactory.concat_int_graphs((g_complete, g_complete)))
    assert contains_cycle(GraphFactory.concat_int_graphs((g_complete, g_spindly_tree)))
    assert contains_cycle(GraphFactory.concat_int_graphs((g_spindly_tree, g_complete)))
    assert not contains_cycle(
        GraphFactory.concat_int_graphs((g_spindly_tree, g_spindly_tree))
    )
