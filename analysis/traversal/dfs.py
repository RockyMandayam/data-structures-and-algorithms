from collections.abc import Callable, Hashable, Mapping, Sequence
from typing import Any

from graphs.analysis.traversal.order import Order
from graphs.analysis.traversal.utils import get_ordered_seed_nodes
from graphs.graph import Graph


# TODO: max_depth
# TODO: goal neighbor
# TODO: allow specifying partial list of seed nodes?
def dfs(
    g: Graph,
    *,
    recursive: bool = False,
    seed_order: Order | Hashable | Sequence[Hashable] | None = None,
    neighbor_order: Order | None = Order.SORTED,
) -> tuple[Sequence, Sequence, Mapping[Hashable, Hashable]]:
    """Depth first search (DFS) implementation.

    The recursive and iterative versions both have an inital overall "iterative" part, but beyond that they diverge
    when starting to explore a node.

    Args:
        g: Graph on which to perform DFS
        recursive: if True, use recursive DFS implementation; otherwise, use iterative DFS implementation
        seed_order: Order in which to iterate through potential start nodes for DFS exploration.
            - If Order, iterate through potential in the given Order
            - If non-Sequence Hashable, first start with the given Hashable (node); rest of order is undetermined
            - If Sequence[Hashable] (sequence of nodes), iterate in the order given by the sequence.
            - NOTE: If seed_order is Hashable and also Sequence[Hashable], it'll be interpreted as Hashable (node)
        neighbor_order: optional order in which to explore neighbors of a node; if not provided, undetermined order.

    Returns:
        Sequence: preorder corresponding to the particular traversal this DFS takes
        Sequence: postorder corresponding to the same traversal
        Mapping[Hashable, Hashable]: path parents map, a map from each node to its parent in the DFS tree,
            or to None if it has no parent in the DFS tree (i.e., if it served as a seed node)
    """
    seed_nodes = get_ordered_seed_nodes(g, seed_order)

    reached = set()
    preorder = []
    postorder = []
    parents = {}
    for u in seed_nodes:
        if u not in reached:
            parents[u] = None
            if recursive:
                _dfs_from_recursive(
                    g, u, neighbor_order, reached, preorder, postorder, parents
                )
            else:
                _dfs_from_iterative(
                    g, u, neighbor_order, reached, preorder, postorder, parents
                )
    return preorder, postorder, parents


def _dfs_from_recursive(
    g: Graph,
    u: Hashable,
    neighbor_order: Order | None,
    reached: set,
    preorder: list[Hashable],
    postorder: list[Hashable],
    parents: Mapping[Hashable, Hashable],
) -> None:
    """Recursive exploration

    NOTE: Instead of doing reached.add(u) as the first thing when you explore a node, you can instead do it before calling
    _dfs_from_recursive. So for v in vs, if v not in reached, first reached.add(v), then recursively call _dfs_from_recursive.
        - Benefit: The benefit of this is that it better tracks with when we set parents (before we recurse).
        - Drawback: Biggest drawback is that now you have to do a reached.add(u) before calling _dfs_from_recursive at the
            higher level from dfs(). Also, this now tracks less well with when we add to preorder. We can also add to
            preorder when we recurse on neighbors, but then similarly we'll have to do preorder.append(u) before calling
            _dfs_from_recursive at the higher level from dfs()
    So overall, these other schemes just don't work as nicely. So I'll keep reached and preorder where they are, and just
    know that the parents mapping is populated in a different way. Since the start node has no parent, you'd think we don't
    need to modify the call to _dfs_from_recursive from dfs(), but we do, in order to set its parent to None. Alternatively,
    you could just have it not be present in the mapping, but I'll just choose the convention that a start node's parent
    is None. At least this change is the same for the recursive and iterative implementations though!
    """
    reached.add(u)
    preorder.append(u)
    vs = [v for v in g[u]]
    if neighbor_order:
        vs.sort(reverse=(neighbor_order == Order.REVERSE_SORTED))
    for v in vs:
        if v not in reached:
            print("###")
            print(u)
            print(v)
            print(g.is_edge((u, v)))
            parents[v] = u
            _dfs_from_recursive(
                g, v, neighbor_order, reached, preorder, postorder, parents
            )
    postorder.append(u)


def _dfs_from_iterative(
    g: Graph,
    u: Hashable,
    neighbor_order: Order | None,
    reached: set,
    preorder: list[Hashable],
    postorder: list[Hashable],
    parents: Mapping[Hashable, Hashable],
) -> None:
    """Iterative implementation of DFS node exploration.

    First, let's discuss the overall idea, without considering preorder and postorder. For simplicity, let's first consider the case of a
    binary tree. In the recursive version, we use the recursion itself plus the for loop (for v in neighbors) to basically track which
    nodes we want to explore. In this iterative version, we need some kind of data structure that we add nodes to as we go. Since we want a
    DEPTH first search, we should use a stack. Then, the most recently added nodes (as we go deeper, these will be the deepest nodes), will
    get popped out first. We can start with stack = [root]. Then we pop(-1), and we can add the children to the stack. So now
    stack = [root.left, root.right]. But wait! If we pop now, we get root.right. But assuming we want sorted order, we want root.left. So
    we actually add it in reverse of the order we actually want! So we add root.right, then root.left, so we get stack = [root.right, root.left].
    Now we pop(-1), and we get root.left. Now notice that everything added from here on out until we pop root.right, will be descendents of
    root.left. Great! We're done.

    What about preorder? Well, when you pop(-1), you just add it to the preorder, since that's exactly the
    order you get with recursive preorder!

    What if it's a non-binary tree? Same idea, just instead of adding root.right then root.left, you generally just add the child nodes to
    stack in the reverse of the order you want to explore.

    What if it's not a tree at all? Well, you just want to make sure not to reach nodes you've already reached. So just use the reached set
    as before. When you pop off the stack, mark the node as reached. Then, in the future, only add a child to the stack if it has not
    already been reached. You have to ALSO check if it's already been reached when you pop(-1). Why? Well, due to there being multiple
    paths to the same node, it can get added repeatedly to the stack, and when you pop off the final one, you'll mark it as reached, but
    when you get to earlier instances of that node in the stack, it'll already be reached, even though it wasn't at the time it was added
    to the stack! Now you may ask, if you're going to check if it's already reached when popping off the stack, why even check when
    adding it to the stack? Well, first thought is, it'll make the stack size shorter. But actually, it's more important than that. If
    you don't check while adding to stack, you can recurse infinitely! Just consider the two-node graph with one edge. You'll start at
    node 1, pop it and mark it reached, then add its neighbor node 2 to the stack. Then you'll pop node 2 and mark it reached, and add
    node 1 (since you don't check if it's reached before adding it to the stack). And this will go on forever. Instead, you should not
    add node 1 to the stack after reaching node 2!

    What about postorder? Turns out this is quite tricky. There are a few ways to consider solving this problem. Let's go over them.
        - Can we get the postorder from the preorder?
            - In general, no.
            - For undirected graphs it turns out that the reverse preorder is in fact a valid postorder but they do not CORRESPOND.
                I.e., the reverse preorder is a valid postorder but it (usually) corresponds to the postorder you'd get if you did
                a DIFFERENT traversal than the one that gave the preorder.
            - Also, this approach does not work for directed graphs. Consider a simple diamond graph A->B, A->C, B->D, C->D.
            - So for both those reasons, I will not take this approach here. But there are implementations of this online, and due to
                above reasons, the ones I've seen work with undirected graphs and don't return a "matching" preorder+postorder pair.
                And, they often implement it on a tree, specifically a rooted binary tree, but with a set of reached/visited nodes, it
                should work with any undirected tree.
            - NOTE: if you search up "two stack" implementations of post order with "iterative" dfs, you'll get results that are about
                this algorithm. The first stack is the normal stack used to track which nodes to reach, while the second stack is literally
                just the preorder. They then reverse it at the end, but literally it's just the preorder iterative DFS solution and then
                they reverse the preorder.
            - References:
                - https://cs.stackexchange.com/questions/151687/are-reversed-reverse-preorder-traversals-equivalent-to-a-postorder-traversal
                - https://www.youtube.com/watch?v=qT65HltK2uE
                - https://www.youtube.com/watch?v=2YBhNLodD8Q
        - Only remove a node when it's been "visited twice":
            - NeetCode does a version for a tree here: https://www.youtube.com/watch?v=QhszUQhGGlA
                - But this is for a tree. If you want it to work more generally (i.e., on cyclic graphs), you can't just use a visited stack:
                    - You have to use a visited set, not stack. In the tree version, a node only gets added to the stack once (and you add
                        False to visited), then popped (along with the False visited) and immediately re-added to the stack (and you add
                        True to visited). However, with a cyclic graph, it can be added multiple times to the stack, and the re-added trick
                        only occurs at the last addition, and when you get to the earlier additions, the corresponding visited element will
                        be False, and you won't know that it's already been processed. So you should use a visited set that keeps track of
                        all visited nodes.
                    - You have to use a double_visited set. Why? For the same reason. There are cycles, so a node can be added multiple times
                        to the stack. It gets added the first time, and then perhaps times after that, all the while node is not in visited.
                        Then, it gets popped up, and you see it's not in visited. So you mark it as visited, and re-add it to the stack, and
                        add all its children. Then the next time you see this node, it's already visited, so you add it to the postorder. So
                        far, so good. BUT. Remember how it was initially added potentially multiple times? So if you keep popping off the
                        stack, you may eventually pop off that node AGAIN. Now, you don't want to add to postorder since that'll be double
                        counting! You could of course just check if node in postorder, BUT that's slow (O(N) each time), so instead it's
                        better to keep a double_visited set. Now, the second time you see the node, i.e., the first time you see it after
                        it's been visited already, i.e., when you add it to postorder,  you also add it to double_visited. Then, for all
                        future times, you check if it's in double_visited, and if it is (which it will be), don't add it to post_order. Think
                        this is awkward since we have a double_visited set and postorder list which track exactly the same nodes? Sure. But
                        also, that's exactly also true of the visited set and the preorder list (they track the same nodes). One is good for
                        instant lookup and one is good for returning an order
                    - Minor implementation detail: I think you could use a visited_count dict that counts whether it's been visited 0, 1, or 2
                        times, instead of two sets. Idk if it's easier/more elegant or less so... just a thought.
                    - Another minor implementation detail is you can do a peek followed by a pop sometimes instead of a pop followed by a
                        re-append sometimes.
                    - There's also a way to not use a double_visited list but instead, when a node is already reached, just check whether all
                        its neighbors are already reached. But, of course, this is just slower. double_visited just makes this check constant
                        time basically.
            - the double_visited set is only used for the iterative DFS implementation, not the recursive DFS impilementation. So do we create
                a double_visited set up in the DFS function and only pass it in to the iterative version and not the recursive version? Well,
                no. double_visited is used to differentiate reached from reached twice among a node and all its descendents in the DFS tree.
                Note that _dfs_from_iterative won't be called on an already reached node. It'll only be called on an unreached node. However,
                with directed graphs, it's possible that a descendent of the start node of _dfs_from_iterative is in fact already reached.
                But in that case, that descendent will have also already been double_reached. By the end of a _dfs_from_iterative call, any
                node that is reached will also be double reached. So the DFS parent function can only use reached, and we can keep a separate
                "local" double_reached set within _dfs_from_iterative that other functions don't have to be aware of. But reached still needs
                to be shared.
        - TODO: check out https://www.youtube.com/watch?v=xLQKdq0Ffjg
    """
    double_reached = set()
    to_explore = [u]
    while to_explore:
        u = to_explore.pop(-1)
        if u in reached:
            # this if block is only used for postorder
            if u not in double_reached:
                double_reached.add(u)
                postorder.append(u)
            continue
        to_explore.append(u)  # this is only used for postorder
        reached.add(u)
        preorder.append(u)
        vs = [v for v in g[u]]
        if neighbor_order:
            # we want to add to stack in reverse order of order of exploration
            vs.sort(reverse=(neighbor_order != Order.REVERSE_SORTED))
        for v in vs:
            if v not in reached:
                parents[v] = u
                to_explore.append(v)
