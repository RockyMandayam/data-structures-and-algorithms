from collections.abc import Hashable

from dsa.graphs.analysis.traversal.dfs import dfs
from dsa.graphs.analysis.traversal_type import TraversalType
from dsa.graphs.digraph import Digraph


def topological_sort(
    dg: Digraph, traversal_type: TraversalType = TraversalType.DFS
) -> list[Hashable]:
    """Topologically sort a digraph; raises error if digraph is cyclic.

    NOTE: only traversal types DFS and BFS are allowed!
    """
    if traversal_type == TraversalType.DFS:
        func = _dfs_topological_sort
    elif traversal_type == TraversalType.BFS:
        # can't use the typical BFS algorithm natively (AFIAK) to get the topological order
        # have to use Kahn's algorithm instead, which is still "BFS" in its node processing order
        func = _kahn_topological_sort
    else:
        raise ValueError(f"{traversal_type=} must be DFS or BFS")
    return func(dg)


def _dfs_topological_sort(dg: Digraph) -> list[Hashable]:
    _, _, _, postorder, _, _, directed_is_cyclic = dfs(dg, recursive=True)
    if directed_is_cyclic:
        raise ValueError("Given digraph is cyclic; cannot topologically sort it.")
    return postorder[::-1]


def _kahn_topological_sort(dg: Digraph) -> list[Hashable]:
    remaining_in_degrees = {u: dg.get_in_degree(u) for u in dg}
    queue = [u for u, deg in remaining_in_degrees.items() if deg == 0]
    sorted_nodes = []
    while queue:
        u = queue.pop(0)
        sorted_nodes.append(u)
        for v in dg[u]:
            remaining_in_degrees[v] -= 1
            if remaining_in_degrees[v] == 0:
                queue.append(v)
    if len(sorted_nodes) == len(dg):
        return sorted_nodes
    else:
        raise ValueError("Given digraph is cyclic; cannot topologically sort it.")
