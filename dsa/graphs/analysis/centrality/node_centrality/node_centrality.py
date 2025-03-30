from collections.abc import Hashable

from dsa.graphs.graph import Graph


def get_degree_centrality(g: Graph, u: Hashable, normalized: bool = True) -> float:
    """Return the normalized (divided by number_of_nodes - 1) degree centrality of node u in graph g."""
    deg = g.get_degree(u)
    if normalized:
        deg = deg / (len(g) - 1)
    return deg


# TODO test this
def get_sorted_degree_centralities(g: Graph, normalized: bool = True) -> float:
    degs = [get_degree_centrality(g, u, normalized=normalized) for u in g]
    degs.sort()
    return degs
