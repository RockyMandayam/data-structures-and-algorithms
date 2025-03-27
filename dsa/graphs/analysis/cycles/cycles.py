from dsa.graphs.analysis.traversal.bfs import bfs
from dsa.graphs.analysis.traversal.dfs import dfs
from dsa.graphs.analysis.traversal_type import TraversalType
from dsa.graphs.graph import Graph


def contains_cycle(g: Graph, traversal_type: TraversalType = TraversalType.DFS) -> bool:
    """Returns False if graph contains a cycle; False otherwise"""
    if traversal_type == TraversalType.DFS:
        *_, contains_cycle = dfs(g)
    elif traversal_type == TraversalType.BFS:
        *_, contains_cycle = bfs(g)
    else:
        raise ValueError(f"Unrecognized {traversal_type=}.")
    return contains_cycle
