import random

import pytest

from dsa.graphs.analysis.traversal.dfs import dfs
from dsa.graphs.analysis.traversal.order import Order
from dsa.graphs.digraph import Digraph
from dsa.graphs.digraph_factory import DigraphFactory
from dsa.graphs.graph import Graph
from dsa.graphs.graph_factory import GraphFactory

# TODO why is this so slow with 2**big_number
MAX_TEST_GRAPH_SIZE = 2**8


@pytest.mark.parametrize("recursive", (True, False))
def test_dfs_undirected(recursive: bool) -> None:
    # non-comparable nodes
    g = Graph(nodes=(12, "blah"), edges=((12, "blah"),))
    with pytest.raises(TypeError):
        dfs(g, recursive=recursive, seed_order=Order.SORTED)

    ### simple graphs

    # empty graph
    g = Graph()
    (
        parents,
        dists,
        pre,
        post,
        ccs,
        undirected_contains_cycle,
        directed_contains_cycle,
    ) = dfs(g, recursive=recursive)
    assert parents == {}
    assert dists == {}
    assert pre == []
    assert post == []
    assert not undirected_contains_cycle

    # singleton graph
    g = Graph(nodes=1)
    (
        parents,
        dists,
        pre,
        post,
        ccs,
        undirected_contains_cycle,
        directed_contains_cycle,
    ) = dfs(g, recursive=recursive)
    assert parents == {0: None}
    assert dists == {0: 0}
    assert pre == [0]
    assert post == [0]
    assert ccs == [[0]]
    assert not undirected_contains_cycle

    # generally: n nodes, 0 edges
    for n in (2, 3, random.randint(4, MAX_TEST_GRAPH_SIZE)):
        g = Graph(nodes=n)
        # seeds in sorted order
        (
            parents,
            dists,
            pre,
            post,
            ccs,
            undirected_contains_cycle,
            directed_contains_cycle,
        ) = dfs(g, recursive=recursive, seed_order=Order.SORTED)
        assert parents == {u: None for u in range(n)}
        assert dists == {u: 0 for u in range(n)}
        assert pre == list(range(n)), n
        assert post == pre, n
        assert ccs == [[i] for i in range(n)]
        assert not undirected_contains_cycle
        # seeds in reverse sorted order
        (
            parents,
            dists,
            pre,
            post,
            ccs,
            undirected_contains_cycle,
            directed_contains_cycle,
        ) = dfs(g, recursive=recursive, seed_order=Order.REVERSE_SORTED)
        assert parents == {u: None for u in range(n)}
        assert dists == {u: 0 for u in range(n)}
        assert pre == list(range(n - 1, -1, -1)), n
        assert post == pre, n
        assert ccs == [[i] for i in range(n - 1, -1, -1)]
        assert not undirected_contains_cycle

    ### spindly trees

    # generally: n node spindly tree
    for n in (2, 3, random.randint(4, MAX_TEST_GRAPH_SIZE)):
        g = GraphFactory.create_spindly_tree(n)
        # in sorted order
        (
            parents,
            dists,
            pre,
            post,
            ccs,
            undirected_contains_cycle,
            directed_contains_cycle,
        ) = dfs(g, recursive=recursive, seed_order=Order.SORTED)
        assert parents == {0: None, **{u: u - 1 for u in range(1, n)}}
        assert dists == {u: u for u in range(n)}
        assert pre == list(range(n)), n
        assert post == pre[::-1]
        assert ccs == [pre]
        assert not undirected_contains_cycle
        # in reverse sorted order
        (
            parents,
            dists,
            pre,
            post,
            ccs,
            undirected_contains_cycle,
            directed_contains_cycle,
        ) = dfs(g, recursive=recursive, seed_order=Order.REVERSE_SORTED)
        assert parents == {n - 1: None, **{u: u + 1 for u in range(n - 1)}}
        assert dists == {u: n - 1 - u for u in range(n)}
        assert pre == list(range(n - 1, -1, -1)), n
        assert post == pre[::-1]
        assert ccs == [pre]
        assert not undirected_contains_cycle
        # branch from the middle
        dfs_root = random.randint(1, n - 1)
        to_left = list(range(dfs_root - 1, -1, -1))  # from middle to the left
        to_right = list(range(dfs_root + 1, n))  # from middle to the right
        # important that dfs_root is first; everything else is irrelevant
        # explore left then right
        (
            parents,
            dists,
            pre,
            post,
            ccs,
            undirected_contains_cycle,
            directed_contains_cycle,
        ) = dfs(
            g, recursive=recursive, seed_order=dfs_root, neighbor_order=Order.SORTED
        )
        exp_parents = {
            dfs_root: None,
            **{u: u + 1 for u in range(dfs_root)},
            **{u: u - 1 for u in range(dfs_root + 1, n)},
        }
        exp_dists = {
            dfs_root: 0,
            **{u: dfs_root - u for u in range(dfs_root)},
            **{u: u - dfs_root for u in range(dfs_root + 1, n)},
        }
        assert parents == exp_parents
        assert dists == exp_dists
        assert pre == [dfs_root, *to_left, *to_right]
        assert post == [*to_left[::-1], *to_right[::-1], dfs_root]
        assert ccs == [pre]
        assert not undirected_contains_cycle
        # explore right then left
        (
            parents,
            dists,
            pre,
            post,
            ccs,
            undirected_contains_cycle,
            directed_contains_cycle,
        ) = dfs(
            g,
            recursive=recursive,
            seed_order=dfs_root,
            neighbor_order=Order.REVERSE_SORTED,
        )
        assert parents == exp_parents
        assert dists == exp_dists
        assert pre == [dfs_root, *to_right, *to_left]
        assert post == [*to_right[::-1], *to_left[::-1], dfs_root]
        assert ccs == [pre]
        assert not undirected_contains_cycle

    ### binary trees

    # simple binary tree (see create_b_ary_tree docstring for example)
    g = GraphFactory.create_b_ary_tree(2, 2)
    # starting from 0, neighbors in sorted order
    (
        parents,
        dists,
        pre,
        post,
        ccs,
        undirected_contains_cycle,
        directed_contains_cycle,
    ) = dfs(
        g, recursive=recursive, seed_order=Order.SORTED, neighbor_order=Order.SORTED
    )
    exp_parents = {0: None, 1: 0, 2: 0, 3: 1, 4: 1, 5: 2, 6: 2}
    exp_dists = {0: 0, 1: 1, 2: 1, 3: 2, 4: 2, 5: 2, 6: 2}
    assert parents == exp_parents
    assert dists == exp_dists
    assert pre == [0, 1, 3, 4, 2, 5, 6]
    assert post == [3, 4, 1, 5, 6, 2, 0]
    assert ccs == [pre]
    assert not undirected_contains_cycle
    # starting from 0, neighbors in reverse order
    (
        parents,
        dists,
        pre,
        post,
        ccs,
        undirected_contains_cycle,
        directed_contains_cycle,
    ) = dfs(
        g,
        recursive=recursive,
        seed_order=Order.SORTED,
        neighbor_order=Order.REVERSE_SORTED,
    )
    assert parents == exp_parents
    assert dists == exp_dists
    assert pre == [0, 2, 6, 5, 1, 4, 3]
    assert post == [6, 5, 2, 4, 3, 1, 0]
    assert ccs == [pre]
    assert not undirected_contains_cycle
    # starting from 6, neighbors in sorted order
    (
        parents,
        dists,
        pre,
        post,
        ccs,
        undirected_contains_cycle,
        directed_contains_cycle,
    ) = dfs(
        g,
        recursive=recursive,
        seed_order=Order.REVERSE_SORTED,
        neighbor_order=Order.SORTED,
    )
    exp_parents = {6: None, 2: 6, 5: 2, 0: 2, 1: 0, 3: 1, 4: 1}
    exp_dists = {6: 0, 2: 1, 5: 2, 0: 2, 1: 3, 3: 4, 4: 4}
    assert parents == exp_parents
    assert dists == exp_dists
    assert pre == [6, 2, 0, 1, 3, 4, 5]
    assert post == [3, 4, 1, 0, 5, 2, 6]
    assert ccs == [pre]
    assert not undirected_contains_cycle
    # starting from 6, neighbors in reverse order
    (
        parents,
        dists,
        pre,
        post,
        ccs,
        undirected_contains_cycle,
        directed_contains_cycle,
    ) = dfs(
        g,
        recursive=recursive,
        seed_order=Order.REVERSE_SORTED,
        neighbor_order=Order.REVERSE_SORTED,
    )
    assert parents == exp_parents
    assert dists == exp_dists
    assert pre == [6, 2, 5, 0, 1, 4, 3]
    assert post == [5, 4, 3, 1, 0, 2, 6]
    assert ccs == [pre]
    assert not undirected_contains_cycle
    # starting from 1
    (
        parents,
        dists,
        pre,
        post,
        ccs,
        undirected_contains_cycle,
        directed_contains_cycle,
    ) = dfs(
        g,
        recursive=recursive,
        seed_order=1,
        neighbor_order=Order.SORTED,
    )
    exp_parents = {1: None, 3: 1, 4: 1, 0: 1, 2: 0, 5: 2, 6: 2}
    exp_dists = {1: 0, 3: 1, 4: 1, 0: 1, 2: 2, 5: 3, 6: 3}
    assert parents == exp_parents
    assert dists == exp_dists
    assert pre == [1, 0, 2, 5, 6, 3, 4]
    assert post == [5, 6, 2, 0, 3, 4, 1]
    assert ccs == [pre]
    assert not undirected_contains_cycle
    # now neighbors in reverse order
    (
        parents,
        dists,
        pre,
        post,
        ccs,
        undirected_contains_cycle,
        directed_contains_cycle,
    ) = dfs(
        g,
        recursive=recursive,
        seed_order=1,
        neighbor_order=Order.REVERSE_SORTED,
    )
    assert parents == exp_parents
    assert dists == exp_dists
    assert pre == [1, 4, 3, 0, 2, 6, 5]
    assert post == [4, 3, 6, 5, 2, 0, 1]
    assert ccs == [pre]
    assert not undirected_contains_cycle

    ### nearly spindly trees

    # See 8 node binary example in create_nearly_spindly_b_ary_tree docstring
    g = GraphFactory.create_nearly_spindly_b_ary_tree(2, 8)
    (
        parents,
        dists,
        pre,
        post,
        ccs,
        undirected_contains_cycle,
        directed_contains_cycle,
    ) = dfs(
        g, recursive=recursive, seed_order=Order.SORTED, neighbor_order=Order.SORTED
    )
    assert parents == {0: None, 1: 0, 2: 0, 3: 1, 4: 1, 5: 3, 6: 3, 7: 5}
    assert dists == {0: 0, 1: 1, 2: 1, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4}
    assert pre == [0, 1, 3, 5, 7, 6, 4, 2]
    assert post == [7, 5, 6, 3, 4, 1, 2, 0]
    assert ccs == [pre]
    assert not undirected_contains_cycle
    # start from node 3 (arbitrarily chosen), neighbors in sorted order
    (
        parents,
        dists,
        pre,
        post,
        ccs,
        undirected_contains_cycle,
        directed_contains_cycle,
    ) = dfs(
        g,
        recursive=recursive,
        seed_order=3,
        neighbor_order=Order.SORTED,
    )
    exp_parents = {3: None, 5: 3, 6: 3, 7: 5, 1: 3, 4: 1, 0: 1, 2: 0}
    exp_dists = {3: 0, 5: 1, 6: 1, 7: 2, 1: 1, 4: 2, 0: 2, 2: 3}
    assert parents == exp_parents
    assert dists == exp_dists
    assert pre == [3, 1, 0, 2, 4, 5, 7, 6]
    assert post == [2, 0, 4, 1, 7, 5, 6, 3]
    assert ccs == [pre]
    assert not undirected_contains_cycle
    # now with neighbors in reverse order
    (
        parents,
        dists,
        pre,
        post,
        ccs,
        undirected_contains_cycle,
        directed_contains_cycle,
    ) = dfs(
        g,
        recursive=recursive,
        seed_order=3,
        neighbor_order=Order.REVERSE_SORTED,
    )
    assert parents == exp_parents
    assert dists == exp_dists
    assert pre == [3, 6, 5, 7, 1, 4, 0, 2]
    assert post == [6, 7, 5, 4, 2, 0, 1, 3]
    assert ccs == [pre]
    assert not undirected_contains_cycle

    # Another nearly spindly binary tree but with 9 nodes
    g = GraphFactory.create_nearly_spindly_b_ary_tree(2, 9)
    (
        parents,
        dists,
        pre,
        post,
        ccs,
        undirected_contains_cycle,
        directed_contains_cycle,
    ) = dfs(
        g, recursive=recursive, seed_order=Order.SORTED, neighbor_order=Order.SORTED
    )
    assert parents == {0: None, 1: 0, 2: 0, 3: 1, 4: 1, 5: 3, 6: 3, 7: 5, 8: 5}
    assert dists == {0: 0, 1: 1, 2: 1, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4}
    assert pre == [0, 1, 3, 5, 7, 8, 6, 4, 2]
    assert post == [7, 8, 5, 6, 3, 4, 1, 2, 0]
    assert ccs == [pre]
    assert not undirected_contains_cycle
    # start from node 8, neighbors in sorted order
    (
        parents,
        dists,
        pre,
        post,
        ccs,
        undirected_contains_cycle,
        directed_contains_cycle,
    ) = dfs(
        g,
        recursive=recursive,
        seed_order=8,
        neighbor_order=Order.SORTED,
    )
    assert parents == {8: None, 5: 8, 7: 5, 3: 5, 6: 3, 1: 3, 4: 1, 0: 1, 2: 0}
    assert dists == {8: 0, 5: 1, 7: 2, 3: 2, 6: 3, 1: 3, 4: 4, 0: 4, 2: 5}
    assert pre == [8, 5, 3, 1, 0, 2, 4, 6, 7]
    assert post == [2, 0, 4, 1, 6, 3, 7, 5, 8]
    assert ccs == [pre]
    assert not undirected_contains_cycle

    # See 10 node 3-ary example in create_nearly_spindly_b_ary_tree docstring
    g = GraphFactory.create_nearly_spindly_b_ary_tree(3, 10)
    (
        parents,
        dists,
        pre,
        post,
        ccs,
        undirected_contains_cycle,
        directed_contains_cycle,
    ) = dfs(
        g, recursive=recursive, seed_order=Order.SORTED, neighbor_order=Order.SORTED
    )
    exp_parents = {0: None, 1: 0, 2: 0, 3: 0, 4: 1, 5: 1, 6: 1, 7: 4, 8: 4, 9: 4}
    exp_dists = {0: 0, 1: 1, 2: 1, 3: 1, 4: 2, 5: 2, 6: 2, 7: 3, 8: 3, 9: 3}
    assert parents == exp_parents
    assert dists == exp_dists
    assert pre == [0, 1, 4, 7, 8, 9, 5, 6, 2, 3]
    assert post == [7, 8, 9, 4, 5, 6, 1, 2, 3, 0]
    assert ccs == [pre]
    assert not undirected_contains_cycle

    # Same with 11 nodes
    g = GraphFactory.create_nearly_spindly_b_ary_tree(3, 11)
    (
        parents,
        dists,
        pre,
        post,
        ccs,
        undirected_contains_cycle,
        directed_contains_cycle,
    ) = dfs(
        g, recursive=recursive, seed_order=Order.SORTED, neighbor_order=Order.SORTED
    )
    exp_parents[10] = 7
    exp_dists[10] = 4
    assert parents == exp_parents
    assert dists == exp_dists
    assert pre == [0, 1, 4, 7, 10, 8, 9, 5, 6, 2, 3]
    assert post == [10, 7, 8, 9, 4, 5, 6, 1, 2, 3, 0]
    assert ccs == [pre]
    assert not undirected_contains_cycle

    # Same with 12 nodes
    g = GraphFactory.create_nearly_spindly_b_ary_tree(3, 12)
    (
        parents,
        dists,
        pre,
        post,
        ccs,
        undirected_contains_cycle,
        directed_contains_cycle,
    ) = dfs(
        g, recursive=recursive, seed_order=Order.SORTED, neighbor_order=Order.SORTED
    )
    exp_parents[11] = 7
    exp_dists[11] = 4
    assert parents == exp_parents
    assert dists == exp_dists
    assert pre == [0, 1, 4, 7, 10, 11, 8, 9, 5, 6, 2, 3]
    assert post == [10, 11, 7, 8, 9, 4, 5, 6, 1, 2, 3, 0]
    assert ccs == [pre]
    assert not undirected_contains_cycle

    ### arbitrary custom tree
    g = Graph(
        nodes=range(10),
        edges=((0, 1), (1, 2), (2, 3), (3, 4), (0, 5), (5, 6), (6, 7), (0, 8), (8, 9)),
    )
    (
        parents,
        dists,
        pre,
        post,
        ccs,
        undirected_contains_cycle,
        directed_contains_cycle,
    ) = dfs(
        g, recursive=recursive, seed_order=Order.SORTED, neighbor_order=Order.SORTED
    )
    assert parents == {0: None, 1: 0, 5: 0, 8: 0, 2: 1, 3: 2, 4: 3, 6: 5, 7: 6, 9: 8}
    assert dists == {0: 0, 1: 1, 5: 1, 8: 1, 2: 2, 3: 3, 4: 4, 6: 2, 7: 3, 9: 2}
    assert pre == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    assert post == [4, 3, 2, 1, 7, 6, 5, 9, 8, 0]
    assert ccs == [pre]
    assert not undirected_contains_cycle

    # complete graphs (fully connected, so node 0 should just recurse fully in one pass)
    k = random.randint(4, 10)
    g = GraphFactory.create_complete_graph(k)
    (
        parents,
        dists,
        pre,
        post,
        ccs,
        undirected_contains_cycle,
        directed_contains_cycle,
    ) = dfs(
        g, recursive=recursive, seed_order=Order.SORTED, neighbor_order=Order.SORTED
    )
    exp_path = list(range(k))
    assert parents == {0: None, **{i: i - 1 for i in range(1, k)}}
    assert dists == {0: 0, **{i: i for i in range(1, k)}}
    assert pre == exp_path
    assert post == exp_path[::-1]
    assert ccs == [pre]
    assert undirected_contains_cycle

    # look ahead graph (see example in create_look_ahead_graph docstring)
    g = GraphFactory.create_look_ahead_graph(5, 2)
    (
        parents,
        dists,
        pre,
        post,
        ccs,
        undirected_contains_cycle,
        directed_contains_cycle,
    ) = dfs(
        g, recursive=recursive, seed_order=Order.SORTED, neighbor_order=Order.SORTED
    )
    assert parents == {0: None, 1: 0, 2: 1, 3: 2, 4: 3}
    assert dists == {0: 0, 1: 1, 2: 2, 3: 3, 4: 4}
    assert pre == [0, 1, 2, 3, 4]
    assert post == pre[::-1]
    assert ccs == [pre]
    assert undirected_contains_cycle
    # now start from 2
    (
        parents,
        dists,
        pre,
        post,
        ccs,
        undirected_contains_cycle,
        directed_contains_cycle,
    ) = dfs(g, recursive=recursive, seed_order=2, neighbor_order=Order.SORTED)
    assert parents == {2: None, 0: 2, 1: 0, 3: 1, 4: 3}
    assert dists == {2: 0, 0: 1, 1: 2, 3: 3, 4: 4}
    assert pre == [2, 0, 1, 3, 4]
    assert post == pre[::-1]
    assert ccs == [pre]
    assert undirected_contains_cycle
    # now start from 3
    (
        parents,
        dists,
        pre,
        post,
        ccs,
        undirected_contains_cycle,
        directed_contains_cycle,
    ) = dfs(g, recursive=recursive, seed_order=3, neighbor_order=Order.SORTED)
    assert parents == {3: None, 1: 3, 0: 1, 2: 0, 4: 2}
    assert dists == {3: 0, 1: 1, 0: 2, 2: 3, 4: 4}
    assert pre == [3, 1, 0, 2, 4]
    assert post == pre[::-1]
    assert ccs == [pre]
    assert undirected_contains_cycle

    # cycles
    g = GraphFactory.create_cycle(4)
    # start at 0, neighbors in sorted order
    (
        parents,
        dists,
        pre,
        post,
        ccs,
        undirected_contains_cycle,
        directed_contains_cycle,
    ) = dfs(
        g, recursive=recursive, seed_order=Order.SORTED, neighbor_order=Order.SORTED
    )
    assert parents == {0: None, **{i: i - 1 for i in range(1, 4)}}
    assert dists == {0: 0, **{i: i for i in range(1, 4)}}
    assert pre == [0, 1, 2, 3]
    assert post == pre[::-1]
    assert ccs == [pre]
    assert undirected_contains_cycle
    # start at 1, neighbors in sorted order
    (
        parents,
        dists,
        pre,
        post,
        ccs,
        undirected_contains_cycle,
        directed_contains_cycle,
    ) = dfs(g, recursive=recursive, seed_order=1, neighbor_order=Order.SORTED)
    assert parents == {1: None, 0: 1, 3: 0, 2: 3}
    assert dists == {1: 0, 0: 1, 3: 2, 2: 3}
    assert pre == [1, 0, 3, 2]
    assert post == pre[::-1]
    assert ccs == [pre]
    assert undirected_contains_cycle
    # start at 3, neighbors in sorted order
    (
        parents,
        dists,
        pre,
        post,
        ccs,
        undirected_contains_cycle,
        directed_contains_cycle,
    ) = dfs(g, recursive=recursive, seed_order=3, neighbor_order=Order.SORTED)
    assert parents == {3: None, 0: 3, 1: 0, 2: 1}
    assert dists == {3: 0, 0: 1, 1: 2, 2: 3}
    assert pre == [3, 0, 1, 2]
    assert post == pre[::-1]
    assert ccs == [pre]
    assert undirected_contains_cycle

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
    (
        parents,
        dists,
        pre,
        post,
        ccs,
        undirected_contains_cycle,
        directed_contains_cycle,
    ) = dfs(
        g, recursive=recursive, seed_order=Order.SORTED, neighbor_order=Order.SORTED
    )
    assert parents == {0: None, 1: 0, 2: 1, 3: 2, 4: 0, 5: 4, 6: 5, 7: 6, 8: 7}
    assert dists == {0: 0, 1: 1, 2: 2, 3: 3, 4: 1, 5: 2, 6: 3, 7: 4, 8: 5}
    assert pre == [0, 1, 2, 3, 4, 5, 6, 7, 8]
    assert post == [3, 2, 1, 8, 7, 6, 5, 4, 0]
    assert ccs == [pre]
    assert undirected_contains_cycle
    # neighbors in reverse order, so larger cycle first, and in the opposite direction
    (
        parents,
        dists,
        pre,
        post,
        ccs,
        undirected_contains_cycle,
        directed_contains_cycle,
    ) = dfs(
        g,
        recursive=recursive,
        seed_order=Order.SORTED,
        neighbor_order=Order.REVERSE_SORTED,
    )
    assert parents == {0: None, 8: 0, 7: 8, 6: 7, 5: 6, 4: 5, 3: 0, 2: 3, 1: 2}
    assert dists == {0: 0, 8: 1, 7: 2, 6: 3, 5: 4, 4: 5, 3: 1, 2: 2, 1: 3}
    assert pre == [0, 8, 7, 6, 5, 4, 3, 2, 1]
    assert post == [4, 5, 6, 7, 8, 1, 2, 3, 0]
    assert ccs == [pre]
    assert undirected_contains_cycle
    # now start at 8
    (
        parents,
        dists,
        pre,
        post,
        ccs,
        undirected_contains_cycle,
        directed_contains_cycle,
    ) = dfs(
        g,
        recursive=recursive,
        seed_order=8,
        neighbor_order=Order.REVERSE_SORTED,
    )
    assert parents == {8: None, 7: 8, 6: 7, 5: 6, 4: 5, 0: 4, 3: 0, 2: 3, 1: 2}
    assert dists == {8: 0, 7: 1, 6: 2, 5: 3, 4: 4, 0: 5, 3: 6, 2: 7, 1: 8}
    assert pre == [8, 7, 6, 5, 4, 0, 3, 2, 1]
    assert post == [1, 2, 3, 0, 4, 5, 6, 7, 8]
    assert ccs == [pre]
    assert undirected_contains_cycle

    # add node 9, add 0-9 edge, start at 9
    g.add_node(9)
    g.add_edge((0, 9))
    (
        parents,
        dists,
        pre,
        post,
        ccs,
        undirected_contains_cycle,
        directed_contains_cycle,
    ) = dfs(
        g,
        recursive=recursive,
        seed_order=Order.REVERSE_SORTED,
        neighbor_order=Order.SORTED,
    )
    assert parents == {9: None, 0: 9, 1: 0, 2: 1, 3: 2, 4: 0, 5: 4, 6: 5, 7: 6, 8: 7}
    assert dists == {9: 0, 0: 1, 1: 2, 2: 3, 3: 4, 4: 2, 5: 3, 6: 4, 7: 5, 8: 6}
    assert pre == [9, 0, 1, 2, 3, 4, 5, 6, 7, 8]
    assert post == [3, 2, 1, 8, 7, 6, 5, 4, 0, 9]
    assert ccs == [pre]
    assert undirected_contains_cycle

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
    (
        parents,
        dists,
        pre,
        post,
        ccs,
        undirected_contains_cycle,
        directed_contains_cycle,
    ) = dfs(
        g,
        recursive=recursive,
        seed_order=9,
        neighbor_order=Order.SORTED,
    )
    assert parents == {
        9: None,
        0: 9,
        1: 0,
        2: 1,
        3: 2,
        4: 0,
        5: 4,
        6: 5,
        7: 6,
        8: 7,
        10: 0,
        11: 10,
        12: 11,
        13: 12,
        14: 11,
        15: 14,
        16: 15,
        17: 16,
        18: 17,
        19: 18,
        20: 19,
    }
    assert dists == {
        9: 0,
        0: 1,
        1: 2,
        2: 3,
        3: 4,
        4: 2,
        5: 3,
        6: 4,
        7: 5,
        8: 6,
        10: 2,
        11: 3,
        12: 4,
        13: 5,
        14: 4,
        15: 5,
        16: 6,
        17: 7,
        18: 8,
        19: 9,
        20: 10,
    }
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
    assert ccs == [pre]
    assert undirected_contains_cycle

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
    (
        parents,
        dists,
        pre,
        post,
        ccs,
        undirected_contains_cycle,
        directed_contains_cycle,
    ) = dfs(
        g, recursive=recursive, seed_order=Order.SORTED, neighbor_order=Order.SORTED
    )
    assert parents == {
        0: None,
        **{i: i - 1 for i in range(1, 8)},
        8: 2,
        **{i: i - 1 for i in range(9, 14)},
    }
    assert dists == {
        0: 0,
        **{i: i for i in range(1, 8)},
        8: 3,
        **{i: i - 5 for i in range(9, 14)},
    }
    assert pre == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    assert post == [7, 6, 5, 4, 3, 13, 12, 11, 10, 9, 8, 2, 1, 0]
    assert ccs == [pre]
    assert undirected_contains_cycle
    (
        parents,
        dists,
        pre,
        post,
        ccs,
        undirected_contains_cycle,
        directed_contains_cycle,
    ) = dfs(
        g,
        recursive=recursive,
        seed_order=Order.SORTED,
        neighbor_order=Order.REVERSE_SORTED,
    )
    assert parents == {
        0: None,
        7: 0,
        6: 7,
        5: 6,
        4: 5,
        3: 4,
        2: 3,
        10: 2,  # to go 13
        13: 10,
        12: 13,
        11: 12,
        9: 10,
        8: 9,
        1: 2,
    }
    assert dists == {
        0: 0,
        7: 1,
        6: 2,
        5: 3,
        4: 4,
        3: 5,
        2: 6,
        10: 7,  # to go 13
        13: 8,
        12: 9,
        11: 10,
        9: 8,
        8: 9,
        1: 7,
    }
    assert pre == [0, 7, 6, 5, 4, 3, 2, 10, 13, 12, 11, 9, 8, 1]
    assert post == [11, 12, 13, 8, 9, 10, 1, 2, 3, 4, 5, 6, 7, 0]
    assert ccs == [pre]
    assert undirected_contains_cycle

    # test disjoint graphs (disconnected components)
    g_spindly = GraphFactory.create_spindly_tree(3)
    exp_parents_spindly = {0: None, 1: 0, 2: 1}
    exp_dists_spindly = {0: 0, 1: 1, 2: 2}
    exp_pre_spindly = list(range(3))
    exp_post_spindly = exp_pre_spindly[::-1]
    g_b_ary = GraphFactory.create_b_ary_tree(2, 2)
    exp_parents_b_ary = {0: None, 1: 0, 2: 0, 3: 1, 4: 1, 5: 2, 6: 2}
    exp_dists_b_ary = {0: 0, 1: 1, 2: 1, 3: 2, 4: 2, 5: 2, 6: 2}
    exp_pre_b_ary = [0, 1, 3, 4, 2, 5, 6]
    exp_post_b_ary = [3, 4, 1, 5, 6, 2, 0]
    # See 8 node binary example in create_nearly_spindly_b_ary_tree docstring
    g_nearly_spindly_b_ary = GraphFactory.create_nearly_spindly_b_ary_tree(2, 8)
    exp_parents_nearly_spindly_b_ary = {
        0: None,
        1: 0,
        2: 0,
        3: 1,
        4: 1,
        5: 3,
        6: 3,
        7: 5,
    }
    exp_dists_nearly_spindly_b_ary = {
        0: 0,
        1: 1,
        2: 1,
        3: 2,
        4: 2,
        5: 3,
        6: 3,
        7: 4,
    }
    exp_pre_nearly_spindly_b_ary = [0, 1, 3, 5, 7, 6, 4, 2]
    exp_post_nearly_spindly_b_ary = [7, 5, 6, 3, 4, 1, 2, 0]
    g_custom = g  # above custom example
    exp_parents_custom = {
        0: None,
        **{i: i - 1 for i in range(1, 8)},
        8: 2,
        **{i: i - 1 for i in range(9, 14)},
    }
    exp_dists_custom = {
        0: 0,
        **{i: i for i in range(1, 8)},
        8: 3,
        **{i: i - 5 for i in range(9, 14)},
    }
    exp_pre_custom = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
    exp_post_custom = [7, 6, 5, 4, 3, 13, 12, 11, 10, 9, 8, 2, 1, 0]
    gs = (g_spindly, g_b_ary, g_nearly_spindly_b_ary, g_custom)
    g_combined = GraphFactory.concat_int_graphs(gs)
    exp_parents_seq = (
        exp_parents_spindly,
        exp_parents_b_ary,
        exp_parents_nearly_spindly_b_ary,
        exp_parents_custom,
    )
    exp_dists_seq = (
        exp_dists_spindly,
        exp_dists_b_ary,
        exp_dists_nearly_spindly_b_ary,
        exp_dists_custom,
    )
    exp_pres = (
        exp_pre_spindly,
        exp_pre_b_ary,
        exp_pre_nearly_spindly_b_ary,
        exp_pre_custom,
    )
    exp_posts = (
        exp_post_spindly,
        exp_post_b_ary,
        exp_post_nearly_spindly_b_ary,
        exp_post_custom,
    )
    lengths = [len(g) for g in gs]
    exp_parents = {}
    exp_dists = {}
    exp_pre = []
    exp_post = []
    exp_ccs = []
    for i, (pre, post, parents, dists) in enumerate(
        zip(exp_pres, exp_posts, exp_parents_seq, exp_dists_seq)
    ):
        offset = sum(lengths[:i])
        exp_parents.update(
            {
                offset + node: offset + parent if parent is not None else None
                for node, parent in parents.items()
            }
        )
        exp_dists.update({offset + node: dist for node, dist in dists.items()})
        exp_pre.extend([offset + node for node in pre])
        exp_post.extend([offset + node for node in post])
        exp_ccs.append([offset + node for node in pre])
    (
        parents,
        dists,
        pre,
        post,
        ccs,
        undirected_contains_cycle,
        directed_contains_cycle,
    ) = dfs(
        g_combined,
        recursive=recursive,
        seed_order=Order.SORTED,
        neighbor_order=Order.SORTED,
    )
    assert parents == exp_parents
    assert dists == exp_dists
    assert pre == exp_pre
    assert post == exp_post
    assert ccs == exp_ccs
    assert undirected_contains_cycle


@pytest.mark.parametrize("recursive", (True, False))
def test_dfs_undirected(recursive: bool) -> None:
    dg = Digraph(nodes=3, edges=((0, 1), (0, 2), (1, 2)))
    (
        parents,
        dists,
        pre,
        post,
        ccs,
        undirected_contains_cycle,
        directed_contains_cycle,
    ) = dfs(
        dg,
        recursive=recursive,
        seed_order=Order.SORTED,
        neighbor_order=Order.SORTED,
    )
    assert parents == {0: None, 1: 0, 2: 1}
    assert dists == {0: 0, 1: 1, 2: 2}
    assert pre == [0, 1, 2]
    assert post == [2, 1, 0]
    assert ccs == [[0, 1, 2]]
    assert not directed_contains_cycle

    dg = Digraph(nodes=3, edges=((0, 1), (1, 2), (2, 0)))
    (
        parents,
        dists,
        pre,
        post,
        ccs,
        undirected_contains_cycle,
        directed_contains_cycle,
    ) = dfs(
        dg,
        recursive=recursive,
        seed_order=Order.SORTED,
        neighbor_order=Order.SORTED,
    )
    assert parents == {0: None, 1: 0, 2: 1}
    assert dists == {0: 0, 1: 1, 2: 2}
    assert pre == [0, 1, 2]
    assert post == [2, 1, 0]
    assert ccs == [[0, 1, 2]]
    assert directed_contains_cycle

    dg = DigraphFactory.create_complete_digraph(4)
    (
        parents,
        dists,
        pre,
        post,
        ccs,
        undirected_contains_cycle,
        directed_contains_cycle,
    ) = dfs(
        dg,
        recursive=recursive,
        seed_order=Order.REVERSE_SORTED,
        neighbor_order=Order.REVERSE_SORTED,
    )
    assert parents == {3: None, 2: 3, 1: 2, 0: 1}
    assert dists == {3: 0, 2: 1, 1: 2, 0: 3}
    assert pre == [3, 2, 1, 0]
    assert post == [0, 1, 2, 3]
    assert ccs == [[3, 2, 1, 0]]
    assert directed_contains_cycle
