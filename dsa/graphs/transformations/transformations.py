from dsa.graphs.digraph import Digraph


def reverse(dg: Digraph) -> Digraph:
    """Returns a new digraph which is the same as the input but with all edge directions reversed."""
    return Digraph(
        nodes=dg.get_nodes(),
        edges={(v, u): tup for (u, v), tup in dg.get_edges().items()},
    )
