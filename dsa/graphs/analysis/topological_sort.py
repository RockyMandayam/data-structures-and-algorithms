from collections.abc import Hashable

from dsa.graphs.analysis.traversal.dfs import dfs
from dsa.graphs.digraph import Digraph


def topological_sort(dg: Digraph) -> list[Hashable]:
    """Topologically sort a digraph; raises error if digraph is cyclic."""
    _, _, _, postorder, _, _, directed_is_cyclic = dfs(dg, recursive=True)
    if directed_is_cyclic:
        raise ValueError("Given digraph is cyclic; cannot topologically sort it.")
    return postorder[::-1]
