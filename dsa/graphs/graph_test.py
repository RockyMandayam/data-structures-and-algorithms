import random
from collections.abc import Callable, Iterable, Mapping

import pytest

from dsa.graphs.graph import Graph
from dsa.graphs.graph_factory import GraphFactory


class TestGraph:
    """Due to the nature of this class, I think it makes more sense to test multiple functionalities in one test.
    E.g., makes sense to test __init__, __len__, __contains__, num_edges, etc. at once for an empty graph instead of
    4 different functions. This is the approach taken in this test class for the following methods:
        - __init__
        - __len__
        - get_nodes
        - is_edge
        - are_edges
        - num_edges
        - __str__
        - __iter__
        - __contains__
        - __getitem__
    """

    # TODO test node and edge attributes

    def _test_iter(self, g: Graph, exp_cnt: int) -> None:
        cnt = 0
        for _ in g:
            cnt += 1
        assert cnt == exp_cnt

    def test_init_invalid(self) -> None:
        # no None nodes or None edges, or edges referencing nonexistent nodes (including None nodes)
        # use iter() to make sure to try actual iterable non-sequences
        # (earlier, there was a bug with iterable non-sequences)
        with pytest.raises(ValueError):
            Graph(nodes={None: {}})
        with pytest.raises(ValueError):
            Graph(nodes=(None,))
        with pytest.raises(ValueError):
            Graph(nodes=iter((None,)))
        with pytest.raises(ValueError):
            Graph(nodes=-1)
        with pytest.raises(ValueError):
            Graph(nodes=(1,), edges=((0, 1),))
        with pytest.raises(ValueError):
            Graph(nodes=(1,), edges=((1, None),))
        # now test with combination of valid and invalid nodes, and same for edges
        with pytest.raises(ValueError):
            Graph(nodes=(1, 0, None))
        with pytest.raises(ValueError):
            Graph(
                nodes=(
                    0,
                    1,
                    2,
                ),
                edges=((0, 1), (0, None)),
            )
        with pytest.raises(ValueError):
            Graph(
                nodes=(
                    0,
                    1,
                    2,
                ),
                edges=((0, 1), (0, -1)),
            )

        g = Graph(nodes=(1,))
        with pytest.raises(ValueError):
            g.is_edge((2, 1))
        with pytest.raises(ValueError):
            g.is_edge((1, 2))
        with pytest.raises(ValueError):
            g.is_edge((2, 3))
        with pytest.raises(ValueError):
            g.is_edge((None, 0))
        with pytest.raises(ValueError):
            g.is_edge((0, None))
        assert g.are_edges([])
        with pytest.raises(ValueError):
            g.are_edges([(1, 2)])

    @pytest.mark.parametrize("name", ("test_name", "", None))
    def test_empty_graph(self, name) -> None:
        # it should just not raise an error
        g = Graph(name=name)
        assert len(g) == 0
        assert g.num_edges() == 0
        assert len(g.get_nodes()) == 0
        assert len(g.get_edges()) == 0
        with pytest.raises(ValueError):
            g.is_edge((0, 1))
        with pytest.raises(ValueError):
            g.are_edges([(0, 1)])
        name_str = name or ""
        assert str(g) == f"Graph '{name_str}' with 0 nodes and 0 edges"
        self._test_iter(g, 0)
        assert 1 not in g
        assert g not in g
        assert None not in g
        with pytest.raises(KeyError):
            g[-1]
        with pytest.raises(KeyError):
            g[None]

    @pytest.mark.parametrize(
        ("nodes_iterable_factory", "edges_sequence_factory"),
        (
            (None, None),
            (lambda d: d.keys(), None),
            (tuple, lambda d: list(d.keys())),
            (list, tuple),
        ),
    )
    def test_nontrivial_graphs(
        self,
        nodes_iterable_factory: Callable[[dict], Iterable] | None,
        edges_sequence_factory: Callable[[dict], Iterable] | None,
    ) -> None:
        """Tests __init__, __len__, num_edges, etc. methods for nontrivial graphs.

        Args:
            nodes_iterable_factory: For each test "case" within this test, it is initialized via a node to node attributes map.
                A graph can alternatively be initialized via an iterable of nodes. If nodes_iterable_factory is None, the map
                initializer is used. If nodes_iterable_factory is a callable, nodes_iterable_factory is used to convert the map
                to an iterable, which is used to initialize the graph. This makes sure to test both code paths.
            edges_sequence_factory: Just like with nodes, you can initialize edges via an edge attribute map or an iterable. If
                edges_sequence_factory is None, the map is used. If edges_sequence_factory is a callable, edges_sequence_factory is
                used to convert the map to an iterable which is used to initialize the graph. This makes sure to test both code paths.
        """
        ### test with one node
        nodes = {1: {}}
        if nodes_iterable_factory:
            nodes = nodes_iterable_factory(nodes)
        g = Graph(nodes=nodes)
        assert len(g) == 1
        assert tuple(g.get_nodes()) == (1,)
        assert g.num_edges() == 0
        assert not g.is_edge((1, 1))
        assert not g.are_edges([(1, 1)])
        assert len(g.get_edges()) == 0
        # note special case of singular 'node' (not 'nodes') for 1 node
        assert str(g) == f"Graph '' with 1 node and 0 edges"
        self._test_iter(g, 1)
        assert 1 in g
        assert 2 not in g
        assert None not in g
        len(g[1]) == 0
        with pytest.raises(KeyError):
            g[2]
        with pytest.raises(KeyError):
            g[None]

        ### test when nodes is an int
        g = Graph(nodes=1)
        assert len(g) == 1
        assert tuple(g.get_nodes()) == (0,)
        assert g.num_edges() == 0
        assert 0 in g
        assert 1 not in g

        ### test with one node and self-loop
        edges = {(1, 1): {}}
        if edges_sequence_factory:
            edges = edges_sequence_factory(edges)
        with pytest.raises(ValueError):
            g = Graph(nodes=nodes, edges=edges)

        ### test with two nodes
        nodes = {1: {}, 2: {}}
        if nodes_iterable_factory:
            nodes = nodes_iterable_factory(nodes)
        g = Graph(nodes=nodes)
        assert len(g) == 2
        assert sorted(g.get_nodes()) == [1, 2]
        assert g.num_edges() == 0
        assert not g.is_edge((1, 1))
        assert not g.is_edge((2, 2))
        assert not g.is_edge((1, 2))
        assert str(g) == f"Graph '' with 2 nodes and 0 edges"
        self._test_iter(g, 2)
        assert 1 in g
        assert 2 in g
        assert 3 not in g
        assert None not in g
        len(g[1]) == 0
        len(g[2]) == 0
        with pytest.raises(KeyError):
            g[3]
        with pytest.raises(KeyError):
            g[None]

        ### test with two nodes and an edge
        nodes = {1: {}, 2: {}}
        if nodes_iterable_factory:
            nodes = nodes_iterable_factory(nodes)
        # test edges referencing unknown nodes
        edges = {(1, 3): {}}
        if edges_sequence_factory:
            edges = edges_sequence_factory(edges)
        with pytest.raises(ValueError):
            g = Graph(nodes=nodes, edges=edges)
        # test "explicit" duplicate using iterable format
        edges = ((1, 2), (1, 2))
        with pytest.raises(ValueError):
            g = Graph(nodes=nodes, edges=edges)
        # test "duplicate" (reversed order) edge
        edges = {(1, 2): {}, (2, 1): {}}
        if edges_sequence_factory:
            edges = edges_sequence_factory(edges)
        with pytest.raises(ValueError):
            g = Graph(nodes=nodes, edges=edges)
        # now allow it by enabling skip_duplicate_edges
        g = Graph(nodes=nodes, edges=edges, skip_duplicate_edges=True)
        assert len(g) == 2
        assert sorted(g.get_nodes()) == [1, 2]
        assert g.num_edges() == 1
        assert g.is_edge((1, 2))
        assert g.is_edge((2, 1))
        assert not g.is_edge((1, 1))
        assert not g.is_edge((2, 2))
        assert g.are_edges([(1, 2), (2, 1)])
        assert g.are_edges([(1, 2), (2, 1), (1, 2)])
        assert not g.are_edges([(1, 2), (1, 1)])
        assert g.get_edges() == {(1, 2): (1, {})}
        # note special case of singular 'edge' (not 'edges') for 1 edge
        assert str(g) == f"Graph '' with 2 nodes and 1 edge"
        self._test_iter(g, 2)
        assert 1 in g
        assert 2 in g
        assert 3 not in g
        assert None not in g
        len(g[1]) == 1
        len(g[2]) == 1
        with pytest.raises(KeyError):
            g[3]
        with pytest.raises(KeyError):
            g[None]

        ### test several nodes and edges
        nodes = {
            1: {},
            2: {},
            "test1": {},
            ("a", "b", "c"): {},
            "a": {},
            "b": {},
            "c": {},
        }
        if nodes_iterable_factory:
            nodes = nodes_iterable_factory(nodes)
        edges = {
            (1, "test1"): {},
            (2, 1): {},
            (2, "test1"): {},
            ("a", ("a", "b", "c")): {},
        }
        if edges_sequence_factory:
            edges = edges_sequence_factory(edges)
        g = Graph(nodes=nodes, edges=edges)
        assert len(g) == 7
        assert len(g.get_nodes()) == 7 and set(g.get_nodes()) == set(
            (1, 2, "test1", ("a", "b", "c"), "a", "b", "c")
        )
        assert g.num_edges() == 4
        assert g.is_edge((1, "test1"))
        assert g.is_edge((1, 2))
        assert g.is_edge((2, "test1"))
        assert g.is_edge(("a", ("a", "b", "c")))
        assert not g.is_edge((1, "a"))
        assert g.are_edges([(1, 2), ("a", ("a", "b", "c"))])
        assert not g.are_edges([("a", 2), (1, 2)])
        assert str(g) == f"Graph '' with 7 nodes and 4 edges"
        self._test_iter(g, 7)
        assert 1 in g
        assert "test1" in g
        assert ("a", "b", "c") in g
        assert "a" in g
        assert ("b", "c") not in g
        assert None not in g
        assert len(g[1]) == 2
        assert len(g[2]) == 2
        assert len(g["test1"]) == 2
        assert len(g["a"]) == 1
        assert len(g["b"]) == 0
        with pytest.raises(KeyError):
            g[("a",)]
        with pytest.raises(KeyError):
            g[None]

    def test_add_node(self) -> None:
        # invalid nodes
        g = Graph()
        with pytest.raises(ValueError):
            g.add_node(None)
        g.add_node(0)
        assert len(g) == 1
        assert 0 in g
        with pytest.raises(ValueError):
            g.add_node(0)
        g.add_node(1)
        assert len(g) == 2
        assert 0 in g
        assert 1 in g
        self._test_iter(g, 2)

    def test_add_edge(self) -> None:
        # invalid edges
        g = Graph(nodes=4, edges=((1, 2),))
        with pytest.raises(ValueError):
            g.add_edge((None, None))
        with pytest.raises(ValueError):
            g.add_edge((1, 2))
        with pytest.raises(ValueError):
            g.add_edge((2, 1))

        # valid edges
        g.add_edge((2, 3))
        assert len(g) == 4
        assert sorted(g.get_nodes()) == [0, 1, 2, 3]
        assert g.num_edges() == 2
        for u in range(4):
            for v in range(4):
                if (u, v) in ((1, 2), (2, 1), (2, 3), (3, 2)):
                    assert g.is_edge((u, v))
                else:
                    assert not g.is_edge((u, v))
        assert g.are_edges([(2, 3)])
        assert not g.are_edges([(2, 3), (3, 1)])
        assert str(g) == f"Graph '' with 4 nodes and 2 edges"
        self._test_iter(g, 4)
        assert all(v in g for v in range(4))
        assert -1 not in g
        assert None not in g
        assert len(g[0]) == 0
        assert len(g[1]) == 1
        assert len(g[2]) == 2

    def test_add_edges(self) -> None:
        g = Graph(3)
        assert len(g) == 3
        assert g.num_edges() == 0

        g.add_edges(((0, 1), (0, 2)))
        assert len(g) == 3
        assert g.num_edges() == 2
        assert g.is_edge((1, 0))
        assert g.is_edge((2, 0))

    def test_A(self) -> None:
        # TODO test node_order
        g = Graph(3)
        assert g.A == [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

        g.add_edge((0, 2))
        assert g.A == [[0, 0, 1], [0, 0, 0], [1, 0, 0]]
        g.add_edge((0, 1))
        assert g.A == [[0, 1, 1], [1, 0, 0], [1, 0, 0]]

        g = GraphFactory.create_complete_graph(3)
        assert g.A == [[0, 1, 1], [1, 0, 1], [1, 1, 0]]

        # example: https://www.jsums.edu/nmeghanathan/files/2015/08/CSC641-Fall2015-Module-2-Centrality-Measures.pdf
        g = Graph(nodes=5, edges=((0, 1), (1, 3), (2, 3), (2, 4), (3, 4)))
        assert g.A == [
            [0, 1, 0, 0, 0],
            [1, 0, 0, 1, 0],
            [0, 0, 0, 1, 1],
            [0, 1, 1, 0, 1],
            [0, 0, 1, 1, 0],
        ]
