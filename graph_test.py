from collections.abc import Callable, Mapping, Iterable

import pytest

from graphs.graph import Graph

class TestGraph:
    """Due to the nature fo this class, I think it makes more sense to test multiple functionalities in one test.
    E.g., makes sense to test __init__, __len__, __contains__, num_edges, etc. at once for an empty graph instead of 
    4 different functions. This is the approach taken in this test class for the following methods:
        - __init__
        - __len__
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
        with pytest.raises(ValueError):
            Graph(nodes={None: {}})
        with pytest.raises(ValueError):
            Graph(nodes=(None,))
        with pytest.raises(ValueError):
            Graph(nodes=(1,), edges={None: {}})
        with pytest.raises(ValueError):
            Graph(nodes=(1,), edges=(None,))

    @pytest.mark.parametrize("name", ("test_name", "", None))
    def test_empty_graph(self, name) -> None:
        # it should just not raise an error
        g = Graph(name=name)
        assert len(g) == 0
        assert g.num_edges() == 0
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
        ("nodes_iterable_factory", "edges_iterable_factory"),
        (
            (None, None),
            (lambda d: d.keys(), None),
            (tuple, lambda d: d.keys()),
            (list, tuple)
        )
    )
    def test_nontrivial_graphs(
        self,
        nodes_iterable_factory: Callable[[dict], Iterable] | None,
        edges_iterable_factory: Callable[[dict], Iterable] | None,
    ) -> None:
        """Tests __init__, __len__, num_edges, etc. methods for nontrivial graphs.

        Args:
            nodes_iterable_factory: For each test "case" within this test, it is initialized via a node to node attributes map.
                A graph can alternatively be initialized via an iterable of nodes. If nodes_iterable_factory is None, the map
                initializer is used. If nodes_iterable_factory is a callable, nodes_iterable_factory is used to convert the map
                to an iterable, which is used to initialize the graph. This makes sure to test both code paths.
            edges_iterable_factory: Just like with nodes, you can initialize edges via an edge attribute map or an iterable. If
                edges_iterable_factory is None, the map is used. If edges_iterable_factory is a callable, edges_iterable_factory is
                used to convert the map to an iterable which is used to initialize the graph. This makes sure to test both code paths.
        """
        ### test with one node
        nodes = {1: {}}
        if nodes_iterable_factory:
            nodes = nodes_iterable_factory(nodes)
        g = Graph(nodes=nodes)
        assert len(g) == 1
        assert g.num_edges() == 0
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
        
        ### test with one node and self-loop
        edges = {(1,1): {}}
        if edges_iterable_factory:
            edges = edges_iterable_factory(edges)
        with pytest.raises(ValueError):
            g = Graph(nodes=nodes, edges=edges)
        
        ### test with two nodes
        nodes = {1: {}, 2: {}}
        if nodes_iterable_factory:
            nodes = nodes_iterable_factory(nodes)
        g = Graph(nodes=nodes)
        assert len(g) == 2
        assert g.num_edges() == 0
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
        edges = {(1,3): {}}
        if edges_iterable_factory:
            edges = edges_iterable_factory(edges)
        with pytest.raises(ValueError):
            g = Graph(nodes=nodes, edges=edges)
        # test "explicit" duplicate using iterable format
        edges = ((1,2), (1,2))
        with pytest.raises(ValueError):
            g = Graph(nodes=nodes, edges=edges)
        # test "duplicate" (reversed order) edge
        edges = {(1,2): {}, (2,1): {}}
        if edges_iterable_factory:
            edges = edges_iterable_factory(edges)
        with pytest.raises(ValueError):
            g = Graph(nodes=nodes, edges=edges)
        # now allow it by enabling skip_duplicate_edges
        g = Graph(nodes=nodes, edges=edges, skip_duplicate_edges=True)
        assert len(g) == 2
        assert g.num_edges() == 1
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
        nodes = {1: {}, 2: {}, "test1": {}, ('a','b','c'): {}, 'a': {}, 'b': {}, 'c': {}}
        if nodes_iterable_factory:
            nodes = nodes_iterable_factory(nodes)
        edges = {(1, "test1"): {}, (2,1): {}, (2, "test1"): {}, ('a', ('a', 'b', 'c')): {}}
        if edges_iterable_factory:
            edges = edges_iterable_factory(edges)
        g = Graph(nodes=nodes, edges=edges)
        assert len(g) == 7
        assert g.num_edges() == 4
        assert str(g) == f"Graph '' with 7 nodes and 4 edges"
        self._test_iter(g, 7)
        assert 1 in g
        assert "test1" in g
        assert ('a', 'b', 'c') in g
        assert 'a' in g
        assert ('b', 'c') not in g
        assert None not in g
        assert len(g[1]) == 2
        assert len(g[2]) == 2
        assert len(g["test1"]) == 2
        assert len(g['a']) == 1
        assert len(g['b']) == 0
        with pytest.raises(KeyError):
            g[('a',)]
        with pytest.raises(KeyError):
            g[None]