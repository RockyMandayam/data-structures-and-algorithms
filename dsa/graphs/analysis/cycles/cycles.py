from dsa.disjoint_sets.disjoint_sets import DisjointSets
from dsa.graphs.analysis.traversal.bfs import bfs
from dsa.graphs.analysis.traversal.dfs import dfs
from dsa.graphs.analysis.traversal.dijkstra import dijkstra
from dsa.graphs.analysis.traversal_type import TraversalType
from dsa.graphs.graph import Graph


def contains_cycle(
    g: Graph, traversal_type: TraversalType | None = TraversalType.DFS
) -> bool:
    """Returns False if graph contains a cycle; False otherwise

    traversal_type indicates which traversal type (DFS, BFS, etc.) to use if using the graph search based cycle detection algorithm. If
    traversal_type is None, this function instead uses the disjoint sets based cycle detection algorithm.
    """
    if traversal_type is None:
        return _contains_cycle_using_disjoint_sets(g)
    else:
        return _contains_cycle_using_graph_traversal(g, traversal_type)


def _contains_cycle_using_graph_traversal(
    g: Graph, traversal_type: TraversalType
) -> bool:
    if traversal_type == TraversalType.DFS:
        *_, contains_cycle, _ = dfs(g)
    elif traversal_type == TraversalType.BFS:
        *_, contains_cycle = bfs(g)
    elif traversal_type == TraversalType.DIJKSTRA:
        *_, contains_cycle = dijkstra(g)
    else:
        raise ValueError(f"Unrecognized {traversal_type=}.")
    return contains_cycle


def _contains_cycle_using_disjoint_sets(g: Graph) -> bool:
    ds = DisjointSets(g.get_nodes())
    for u, v in g.get_edges():
        if ds.is_connected(u, v):
            return True
        ds.connect(u, v)
    return False
