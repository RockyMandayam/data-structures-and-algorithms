import random

import pytest

from graphs.analysis.traversal.bfs import bfs
from graphs.analysis.traversal.order import Order
from graphs.graph import Graph
from graphs.graph_factory import GraphFactory

# TODO why is this so slow with 2**big_number
MAX_TEST_GRAPH_SIZE = 2**8


@pytest.mark.parametrize("use_approach_1", (True, False))
def test_bfs(use_approach_1: bool) -> None:
    # non-comparable nodes
    g = Graph(nodes=(12, "blah"), edges=((12, "blah"),))
    with pytest.raises(TypeError):
        bfs(g, use_approach_1=use_approach_1, seed_order=Order.SORTED)

    ### simple graphs

    # empty graph
    g = Graph()
    level, parents = bfs(g, use_approach_1=use_approach_1)
    assert level == []
    assert parents == {}

    # singleton graph
    g = Graph(nodes=1)
    level, parents = bfs(g, use_approach_1=use_approach_1)
    assert level == [0]
    assert parents == {0: None}

    # generally: n nodes, 0 edges
    for n in (2, 3, random.randint(4, MAX_TEST_GRAPH_SIZE)):
        g = Graph(nodes=n)
        # seeds in sorted order
        level, parents = bfs(g, use_approach_1=use_approach_1, seed_order=Order.SORTED)
        assert level == list(range(n)), n
        # seeds in reverse sorted order
        level, parents = bfs(
            g, use_approach_1=use_approach_1, seed_order=Order.REVERSE_SORTED
        )
        assert level == list(range(n - 1, -1, -1)), n
        assert parents == {u: None for u in range(n)}

    ### spindly trees

    # generally: n node spindly tree
    for n in (2, 3, random.randint(4, MAX_TEST_GRAPH_SIZE)):
        g = GraphFactory.create_spindly_tree(n)
        # in sorted order
        level, parents = bfs(g, use_approach_1=use_approach_1, seed_order=Order.SORTED)
        assert level == list(range(n)), n
        assert parents == {0: None, **{u: u - 1 for u in range(1, n)}}
        # in reverse sorted order
        level, parents = bfs(
            g, use_approach_1=use_approach_1, seed_order=Order.REVERSE_SORTED
        )
        assert level == list(range(n - 1, -1, -1)), n
        assert parents == {n - 1: None, **{u: u + 1 for u in range(n - 1)}}
        # branch from the middle
        bfs_root = random.randint(1, n - 1)
        to_left = list(range(bfs_root - 1, -1, -1))  # from middle to the left
        to_right = list(range(bfs_root + 1, n))  # from middle to the right
        # important that bfs_root is first; everything else is irrelevant
        # explore left then right
        level, parents = bfs(
            g,
            use_approach_1=use_approach_1,
            seed_order=bfs_root,
            neighbor_order=Order.SORTED,
        )
        exp_level = [bfs_root]
        for dist in range(1, len(g)):
            left, right = bfs_root - dist, bfs_root + dist
            if left in g:
                exp_level.append(left)
            if right in g:
                exp_level.append(right)
        assert level == exp_level
        exp_parents = {
            bfs_root: None,
            **{u: u + 1 for u in range(bfs_root)},
            **{u: u - 1 for u in range(bfs_root + 1, n)},
        }
        assert parents == exp_parents
        # explore right then left
        level, parents = bfs(
            g,
            use_approach_1=use_approach_1,
            seed_order=bfs_root,
            neighbor_order=Order.REVERSE_SORTED,
        )
        exp_level = [bfs_root]
        for dist in range(1, len(g)):
            left, right = bfs_root - dist, bfs_root + dist
            if right in g:
                exp_level.append(right)
            if left in g:
                exp_level.append(left)
        assert level == exp_level
        assert parents == exp_parents

    ### binary trees

    # simple binary tree (see create_b_ary_tree docstring for example)
    g = GraphFactory.create_b_ary_tree(2, 2)
    # starting from 0, neighbors in sorted order
    level, parents = bfs(
        g,
        use_approach_1=use_approach_1,
        seed_order=Order.SORTED,
        neighbor_order=Order.SORTED,
    )
    assert level == [0, 1, 2, 3, 4, 5, 6]
    exp_parents = {0: None, 1: 0, 2: 0, 3: 1, 4: 1, 5: 2, 6: 2}
    assert parents == exp_parents
    # starting from 0, neighbors in reverse order
    level, parents = bfs(
        g,
        use_approach_1=use_approach_1,
        seed_order=Order.SORTED,
        neighbor_order=Order.REVERSE_SORTED,
    )
    assert level == [0, 2, 1, 6, 5, 4, 3]
    assert parents == exp_parents
    # starting from 6, neighbors in sorted order
    level, parents = bfs(
        g,
        use_approach_1=use_approach_1,
        seed_order=Order.REVERSE_SORTED,
        neighbor_order=Order.SORTED,
    )
    assert level == [6, 2, 0, 5, 1, 3, 4]
    exp_parents = {6: None, 2: 6, 5: 2, 0: 2, 1: 0, 3: 1, 4: 1}
    assert parents == exp_parents
    # starting from 6, neighbors in reverse order
    level, parents = bfs(
        g,
        use_approach_1=use_approach_1,
        seed_order=Order.REVERSE_SORTED,
        neighbor_order=Order.REVERSE_SORTED,
    )
    assert level == [6, 2, 5, 0, 1, 4, 3]
    assert parents == exp_parents
    # starting from 1
    level, parents = bfs(
        g,
        use_approach_1=use_approach_1,
        seed_order=1,
        neighbor_order=Order.SORTED,
    )
    assert level == [1, 0, 3, 4, 2, 5, 6]
    exp_parents = {1: None, 3: 1, 4: 1, 0: 1, 2: 0, 5: 2, 6: 2}
    assert parents == exp_parents
    # now neighbors in reverse order
    level, parents = bfs(
        g,
        use_approach_1=use_approach_1,
        seed_order=1,
        neighbor_order=Order.REVERSE_SORTED,
    )
    assert level == [1, 4, 3, 0, 2, 6, 5]
    assert parents == exp_parents

    ### nearly spindly trees

    # See 8 node binary example in create_nearly_spindly_b_ary_tree docstring
    g = GraphFactory.create_nearly_spindly_b_ary_tree(2, 8)
    level, parents = bfs(
        g,
        use_approach_1=use_approach_1,
        seed_order=Order.SORTED,
        neighbor_order=Order.SORTED,
    )
    assert level == list(range(8))
    assert parents == {0: None, 1: 0, 2: 0, 3: 1, 4: 1, 5: 3, 6: 3, 7: 5}
    # start from node 3 (arbitrarily chosen), neighbors in sorted order
    level, parents = bfs(
        g,
        use_approach_1=use_approach_1,
        seed_order=3,
        neighbor_order=Order.SORTED,
    )
    assert level == [3, 1, 5, 6, 0, 4, 7, 2]
    exp_parents = {3: None, 5: 3, 6: 3, 1: 3, 7: 5, 4: 1, 0: 1, 2: 0}
    assert parents == exp_parents
    # now with neighbors in reverse order
    level, parents = bfs(
        g,
        use_approach_1=use_approach_1,
        seed_order=3,
        neighbor_order=Order.REVERSE_SORTED,
    )
    assert level == [3, 6, 5, 1, 7, 4, 0, 2]
    parents == exp_parents

    # Same with 9 nodes
    g = GraphFactory.create_nearly_spindly_b_ary_tree(2, 9)
    level, parents = bfs(
        g,
        use_approach_1=use_approach_1,
        seed_order=Order.SORTED,
        neighbor_order=Order.SORTED,
    )
    assert level == list(range(9))
    assert parents == {0: None, 1: 0, 2: 0, 3: 1, 4: 1, 5: 3, 6: 3, 7: 5, 8: 5}
    # start from node 8, neighbors in sorted order
    level, parents = bfs(
        g,
        use_approach_1=use_approach_1,
        seed_order=8,
        neighbor_order=Order.SORTED,
    )
    assert level == [8, 5, 3, 7, 1, 6, 0, 4, 2]
    assert parents == {8: None, 5: 8, 7: 5, 3: 5, 6: 3, 1: 3, 4: 1, 0: 1, 2: 0}

    # See 10 node 3-ary example in create_nearly_spindly_b_ary_tree docstring
    g = GraphFactory.create_nearly_spindly_b_ary_tree(3, 10)
    level, parents = bfs(
        g,
        use_approach_1=use_approach_1,
        seed_order=Order.SORTED,
        neighbor_order=Order.SORTED,
    )
    assert level == list(range(10))
    exp_parents = {0: None, 1: 0, 2: 0, 3: 0, 4: 1, 5: 1, 6: 1, 7: 4, 8: 4, 9: 4}
    assert parents == exp_parents

    # Same with 11 nodes
    g = GraphFactory.create_nearly_spindly_b_ary_tree(3, 11)
    level, parents = bfs(
        g,
        use_approach_1=use_approach_1,
        seed_order=Order.SORTED,
        neighbor_order=Order.SORTED,
    )
    assert level == list(range(11))
    exp_parents[10] = 7
    assert parents == exp_parents

    # Same with 12 nodes
    g = GraphFactory.create_nearly_spindly_b_ary_tree(3, 12)
    level, parents = bfs(
        g,
        use_approach_1=use_approach_1,
        seed_order=Order.SORTED,
        neighbor_order=Order.SORTED,
    )
    assert level == list(range(12))
    exp_parents[11] = 7
    assert parents == exp_parents

    ### arbitrary custom tree
    g = Graph(
        nodes=range(10),
        edges=((0, 1), (1, 2), (2, 3), (3, 4), (0, 5), (5, 6), (6, 7), (0, 8), (8, 9)),
    )
    level, parents = bfs(
        g,
        use_approach_1=use_approach_1,
        seed_order=Order.SORTED,
        neighbor_order=Order.SORTED,
    )
    assert level == [0, 1, 5, 8, 2, 6, 9, 3, 7, 4]
    assert parents == {0: None, 1: 0, 5: 0, 8: 0, 2: 1, 3: 2, 4: 3, 6: 5, 7: 6, 9: 8}

    # complete graphs (fully connected, so node 0 should just recurse fully in one pass)
    k = random.randint(4, 10)
    g = GraphFactory.create_complete_graph(k)
    level, parents = bfs(
        g,
        use_approach_1=use_approach_1,
        seed_order=Order.SORTED,
        neighbor_order=Order.SORTED,
    )
    assert level == list(range(k))
    assert parents == {0: None, **{i: 0 for i in range(1, k)}}

    # look ahead graph (see example in create_look_ahead_graph docstring)
    g = GraphFactory.create_look_ahead_graph(5, 2)
    level, parents = bfs(
        g,
        use_approach_1=use_approach_1,
        seed_order=Order.SORTED,
        neighbor_order=Order.SORTED,
    )
    assert level == [0, 1, 2, 3, 4]
    assert parents == {0: None, 1: 0, 2: 0, 3: 1, 4: 2}
    # now start from 2
    level, parents = bfs(
        g, use_approach_1=use_approach_1, seed_order=2, neighbor_order=Order.SORTED
    )
    assert level == [2, 0, 1, 3, 4]
    assert parents == {2: None, 0: 2, 1: 2, 3: 2, 4: 2}
    # now start from 3
    level, parents = bfs(
        g, use_approach_1=use_approach_1, seed_order=3, neighbor_order=Order.SORTED
    )
    assert level == [3, 1, 2, 4, 0]
    assert parents == {3: None, 1: 3, 2: 3, 4: 3, 0: 1}

    # cycles
    g = GraphFactory.create_circuit(4)
    # start at 0, neighbors in sorted order
    level, parents = bfs(
        g,
        use_approach_1=use_approach_1,
        seed_order=Order.SORTED,
        neighbor_order=Order.SORTED,
    )
    assert level == [0, 1, 3, 2]
    assert parents == {0: None, 1: 0, 3: 0, 2: 1}
    # start at 1, neighbors in sorted order
    level, parents = bfs(
        g, use_approach_1=use_approach_1, seed_order=1, neighbor_order=Order.SORTED
    )
    assert level == [1, 0, 2, 3]
    assert parents == {1: None, 0: 1, 2: 1, 3: 0}
    # start at 3, neighbors in sorted order
    level, parents = bfs(
        g, use_approach_1=use_approach_1, seed_order=3, neighbor_order=Order.SORTED
    )
    assert level == [3, 0, 2, 1]
    assert parents == {3: None, 0: 3, 2: 3, 1: 0}

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
    level, parents = bfs(
        g,
        use_approach_1=use_approach_1,
        seed_order=Order.SORTED,
        neighbor_order=Order.SORTED,
    )
    assert level == [0, 1, 3, 4, 8, 2, 5, 7, 6]
    assert parents == {0: None, 1: 0, 3: 0, 4: 0, 8: 0, 2: 1, 5: 4, 7: 8, 6: 5}
    # neighbors in reverse order, so larger cycle first, and in the opposite direction
    level, parents = bfs(
        g,
        use_approach_1=use_approach_1,
        seed_order=Order.SORTED,
        neighbor_order=Order.REVERSE_SORTED,
    )
    assert level == [0, 8, 4, 3, 1, 7, 5, 2, 6]
    assert parents == {0: None, 8: 0, 4: 0, 3: 0, 1: 0, 7: 8, 5: 4, 2: 3, 6: 7}
    # now start at 8
    level, parents = bfs(
        g,
        use_approach_1=use_approach_1,
        seed_order=8,
        neighbor_order=Order.REVERSE_SORTED,
    )
    assert level == [8, 7, 0, 6, 4, 3, 1, 5, 2]
    assert parents == {8: None, 7: 8, 0: 8, 6: 7, 4: 0, 3: 0, 1: 0, 5: 6, 2: 3}

    # add node 9, add 0-9 edge, start at 9
    g.add_node(9)
    g.add_edge((0, 9))
    level, parents = bfs(
        g,
        use_approach_1=use_approach_1,
        seed_order=Order.REVERSE_SORTED,
        neighbor_order=Order.SORTED,
    )
    assert level == [9, 0, 1, 3, 4, 8, 2, 5, 7, 6]
    assert parents == {9: None, 0: 9, 1: 0, 3: 0, 4: 0, 8: 0, 2: 1, 5: 4, 7: 8, 6: 5}

    # graph with a main line with cycles coming off of it
    # we already have the current example, we can just add to that
    # 9 - 0
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
    level, parents = bfs(
        g,
        use_approach_1=use_approach_1,
        seed_order=9,
        neighbor_order=Order.SORTED,
    )
    assert level == [
        9,
        0,
        1,
        3,
        4,
        8,
        10,
        2,
        5,
        7,
        11,
        6,
        12,
        13,
        14,
        15,
        20,
        16,
        19,
        17,
        18,
    ]
    assert parents == {
        9: None,
        0: 9,
        1: 0,
        3: 0,
        4: 0,
        8: 0,
        10: 0,
        2: 1,
        5: 4,
        7: 8,
        11: 10,
        6: 5,
        12: 11,
        13: 11,
        14: 11,
        15: 14,
        20: 14,
        16: 15,
        19: 20,
        17: 16,
        18: 19,
    }

    # "nested" cycles
    # 0-1-2-3-4-5-6-7-0
    # 2-8-9-10-2
    # 10-11-12-13-10
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
    level, parents = bfs(
        g,
        use_approach_1=use_approach_1,
        seed_order=Order.SORTED,
        neighbor_order=Order.SORTED,
    )
    assert level == [0, 1, 7, 2, 6, 3, 8, 10, 5, 4, 9, 11, 13, 12]
    assert parents == {
        0: None,
        1: 0,
        7: 0,
        2: 1,
        6: 7,
        3: 2,
        8: 2,
        10: 2,
        5: 6,
        4: 3,
        9: 8,
        11: 10,
        13: 10,
        5: 6,
        12: 11.0,
    }
    level, parents = bfs(
        g,
        use_approach_1=use_approach_1,
        seed_order=Order.SORTED,
        neighbor_order=Order.REVERSE_SORTED,
    )
    assert level == [0, 7, 1, 6, 2, 5, 10, 8, 3, 4, 13, 11, 9, 12]
    assert parents == {
        0: None,
        7: 0,
        1: 0,
        6: 7,
        2: 1,
        5: 6,
        10: 2,
        8: 2,
        3: 2,
        4: 5,
        13: 10,
        11: 10,
        9: 10,
        12: 13,
    }

    # test disjoint graphs (disconnected components)
    g_spindly = GraphFactory.create_spindly_tree(3)
    level_spindly = list(range(3))
    parents_spindly = {0: None, 1: 0, 2: 1}
    g_b_ary = GraphFactory.create_b_ary_tree(2, 2)
    level_b_ary = [0, 1, 2, 3, 4, 5, 6]
    parents_b_ary = {0: None, 1: 0, 2: 0, 3: 1, 4: 1, 5: 2, 6: 2}
    # See 8 node binary example in create_nearly_spindly_b_ary_tree docstring
    g_nearly_spindly_b_ary = GraphFactory.create_nearly_spindly_b_ary_tree(2, 8)
    level_nearly_spindly_b_ary = list(range(8))
    parents_nearly_spindly_b_ary = {0: None, 1: 0, 2: 0, 3: 1, 4: 1, 5: 3, 6: 3, 7: 5}
    g_custom = g  # above custom example
    level_custom = [0, 1, 7, 2, 6, 3, 8, 10, 5, 4, 9, 11, 13, 12]
    parents_custom = {
        0: None,
        1: 0,
        7: 0,
        2: 1,
        6: 7,
        3: 2,
        8: 2,
        10: 2,
        5: 6,
        4: 3,
        9: 8,
        11: 10,
        13: 10,
        5: 6,
        12: 11.0,
    }
    gs = (g_spindly, g_b_ary, g_nearly_spindly_b_ary, g_custom)
    g_combined = GraphFactory.concat_int_graphs(gs)
    levels = (level_spindly, level_b_ary, level_nearly_spindly_b_ary, level_custom)
    parents_seq = (
        parents_spindly,
        parents_b_ary,
        parents_nearly_spindly_b_ary,
        parents_custom,
    )
    lengths = [len(g) for g in gs]
    level_exp = []
    parents_exp = {}
    for i, (level, parents) in enumerate(zip(levels, parents_seq)):
        offset = sum(lengths[:i])
        level_exp.extend([offset + node for node in level])
        parents_exp.update(
            {
                offset + node: offset + parent if parent is not None else None
                for node, parent in parents.items()
            }
        )
    level, parents = bfs(
        g_combined,
        use_approach_1=use_approach_1,
        seed_order=Order.SORTED,
        neighbor_order=Order.SORTED,
    )
    assert level == level_exp
    assert parents == parents_exp
