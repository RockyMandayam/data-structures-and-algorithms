from collections.abc import Hashable

from dsa.graphs.analysis.traversal.bfs import bfs
from dsa.graphs.analysis.traversal.dijkstra import dijkstra
from dsa.graphs.analysis.traversal_type import TraversalType
from dsa.graphs.graph import Graph


def get_shortest_paths(
    g: Graph,
    s: Hashable,
    weighted: bool = True,
) -> dict[Hashable, Hashable]:
    """Returns paths from s to all reachable nodes via a parents dict"""
    # TODO implement algorithm for negative edges
    assert all(g.get_weight(edge) >= 0 for edge in g.get_edges())
    if weighted:
        parents, *_ = dijkstra(g)
    else:
        parents, *_ = bfs(g)
    return parents
