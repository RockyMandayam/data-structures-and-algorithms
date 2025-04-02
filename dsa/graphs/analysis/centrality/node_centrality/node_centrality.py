from collections.abc import Hashable

import numpy as np

from dsa.graphs.analysis.connected_components.connected_components import is_connected
from dsa.graphs.digraph import Digraph
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


# TODO test this
def get_eigvec_centrality(g: Graph, u: Hashable, normalization: str = "l1") -> float:
    """Return the normalized eigenvector centrality measure of node u in graph g. If you want all centralities,
    call get_eigvec_centralities, since that is more efficient.

    Normalized means the sum of
    NOTE: A ValueError is raised if g isn't connected, since eigenvector centrality is only well-defined for connected graphs.
    """
    eigvec_centralities = get_eigvec_centralities(g, normalization=normalization)
    u_index = g.get_default_index_in_A(u)
    return eigvec_centralities[u_index]


def get_eigvec_centralities(g: Graph, normalization: str = "l1") -> list[float]:
    """Return the normalized eigenvector centrality measures in graph g.

    Normalized means most central node has centrality of 1.
    NOTE: A ValueError is raised if g isn't connected, since eigenvector centrality is only well-defined for connected graphs.
    """
    if normalization not in ("l1", "l2"):
        raise ValueError(f"Unrecognized {normalization=}")
    if not is_connected(g):
        raise ValueError(
            "g must be connected for eigenvector centrality to be well-defined."
        )
    A = np.array(g.A)
    eigvals, eigvecs = np.linalg.eig(A)
    max_eigval_index = eigvals.argmax()
    eigvec_for_max_eigval = eigvecs[:, max_eigval_index]
    if eigvec_for_max_eigval[0] < 0:
        # we want all positive, not all negative
        eigvec_for_max_eigval = -eigvec_for_max_eigval
    if normalization == "l1":
        # don't need to do abs value since all elements are non-negative
        eigvec_for_max_eigval = eigvec_for_max_eigval / np.sum(eigvec_for_max_eigval)
    else:
        eigvec_for_max_eigval = eigvec_for_max_eigval / np.linalg.norm(
            eigvec_for_max_eigval
        )
    return list(eigvec_for_max_eigval)


def get_in_degree_centrality(
    dg: Digraph, u: Hashable, normalized: bool = True
) -> float:
    """Return the normalized (divided by number_of_nodes - 1) degree centrality of node u in graph g."""
    deg = dg.get_in_degree(u)
    if normalized:
        deg = deg / (len(dg) - 1)
    return deg


# TODO test this
def get_sorted_in_degree_centralities(dg: Digraph, normalized: bool = True) -> float:
    degs = [get_in_degree_centrality(dg, u, normalized=normalized) for u in dg]
    degs.sort()
    return degs


def get_out_degree_centrality(
    dg: Digraph, u: Hashable, normalized: bool = True
) -> float:
    """Return the normalized (divided by number_of_nodes - 1) degree centrality of node u in graph g."""
    deg = dg.get_out_degree(u)
    if normalized:
        deg = deg / (len(dg) - 1)
    return deg


# TODO test this
def get_sorted_out_degree_centralities(dg: Digraph, normalized: bool = True) -> float:
    degs = [get_out_degree_centrality(dg, u, normalized=normalized) for u in dg]
    degs.sort()
    return degs
