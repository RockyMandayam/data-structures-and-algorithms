import random

import pytest

from graphs.analysis.traversal.dfs import Order, dfs_recursive
from graphs.graph import Graph
from graphs.graph_factory import GraphFactory

# TODO why is this so slow with 2**big_number
MAX_TEST_GRAPH_SIZE = 2**8


def test_dfs_recursive() -> None:
    # non-comparable nodes
    g = Graph(nodes=(12, "blah"), edges=((12, "blah"),))
    with pytest.raises(TypeError):
        dfs_recursive(g, seed_order=Order.SORTED)

    ### simple graphs

    # empty graph
    g = Graph()
    pre, post = dfs_recursive(g)
    assert pre == []
    assert post == []

    # singleton graph
    g = Graph(nodes=1)
    pre, post = dfs_recursive(g)
    assert pre == [0]
    assert post == [0]

    # generally: n nodes, 0 edges
    for n in (2, 3, random.randint(4, MAX_TEST_GRAPH_SIZE)):
        g = Graph(nodes=n)
        # seeds in sorted order
        pre, post = dfs_recursive(g, seed_order=Order.SORTED)
        assert pre == list(range(n)), n
        assert post == pre, n
        # seeds in reverse sorted order
        pre, post = dfs_recursive(g, seed_order=Order.REVERSE_SORTED)
        assert pre == list(range(n - 1, -1, -1)), n
        assert post == pre, n

    ### spindly trees

    # generally: n node spindly tree
    for n in (2, 3, random.randint(4, MAX_TEST_GRAPH_SIZE)):
        g = GraphFactory.create_spindly_tree(n)
        # need to specify order to have deterministic pre/post
        # in sorted order
        pre, post = dfs_recursive(g, seed_order=Order.SORTED)
        assert pre == list(range(n)), n
        assert post == pre[::-1]
        # in reverse sorted order
        pre, post = dfs_recursive(g, seed_order=Order.REVERSE_SORTED)
        assert pre == list(range(n - 1, -1, -1)), n
        assert post == pre[::-1]
        # branch from the middle
        dfs_root = random.randint(1, n - 1)
        to_left = list(range(dfs_root - 1, -1, -1))  # from middle to the left
        to_right = list(range(dfs_root + 1, n))  # from middle to the right
        # important that dfs_root is first; everything else is irrelevant
        seed_order = [dfs_root, *to_left, *to_right]
        # explore left then right
        pre, post = dfs_recursive(g, seed_order=seed_order, neighbor_order=Order.SORTED)
        assert pre == [dfs_root, *to_left, *to_right]
        assert post == [*to_left[::-1], *to_right[::-1], dfs_root]
        # explore right then left
        pre, post = dfs_recursive(
            g, seed_order=seed_order, neighbor_order=Order.REVERSE_SORTED
        )
        assert pre == [dfs_root, *to_right, *to_left]
        assert post == [*to_right[::-1], *to_left[::-1], dfs_root]

    ### binary trees

    # simple binary tree (see create_b_ary_tree docstring for example)
    g = GraphFactory.create_b_ary_tree(2, 2)
    # starting from 0, neighbors in sorted order
    pre, post = dfs_recursive(g, seed_order=Order.SORTED, neighbor_order=Order.SORTED)
    assert pre == [0, 1, 3, 4, 2, 5, 6]
    assert post == [3, 4, 1, 5, 6, 2, 0]
    # starting from 0, neighbors in reverse order
    pre, post = dfs_recursive(
        g, seed_order=Order.SORTED, neighbor_order=Order.REVERSE_SORTED
    )
    assert pre == [0, 2, 6, 5, 1, 4, 3]
    assert post == [6, 5, 2, 4, 3, 1, 0]
    # starting from 6, neighbors in sorted order
    pre, post = dfs_recursive(
        g, seed_order=Order.REVERSE_SORTED, neighbor_order=Order.SORTED
    )
    assert pre == [6, 2, 0, 1, 3, 4, 5]
    assert post == [3, 4, 1, 0, 5, 2, 6]
    # starting from 6, neighbors in reverse order
    pre, post = dfs_recursive(
        g, seed_order=Order.REVERSE_SORTED, neighbor_order=Order.REVERSE_SORTED
    )
    assert pre == [6, 2, 5, 0, 1, 4, 3]
    assert post == [5, 4, 3, 1, 0, 2, 6]
    # start from node 1 (arbitrarily chosen), neighbors in sorted order
    # what's important in seed_order is that 1 comes first, order of the rest doesn't matter
    pre, post = dfs_recursive(
        g, seed_order=[1, 0, 2, 3, 4, 5, 6], neighbor_order=Order.SORTED
    )
    assert pre == [1, 0, 2, 5, 6, 3, 4]
    assert post == [5, 6, 2, 0, 3, 4, 1]
    # now neighbors in reverse order
    pre, post = dfs_recursive(
        g, seed_order=[1, 0, 2, 3, 4, 5, 6], neighbor_order=Order.REVERSE_SORTED
    )
    assert pre == [1, 4, 3, 0, 2, 6, 5]
    assert post == [4, 3, 6, 5, 2, 0, 1]

    ### nearly spindly trees

    # See 8 node binary example in create_nearly_spindly_b_ary_tree docstring
    g = GraphFactory.create_nearly_spindly_b_ary_tree(2, 8)
    pre, post = dfs_recursive(g, seed_order=Order.SORTED, neighbor_order=Order.SORTED)
    assert pre == [0, 1, 3, 5, 7, 6, 4, 2]
    assert post == [7, 5, 6, 3, 4, 1, 2, 0]
    # start from node 3 (arbitrarily chosen), neighbors in sorted order
    pre, post = dfs_recursive(
        g, seed_order=[3, 0, 1, 2, 4, 5, 6, 7], neighbor_order=Order.SORTED
    )
    assert pre == [3, 1, 0, 2, 4, 5, 7, 6]
    assert post == [2, 0, 4, 1, 7, 5, 6, 3]
    # now with neighbors in reverse order
    pre, post = dfs_recursive(
        g, seed_order=[3, 0, 1, 2, 4, 5, 6, 7], neighbor_order=Order.REVERSE_SORTED
    )
    assert pre == [3, 6, 5, 7, 1, 4, 0, 2]
    assert post == [6, 7, 5, 4, 2, 0, 1, 3]

    # Same with 9 nodes
    g = GraphFactory.create_nearly_spindly_b_ary_tree(2, 9)
    pre, post = dfs_recursive(g, seed_order=Order.SORTED, neighbor_order=Order.SORTED)
    assert pre == [0, 1, 3, 5, 7, 8, 6, 4, 2]
    assert post == [7, 8, 5, 6, 3, 4, 1, 2, 0]
    # start from node 8, neighbors in sorted order
    pre, post = dfs_recursive(
        g, seed_order=[8, 0, 1, 2, 3, 4, 5, 6, 7], neighbor_order=Order.SORTED
    )
    assert pre == [8, 5, 3, 1, 0, 2, 4, 6, 7]
    assert post == [2, 0, 4, 1, 6, 3, 7, 5, 8]

    # See 10 node 3-ary example in create_nearly_spindly_b_ary_tree docstring
    g = GraphFactory.create_nearly_spindly_b_ary_tree(3, 10)
    pre, post = dfs_recursive(g, seed_order=Order.SORTED, neighbor_order=Order.SORTED)
    assert pre == [0, 1, 4, 7, 8, 9, 5, 6, 2, 3]
    assert post == [7, 8, 9, 4, 5, 6, 1, 2, 3, 0]

    # Same with 11 nodes
    g = GraphFactory.create_nearly_spindly_b_ary_tree(3, 11)
    pre, post = dfs_recursive(g, seed_order=Order.SORTED, neighbor_order=Order.SORTED)
    assert pre == [0, 1, 4, 7, 10, 8, 9, 5, 6, 2, 3]
    assert post == [10, 7, 8, 9, 4, 5, 6, 1, 2, 3, 0]

    # Same with 12 nodes
    g = GraphFactory.create_nearly_spindly_b_ary_tree(3, 12)
    pre, post = dfs_recursive(g, seed_order=Order.SORTED, neighbor_order=Order.SORTED)
    assert pre == [0, 1, 4, 7, 10, 11, 8, 9, 5, 6, 2, 3]
    assert post == [10, 11, 7, 8, 9, 4, 5, 6, 1, 2, 3, 0]

    ### arbitrary custom trees
    g = Graph(
        nodes=range(10),
        edges=((0, 1), (1, 2), (2, 3), (3, 4), (0, 5), (5, 6), (6, 7), (0, 8), (8, 9)),
    )
    pre, post = dfs_recursive(g, seed_order=Order.SORTED, neighbor_order=Order.SORTED)
    assert pre == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert post == [4, 3, 2, 1, 7, 6, 5, 9, 8, 0]

    # complete graphs (fully connected, so node 0 should just recurse fully in one pass)
    k = random.randint(4, 10)
    g = GraphFactory.create_complete_graph(k)
    pre, post = dfs_recursive(g, seed_order=Order.SORTED, neighbor_order=Order.SORTED)
    exp_path = list(range(k))
    assert pre == exp_path
    assert post == exp_path[::-1]

    # look ahead graph (see example in create_look_ahead_graph docstring)
    g = GraphFactory.create_look_ahead_graph(5, 2)
    pre, post = dfs_recursive(g, seed_order=Order.SORTED, neighbor_order=Order.SORTED)
    assert pre == [0, 1, 2, 3, 4]
    assert post == pre[::-1]
    # now start from 2
    pre, post = dfs_recursive(
        g, seed_order=[2, 0, 1, 3, 4], neighbor_order=Order.SORTED
    )
    assert pre == [2, 0, 1, 3, 4]
    assert post == pre[::-1]
    # now start from 3
    pre, post = dfs_recursive(
        g, seed_order=[3, 0, 1, 2, 4], neighbor_order=Order.SORTED
    )
    assert pre == [3, 1, 0, 2, 4]
    assert post == pre[::-1]

    # cycles
    g = GraphFactory.create_circuit(4)
    # start at 0, neighbors in sorted order
    pre, post = dfs_recursive(g, seed_order=Order.SORTED, neighbor_order=Order.SORTED)
    assert pre == [0, 1, 2, 3]
    assert post == pre[::-1]
    # start at 1, neighbors in sorted order
    pre, post = dfs_recursive(g, seed_order=[1, 0, 2, 3], neighbor_order=Order.SORTED)
    assert pre == [1, 0, 3, 2]
    assert post == pre[::-1]
    # start at 3, neighbors in sorted order
    pre, post = dfs_recursive(g, seed_order=[3, 0, 1, 2], neighbor_order=Order.SORTED)
    assert pre == [3, 0, 1, 2]
    assert post == pre[::-1]

    ### custom cylic graphs
    # two uneven cycles with 0 at center. I.e., a lopsided figure-8
    g = Graph(
        nodes=range(9),
        edges=(
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 0),
            (0, 4),
            (4, 5),
            (5, 6),
            (6, 7),
            (7, 8),
            (8, 0),
        ),
    )
    # neighbors in order, so shorter cycle first
    pre, post = dfs_recursive(g, seed_order=Order.SORTED, neighbor_order=Order.SORTED)
    assert pre == [0, 1, 2, 3, 4, 5, 6, 7, 8]
    assert post == [3, 2, 1, 8, 7, 6, 5, 4, 0]
    # neighbors in reverse order, so larger cycle first, and in the opposite direction
    pre, post = dfs_recursive(
        g, seed_order=Order.SORTED, neighbor_order=Order.REVERSE_SORTED
    )
    assert pre == [0, 8, 7, 6, 5, 4, 3, 2, 1]
    assert post == [4, 5, 6, 7, 8, 1, 2, 3, 0]
    # now start at 8
    pre, post = dfs_recursive(
        g, seed_order=[8, 0, 1, 2, 3, 4, 5, 6, 7], neighbor_order=Order.REVERSE_SORTED
    )
    assert pre == [8, 7, 6, 5, 4, 0, 3, 2, 1]
    assert post == [1, 2, 3, 0, 4, 5, 6, 7, 8]

    # now add 0-9 edge, start at the 9
    g.add_node(9)
    g.add_edge((0, 9))
    pre, post = dfs_recursive(
        g, seed_order=Order.REVERSE_SORTED, neighbor_order=Order.SORTED
    )
    # prepend 9 to pre, append 9 to post
    assert pre == [9, 0, 1, 2, 3, 4, 5, 6, 7, 8]
    assert post == [3, 2, 1, 8, 7, 6, 5, 4, 0, 9]

    # graph with a main line with cycles coming off of it
    # we already have the current example, we can just add to that
    # 9 -> 0
    # 0 has two cycles coming off it, using up nodes 1 through 8
    # add nodes 10 and 11
    # add a 3-cycle off of 11, using nodes 12 and 13
    # add node 14;
    # add 7-cycle off 14, using nodes 15, 16, 17, 18, 19, 20
    g.add_nodes(range(10, 21))
    g.add_edges(
        (
            (0, 10),
            (10, 11),
            (11, 12),  # start 3-cycle
            (12, 13),
            (13, 11),
            (11, 14),
            (14, 15),  # start 7-cycle
            (15, 16),
            (16, 17),
            (17, 18),
            (18, 19),
            (19, 20),
            (20, 14),
        )
    )
    pre, post = dfs_recursive(
        g, seed_order=[9, *range(9), *range(10, 21)], neighbor_order=Order.SORTED
    )
    assert pre == [
        9,
        0,
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        8,
        10,
        11,
        12,
        13,
        14,
        15,
        16,
        17,
        18,
        19,
        20,
    ]
    assert post == [
        3,
        2,
        1,
        8,
        7,
        6,
        5,
        4,
        13,
        12,
        20,
        19,
        18,
        17,
        16,
        15,
        14,
        11,
        10,
        0,
        9,
    ]

    # nested cycles
    # 0->...->7
    # 2->8->9->10->2
    # 10->11->12->13->10
    g = Graph(
        nodes=range(14),
        edges=(
            (0, 1),
            (1, 2),
            (2, 3),
            (3, 4),
            (4, 5),
            (5, 6),
            (6, 7),
            (7, 0),
            (2, 8),
            (8, 9),
            (9, 10),
            (10, 2),
            (10, 11),
            (11, 12),
            (12, 13),
            (13, 10),
        ),
    )
    pre, post = dfs_recursive(g, seed_order=Order.SORTED, neighbor_order=Order.SORTED)
    assert pre == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    assert post == [7, 6, 5, 4, 3, 13, 12, 11, 10, 9, 8, 2, 1, 0]
    pre, post = dfs_recursive(
        g, seed_order=Order.SORTED, neighbor_order=Order.REVERSE_SORTED
    )
    # assert pre == [0, 1, 2, 10, 13, 12, 11, 9, 8, 3, 4, 5, 6, 73, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    assert pre == [0, 7, 6, 5, 4, 3, 2, 10, 13, 12, 11, 9, 8, 1]
    assert post == [11, 12, 13, 8, 9, 10, 1, 2, 3, 4, 5, 6, 7, 0]

    # test disjoint graphs (disconnected components)
    g_spindly = GraphFactory.create_spindly_tree(3)
    pre_spindly = list(range(3))
    post_spindly = pre_spindly[::-1]
    g_b_ary = GraphFactory.create_b_ary_tree(2, 2)
    pre_b_ary = [0, 1, 3, 4, 2, 5, 6]
    post_b_ary = [3, 4, 1, 5, 6, 2, 0]
    # See 8 node binary example in create_nearly_spindly_b_ary_tree docstring
    g_nearly_spindly_b_ary = GraphFactory.create_nearly_spindly_b_ary_tree(2, 8)
    pre_nearly_spindly_b_ary = [0, 1, 3, 5, 7, 6, 4, 2]
    post_nearly_spindly_b_ary = [7, 5, 6, 3, 4, 1, 2, 0]
    g_custom = g  # above custom example
    pre_custom = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    post_custom = [7, 6, 5, 4, 3, 13, 12, 11, 10, 9, 8, 2, 1, 0]
    gs = (g_spindly, g_b_ary, g_nearly_spindly_b_ary, g_custom)
    g_combined = GraphFactory.concat_int_graphs(gs)
    pres = (pre_spindly, pre_b_ary, pre_nearly_spindly_b_ary, pre_custom)
    posts = (post_spindly, post_b_ary, post_nearly_spindly_b_ary, post_custom)
    lengths = [len(g) for g in gs]
    pre_exp = []
    post_exp = []
    for i, (pre, post) in enumerate(zip(pres, posts)):
        offset = sum(lengths[:i])
        pre_exp.extend([offset + node for node in pre])
        post_exp.extend([offset + node for node in post])
    pre, post = dfs_recursive(
        g_combined, seed_order=Order.SORTED, neighbor_order=Order.SORTED
    )
    assert pre == pre_exp
    assert post == post_exp
