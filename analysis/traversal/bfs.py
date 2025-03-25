from collections.abc import Hashable, Sequence

from graphs.analysis.traversal.order import Order
from graphs.analysis.traversal.utils import (
    get_ordered_neighbors,
    get_ordered_seed_nodes,
)
from graphs.graph import Graph


def bfs(
    g: Graph,
    *,
    seed_order: Order | Hashable | Sequence[Hashable] | None = None,
    neighbor_order: Order | None = Order.SORTED,
    use_approach_1: bool = True,
) -> tuple[list[Hashable], dict[Hashable, Hashable], list[list[Hashable]]]:
    """Breadth first search (BFS) implementation.

    This is VERY similar to DFS. It could be implemented in the same function. But because of the different return
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
        list[Hashable]: level order of nodes in the BFS traversal
        dict[Hashable, Hashable]: parents dict which encodes the traversal tree
        list[list[Hashable]]]: list of lists of nodes where each nested list is all nodes reached from one seed, i.e.
            one call to _bfs_from. For undirected graphs, each nested list is one connected component
    """
    seed_nodes = get_ordered_seed_nodes(g, seed_order)

    reached = set()
    levelorder = []
    parents = {}
    reached_from_seeds = []
    for u in seed_nodes:
        if u not in reached:
            _bfs_from: Callable = (
                _bfs_from_approach_1 if use_approach_1 else _bfs_from_approach_2
            )
            parents_from_u, levelorder_from_u = _bfs_from(g, u, neighbor_order, reached)
            parents.update(parents_from_u)
            levelorder.extend(levelorder_from_u)
    return levelorder, parents, reached_from_seeds


def _bfs_from_approach_1(
    g: Graph,
    u: Hashable,
    neighbor_order: Order | None,
    reached: set,
) -> tuple[list[Hashable], list[Hashable], dict[Hashable, Hashable]]:
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
    to_explore = [u]
    levelorder = []
    while to_explore:
        u = to_explore.pop(0)
        if u in reached:
            continue
        reached.add(u)
        levelorder.append(u)
        for v in get_ordered_neighbors(g, u, neighbor_order):
            # in DFS, we do "if v not in reached"
            # parents serves as a "seen" set. BFS relies on concept of "seen" not "reached"
            # but at least for now, I find "reached" a cleaner concept
            if v not in parents:
                parents[v] = u
                to_explore.append(v)
    return parents, levelorder


def _bfs_from_approach_2(
    g: Graph,
    u: Hashable,
    neighbor_order: Order | None,
    reached: set,
) -> tuple[list[Hashable], list[Hashable], dict[Hashable, Hashable]]:
    """Same as the iterative DFS implementation without the "hack" added to get the postorder, except
    use a queue instead of a stack (well, use a list in both cases, but do pop(0) instead of pop(-1) here),
    AND only update parents if a node isn't already in it.

    In this approach (approach 2), we use "reached" to really mean more like "seen", i.e., the keys of parents.
    In fact, we don't even need reached for this traversal, but I'm just keeping it for consistency. Theoretically,
    the caller could completely remove reached and just check if a node is in parents... And it just keeps it
    more consistent with the DFS implementation.
    """
    parents = {u: None}
    to_explore = [u]
    levelorder = []
    reached.add(u)
    while to_explore:
        u = to_explore.pop(0)
        levelorder.append(u)
        for v in get_ordered_neighbors(g, u, neighbor_order):
            if v not in reached:
                parents[v] = u
                to_explore.append(v)
                reached.add(v)
    return parents, levelorder
