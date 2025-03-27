from collections.abc import Hashable

from dsa.graphs.analysis.traversal.bfs import bfs
from dsa.graphs.analysis.traversal.dfs import dfs
from dsa.graphs.analysis.traversal_type import TraversalType
from dsa.graphs.graph import Graph


def get_connected_components(
    g: Graph, traversal_type: TraversalType = TraversalType.DFS
) -> list[list[Hashable]]:
    """Gets connected components in graph g

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
    else:
        raise ValueError(f"Unrecognized {traversal_type=}")
    return ccs
