from collections.abc import Hashable

from dsa.graphs.analysis.traversal.bfs import bfs
from dsa.graphs.analysis.traversal.dfs import dfs
from dsa.graphs.analysis.traversal.dijkstra import dijkstra
from dsa.graphs.analysis.traversal_type import TraversalType
from dsa.graphs.graph import Graph


def is_connected(g: Graph) -> bool:
    """Returns if the graph is connected. NOTE: only for undirected graphs."""
    return len(get_connected_components(g)) == 1


def get_connected_components(
    g: Graph, traversal_type: TraversalType = TraversalType.DFS
) -> list[list[Hashable]]:
    """Gets connected components in graph g

    NOTE: only for undirected graphs.

    Args:
        g: Graph
        traversal_type: what traversal algorithm to use; defaults to DFS

    Returns:
        list[list[Hashable]]: List of connected components (CC), where each CC is a list of nodes
    """
    if traversal_type == TraversalType.DFS:
        *_, ccs, _ = dfs(g)
    elif traversal_type == TraversalType.BFS:
        *_, ccs, _ = bfs(g)
    elif traversal_type == TraversalType.DIJKSTRA:
        *_, ccs, _ = dijkstra(g)
    else:
        raise ValueError(f"Unrecognized {traversal_type=}")
    return ccs
