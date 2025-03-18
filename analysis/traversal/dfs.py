from collections.abc import Callable, Hashable, Sequence
from enum import Enum, auto
from typing import Any

from graphs.graph import Graph


class Order(Enum):
    SORTED = auto()
    REVERSE_SORTED = auto()


# TODO: max_depth
# TODO: goal neighbor
# TODO: return paths
# TODO: from only one source
def dfs_recursive(
    g: Graph,
    seed_order: Order | Sequence[Hashable] | None = None,
    neighbor_order: Order | None = Order.SORTED,
) -> tuple[Sequence, Sequence]:
    """Recursive implementation of DFS.

    In general, to help with intuition, I maintain two separate concepts of "exploring" a node vs "finalizing" a node:
        - explore a node: for each of the node's neighbors, potentially add it to the queue of nodes to finalize
        - finalize a node: consider a node "visited" and the the path to it finalized
    In a recursive DFS algorithm, they coincide. Recursing on a node is both finalization and exploration.
    When you explore a node, you finalize it AND recurse on each of its non-finalized neighbors!
    Therefore, I use a single explored_and_finalized set to track the set of explored/finalized nodes.
    """
    if isinstance(seed_order, Sequence) and (
        len(seed_order) != len(g) or set(seed_order) != set(g.get_nodes())
    ):
        raise ValueError(
            f"When providing seed_order as sequence, it must include every node in g exactly once. Received {seed_order=}. Expected {g.get_nodes()=}"
        )
    explored_and_finalized = set()
    preorder = []
    postorder = []
    if isinstance(seed_order, Sequence):
        seed_nodes = seed_order
    else:
        seed_nodes = list(g.get_nodes())
        if seed_order:
            seed_nodes.sort(reverse=(seed_order == Order.REVERSE_SORTED))
    for u in seed_nodes:
        if u not in explored_and_finalized:
            _explore_recursive(
                g, u, neighbor_order, explored_and_finalized, preorder, postorder
            )
    return preorder, postorder


def _explore_recursive(
    g: Graph,
    u: Hashable,
    neighbor_order: Order | None,
    explored_and_finalized: set,
    preorder: list[Hashable],
    postorder: list[Hashable],
) -> None:
    explored_and_finalized.add(u)
    preorder.append(u)
    vs = [v for v in g[u]]
    if neighbor_order:
        vs.sort(reverse=(neighbor_order == Order.REVERSE_SORTED))
    for v in vs:
        if v not in explored_and_finalized:
            _explore_recursive(
                g, v, neighbor_order, explored_and_finalized, preorder, postorder
            )
    postorder.append(u)
