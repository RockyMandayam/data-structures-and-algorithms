import random

import pytest

from dsa.graphs.digraph import Digraph
from dsa.graphs.digraph_factory import DigraphFactory


class TestDigraphFactory:
    def test_concat_int_digraphs(self) -> None:
        # two empty graphs
        g = Digraph()
        h = DigraphFactory.concat_int_digraphs((g, g))
        assert len(h) == 0

        # two singleton graphs
        g = Digraph(nodes=1)
        h = DigraphFactory.concat_int_digraphs((g, g))
        assert len(h) == 2
        assert set(h.get_nodes()) == set((0, 1))

        # example from concat_int_digraphs docstring
        h = DigraphFactory.concat_int_digraphs(
            (
                DigraphFactory.create_complete_digraph(3),
                DigraphFactory.create_spindly_tree(5),
            )
        )
        # So graphs[0] has nodes 0,1,2 and edges (0,1),(0,2),(1,2).
        # And graphs[1] has nodes 0,1,2,3 and edges (0,1),(1,2),(2,3),(3,4)
        assert len(h) == 8
        assert set(range(8)) == set(h.get_nodes())
        assert h.are_edges(((0, 1), (0, 2), (1, 2), (3, 4), (4, 5), (5, 6), (6, 7)))

    def test_create_complete_digraph(self) -> None:
        # invalid k
        with pytest.raises(ValueError):
            DigraphFactory.create_complete_digraph(-2)

        # empty graph
        g = DigraphFactory.create_complete_digraph(0)
        assert len(g) == 0
        assert g.num_edges() == 0

        # 1, 2, and several nodes
        # TODO why is this so slow with 2**big_number
        for k in (1, 2, random.randint(3, 2**8)):
            g = DigraphFactory.create_complete_digraph(k)
            assert len(g) == k
            # this formula holds for edge cases of 1 and 2 nodes as well
            assert g.num_edges() == (k - 1) * k
            for node in range(k):
                for other_node in range(node + 1, k):
                    if node != other_node:
                        assert g.is_edge((node, other_node))
                        assert g.is_edge((other_node, node))
                    else:
                        assert not g.is_edge((node, other_node))
                        assert not g.is_edge((other_node, node))

    def test_create_spindly_tree(self) -> None:
        # invalid k
        with pytest.raises(ValueError):
            DigraphFactory.create_spindly_tree(-2)

        # empty graph
        g = DigraphFactory.create_spindly_tree(0)
        assert len(g) == 0
        assert g.num_edges() == 0

        # 1, 2, and several nodes
        for k in (1, 2, 12):
            g = DigraphFactory.create_spindly_tree(k)
            assert len(g) == k
            # this formula holds for edge case of 1 node as well
            assert g.num_edges() == k - 1
            for node in range(k):
                for other_node in range(node + 1, k):
                    if node + 1 == other_node:
                        assert g.is_edge((node, other_node))
                        assert not g.is_edge((other_node, node))
                    else:
                        assert not g.is_edge((node, other_node))
                        assert not g.is_edge((other_node, node))

    def test_create_b_ary_tree(self) -> None:
        # invalid b, depth
        with pytest.raises(ValueError):
            DigraphFactory.create_b_ary_tree(-1, 2)
        with pytest.raises(ValueError):
            DigraphFactory.create_b_ary_tree(2, -1)

        # depth 0
        g = DigraphFactory.create_b_ary_tree(2, 0)
        assert len(g) == 1

        # b=1, depth=1
        g = DigraphFactory.create_b_ary_tree(1, 1)
        assert len(g) == 2
        assert g.num_edges() == 1
        assert g.is_edge((0, 1))

        # b=2, depth=1
        g = DigraphFactory.create_b_ary_tree(2, 1)
        assert len(g) == 3
        assert g.num_edges() == 2
        assert g.is_edge((0, 1))
        assert g.is_edge((0, 2))

        # b=1, depth=2
        g = DigraphFactory.create_b_ary_tree(1, 2)
        assert len(g) == 3
        assert g.num_edges() == 2
        assert g.is_edge((0, 1))
        assert g.is_edge((1, 2))

        # b=2, depth=2
        g = DigraphFactory.create_b_ary_tree(2, 2)
        assert len(g) == 7
        assert g.num_edges() == 6
        assert g.are_edges(((0, 1), (0, 2), (1, 3), (1, 4), (2, 5), (2, 6)))

        # test b and depth chosen at random in arbitrary range
        for b in (3, random.randint(4, 6)):
            for depth in (3, random.randint(4, 6)):
                g = DigraphFactory.create_b_ary_tree(b, depth)
                assert len(g) == (b ** (depth + 1) - 1) / (b - 1)
                assert g.num_edges() == len(g) - 1

    def test_create_nearly_spindly_b_ary_tree(self) -> None:
        # invalid b, n
        with pytest.raises(ValueError):
            DigraphFactory.create_nearly_spindly_b_ary_tree(0, 2)
        with pytest.raises(ValueError):
            DigraphFactory.create_nearly_spindly_b_ary_tree(1, -1)

        # n=0
        g = DigraphFactory.create_nearly_spindly_b_ary_tree(random.randint(1, 10), 0)
        assert len(g) == 0

        # n=1
        g = DigraphFactory.create_nearly_spindly_b_ary_tree(random.randint(1, 10), 1)
        assert len(g) == 1

        # n=2
        g = DigraphFactory.create_nearly_spindly_b_ary_tree(random.randint(1, 10), 2)
        assert len(g) == 2
        assert g.num_edges() == 1

        # b=1, n=3
        g = DigraphFactory.create_nearly_spindly_b_ary_tree(1, 3)
        assert len(g) == 3
        assert g.num_edges() == 2
        assert g.are_edges(((0, 1), (1, 2)))

        # b=2, n=3
        g = DigraphFactory.create_nearly_spindly_b_ary_tree(2, 3)
        assert len(g) == 3
        assert g.num_edges() == 2
        assert g.are_edges(((0, 1), (0, 2)))

        # 8 node binary example in docstring
        g = DigraphFactory.create_nearly_spindly_b_ary_tree(2, 8)
        assert len(g) == 8
        assert g.num_edges() == 7

        exp_edges = [(0, 1), (0, 2), (1, 3), (1, 4), (3, 5), (3, 6), (5, 7)]
        assert g.are_edges(exp_edges)

        # same but with 9 nodes
        g = DigraphFactory.create_nearly_spindly_b_ary_tree(2, 9)
        assert len(g) == 9
        assert g.num_edges() == 8
        exp_edges.append((5, 8))
        assert g.are_edges(exp_edges)

        # 10 node 3-ary example in docstring
        g = DigraphFactory.create_nearly_spindly_b_ary_tree(3, 10)
        assert len(g) == 10
        assert g.num_edges() == 9
        exp_edges = [
            (0, 1),
            (0, 2),
            (0, 3),
            (1, 4),
            (1, 5),
            (1, 6),
            (4, 7),
            (4, 8),
            (4, 9),
        ]
        assert g.are_edges(exp_edges)

        # same with 11 nodes
        g = DigraphFactory.create_nearly_spindly_b_ary_tree(3, 11)
        assert len(g) == 11
        assert g.num_edges() == 10
        exp_edges.append((7, 10))
        assert g.are_edges(exp_edges)

        # same with 12 nodes
        g = DigraphFactory.create_nearly_spindly_b_ary_tree(3, 12)
        assert len(g) == 12
        assert g.num_edges() == 11
        exp_edges.append((7, 11))
        assert g.are_edges(exp_edges)

    def test_create_look_ahead_digraph(self) -> None:
        # invalid n, look_ahead
        with pytest.raises(ValueError):
            DigraphFactory.create_look_ahead_digraph(-1, 1)
        with pytest.raises(ValueError):
            DigraphFactory.create_look_ahead_digraph(1, -1)

        # n=0
        g = DigraphFactory.create_look_ahead_digraph(0, 1)
        assert len(g) == 0

        # n=1
        g = DigraphFactory.create_look_ahead_digraph(1, 1)
        assert len(g) == 1

        # n=2, look_ahead=1
        g = DigraphFactory.create_look_ahead_digraph(2, 1)
        assert len(g) == 2
        assert g.num_edges() == 1

        # n=2, look_ahead=2, should be the same
        g = DigraphFactory.create_look_ahead_digraph(2, 2)
        assert len(g) == 2
        assert g.num_edges() == 1

        # n=3, look_ahead=1
        g = DigraphFactory.create_look_ahead_digraph(3, 1)
        assert len(g) == 3
        assert g.num_edges() == 2
        assert g.are_edges(((0, 1), (1, 2)))

        # n=3, look_ahead=2
        g = DigraphFactory.create_look_ahead_digraph(3, 2)
        assert len(g) == 3
        assert g.num_edges() == 3
        assert g.are_edges(((0, 1), (0, 2), (1, 2)))

        # n=5, look_ahead=2, see example in create_look_ahead_digraph docstring
        g = DigraphFactory.create_look_ahead_digraph(5, 2)
        assert len(g) == 5
        assert g.num_edges() == 7
        assert g.are_edges(((0, 1), (0, 2), (1, 2), (1, 3), (2, 3), (2, 4), (3, 4)))

    def test_create_cycle(self) -> None:
        # invalid graphs
        with pytest.raises(ValueError):
            DigraphFactory.create_cycle(-1)
        with pytest.raises(ValueError):
            DigraphFactory.create_cycle(0)
        with pytest.raises(ValueError):
            DigraphFactory.create_cycle(1)
        with pytest.raises(ValueError):
            DigraphFactory.create_cycle(2)

        # 3 nodes
        g = DigraphFactory.create_cycle(3)
        assert len(g) == 3
        assert g.num_edges() == 3
        assert g.are_edges(((0, 1), (1, 2), (2, 0)))
