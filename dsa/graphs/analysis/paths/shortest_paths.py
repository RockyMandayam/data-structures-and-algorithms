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
    if all(g.get_weight(edge) >= 0 for edge in g.get_edges()):
        if weighted:
            parents, *_ = dijkstra(g)
        else:
            parents, *_ = bfs(g)
    else:
        parents = _bellman_ford(g, s)
    return parents


def _bellman_ford(g: Graph, s: Hashable) -> dict[Hashable, Hashable]:
    eps = 10e-6
    parents = {s: None}
    dists = {s: 0}
    for _ in range(len(g) - 1):
        updated = _relax_all_edges(g, parents, dists, eps)
        if not updated:
            break
    if not updated:
        return parents
    updated = _relax_all_edges(g, parents, dists, eps)
    if updated:
        raise ValueError(
            "Reachable part of the graph contains negative cycles; shortest paths are ill-defined"
        )
    return parents


def _relax_all_edges(g: Graph, parents: dict, dists: dict, eps: float) -> bool:
    updated = False
    for u in g:
        for v in g[u]:
            w = g.get_weight((u, v))
            curr_dist = dists[u] if u in dists else float("inf")
            alt_dist = dists[v] + w if v in dists else float("inf")
            if alt_dist < curr_dist - eps:
                dists[u] = alt_dist
                parents[u] = v
                updated = True
    return updated
