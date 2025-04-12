from collections.abc import Hashable, Sequence

from dsa.graphs.analysis.traversal.order import Order
from dsa.graphs.analysis.traversal.utils import (
    get_ordered_neighbors,
    get_ordered_seed_nodes,
)
from dsa.graphs.graph import Graph


def bfs(
    g: Graph,
    *,
    seed_order: Order | Hashable | Sequence[Hashable] | None = None,
    neighbor_order: Order | None = Order.SORTED,
    use_approach_1: bool = True,
) -> tuple[
    dict[Hashable, Hashable],
    dict[Hashable, float],
    list[Hashable],
    list[list[Hashable]],
    bool,
]:
    """Breadth first search (BFS) implementation.

    This is somewhat similar to DFS. It could potentially be implemented in the same function. But because of the different return
    types (preorder and postorder vs levelorder), and the fact that the 'recursive' kwarg only makes sense (as of now)
    for DFS, I chose to do it separately.

    Args:
        g: Graph on which to perform DFS
        seed_order: Order in which to iterate through potential start nodes for DFS exploration.
            - If Order, iterate through potential in the given Order
            - If non-Sequence Hashable, first start with the given Hashable (node); rest of order is undetermined
            - If Sequence[Hashable] (sequence of nodes), iterate in the order given by the sequence.
            - NOTE: If seed_order is Hashable and also Sequence[Hashable], it'll be interpreted as Hashable (node)
        neighbor_order: optional order in which to explore neighbors of a node; if not provided, undetermined order.

    Returns:
        dict[Hashable, float]: map from node to the distance from its seed to the node
        dict[Hashable, Hashable]: parents dict which encodes the traversal tree
        list[Hashable]: level order of nodes in the BFS traversal
        list[list[Hashable]]: List of connected components (CC), where each CC is a list of nodes, with the same order
            as the level order of the BFS traversal.
        bool: if the graph is undirected, True if graph contains cycle; False otherwise
    """
    seed_nodes = get_ordered_seed_nodes(g, seed_order)

    parents = {}
    dists = {}
    reached = set()
    levelorder = []
    ccs = []
    undirected_contains_cycle = False
    for u in seed_nodes:
        if u not in reached:
            (
                parents_from_u,
                dists_from_u,
                levelorder_from_u,
                undirected_contains_cycle_from_u,
            ) = bfs_from(g, u, neighbor_order, reached, use_approach_1=use_approach_1)
            parents.update(parents_from_u)
            dists.update(dists_from_u)
            levelorder.extend(levelorder_from_u)
            ccs.append(levelorder_from_u)
            undirected_contains_cycle = (
                undirected_contains_cycle or undirected_contains_cycle_from_u
            )
    return parents, dists, levelorder, ccs, undirected_contains_cycle


# TODO test this separately
def bfs_from(
    g: Graph,
    u: Hashable,
    neighbor_order: Order | None,
    reached: set | None = None,
    use_approach_1: bool = True,
) -> tuple[dict[Hashable, Hashable], dict[Hashable, float], list[Hashable], bool]:
    _bfs_from: Callable = (
        _bfs_from_approach_1 if use_approach_1 else _bfs_from_approach_2
    )
    if reached is None:
        reached = set()
    return _bfs_from(g, u, neighbor_order, reached)


def _bfs_from_approach_1(
    g: Graph,
    u: Hashable,
    neighbor_order: Order | None,
    reached: set,
) -> tuple[list[Hashable], dict[Hashable, float], list[Hashable], bool]:
    """Same as the iterative DFS implementation without the "hack" added to get the postorder, except
    use a queue instead of a stack (well, use a list in both cases, but do pop(0) instead of pop(-1) here),
    AND only update parents if a node isn't already in it.

    In this approach (approach 1), we replace the "if v not in reached" with "if v not in parents" to achieve
    the goal of only updating parents if a ndoe isn't already in it. The keys of parents serve as a "seen"
    set, which is all the reached nodes plus the nodes in the queue that haven't been popped yet (i.e., they're
    "seen" but not "reached").

    Instead of marking a node as reached when we pop it off the queue, we could mark a node as reached when
    we add it to the queue. However, this means the seed node would need to be marked as reached by the caller,
    and I think this is messier. I think keeping the idea of "reached" as "popped off the queue" is easier to
    understand, and also generalizes better to Dijkstra. But then again, the downside of this scheme is that
    it doesn't vibe well with reached. I.e., a node is not reached and yet at that point it's enqueued, its
    parent is set!
    """
    parents = {u: None}
    dists = {u: 0}
    to_explore = [u]
    levelorder = []
    undirected_contains_cycle = False
    while to_explore:
        u = to_explore.pop(0)
        # don't need to do "continue if u in reached" since a node never gets added twice to the queue
        reached.add(u)
        levelorder.append(u)
        for v in get_ordered_neighbors(g, u, neighbor_order):
            if v not in parents:
                parents[v] = u
                dists[v] = dists[u] + 1
                to_explore.append(v)
            else:
                undirected_contains_cycle = undirected_contains_cycle or v != parents[u]
    return parents, dists, levelorder, undirected_contains_cycle


def _bfs_from_approach_2(
    g: Graph,
    u: Hashable,
    neighbor_order: Order | None,
    reached: set,
) -> tuple[dict[Hashable, Hashable], dict[Hashable, float], list[Hashable], bool]:
    """Same as the iterative DFS implementation without the "hack" added to get the postorder, except
    use a queue instead of a stack (well, use a list in both cases, but do pop(0) instead of pop(-1) here),
    AND only update parents if a node isn't already in it.

    In this approach (approach 2), we use "reached" to really mean more like "seen", i.e., the keys of parents.
    In fact, we don't even need reached for this traversal, but I'm just keeping it for consistency. Theoretically,
    the caller could completely remove reached and just check if a node is in parents... And it just keeps it
    more consistent with the DFS implementation.
    """
    parents = {u: None}
    dists = {u: 0}
    to_explore = [u]
    levelorder = []
    reached.add(u)
    undirected_contains_cycle = False
    while to_explore:
        u = to_explore.pop(0)
        levelorder.append(u)
        for v in get_ordered_neighbors(g, u, neighbor_order):
            if v not in reached:
                parents[v] = u
                dists[v] = dists[u] + 1
                to_explore.append(v)
                reached.add(v)
            else:
                undirected_contains_cycle = undirected_contains_cycle or v != parents[u]
    return parents, dists, levelorder, undirected_contains_cycle
