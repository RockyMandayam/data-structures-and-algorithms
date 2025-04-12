from collections.abc import Hashable

from dsa.graphs.analysis.traversal.bfs import bfs
from dsa.graphs.analysis.traversal.dfs import dfs
from dsa.graphs.analysis.traversal.dijkstra import dijkstra
from dsa.graphs.analysis.traversal_type import TraversalType
from dsa.graphs.digraph import Digraph
from dsa.graphs.graph import Graph
from dsa.graphs.transformations.transformations import reverse
from dsa.utils import get_key_to_index


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
        *_, ccs, _, _ = dfs(g)
    elif traversal_type == TraversalType.BFS:
        *_, ccs, _ = bfs(g)
    elif traversal_type == TraversalType.DIJKSTRA:
        *_, ccs, _ = dijkstra(g)
    else:
        raise ValueError(f"Unrecognized {traversal_type=}")
    return ccs


def is_strongly_connected(dg: Digraph) -> bool:
    return len(get_strongly_connected_components(dg)) == 1


def get_strongly_connected_components(dg: Digraph) -> list[list[Hashable]]:
    """Get strongly connected components in a digraph using Kosaraju's algorithm."""
    _, _, _, postorder, *_ = dfs(reverse(dg))
    sink_to_src_order = postorder[::-1]
    # now I need to call DFS, with seed order and neighbor order determiend by sink_to_src_order
    node_to_index = get_key_to_index(sink_to_src_order)
    *_, ccs, _, _ = dfs(
        dg, seed_order=sink_to_src_order, neighbor_order=lambda u: node_to_index[u]
    )
    return ccs
