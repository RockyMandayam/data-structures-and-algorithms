from dsa.graphs.analysis.paths.shortest_paths import get_shortest_paths
from dsa.graphs.graph import Graph


def test_get_shortest_paths() -> None:
    g = Graph(
        nodes=7,
        edges=(
            {
                (0, 1): 2,
                (0, 2): 1,
                (1, 2): 5,
                (1, 3): 11,
                (1, 4): 3,
                (2, 4): 1,
                (2, 5): 15,
                (3, 4): 2,
                (3, 6): 1,
                (4, 5): 4,
                (4, 6): 5,
            }
        ),
    )
    parents = get_shortest_paths(g, 0)
    assert parents == {
        0: None,
        1: 0,
        2: 0,
        3: 4,
        4: 2,
        5: 4,
        6: 3,
    }

    parents = get_shortest_paths(g, 0, weighted=False)
    assert parents == {
        0: None,
        1: 0,
        2: 0,
        3: 1,
        4: 1,
        5: 2,
        6: 3,
    }
