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
        - is_edge
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
            Graph(nodes=(1,), edges={None: {}})
        with pytest.raises(ValueError):
            Graph(nodes=(1,), edges=(None,))
        with pytest.raises(ValueError):
            Graph(nodes=(1,), edges=iter((None,)))
        with pytest.raises(ValueError):
            Graph(nodes=(1,), edges=((0,1),))
        with pytest.raises(ValueError):
            Graph(nodes=(1,), edges=((1,None),))
        # now test with combination of valid and invalid nodes, and same for edges
        with pytest.raises(ValueError):
            Graph(nodes=(1, 0, None))
        with pytest.raises(ValueError):
            Graph(nodes=(0,1,2,), edges=((0,1), None))
        with pytest.raises(ValueError):
            Graph(nodes=(0,1,2,), edges=((0,1), (0, None)))
        with pytest.raises(ValueError):
            Graph(nodes=(0,1,2,), edges=((0,1), (0, -1)))
        
        g = Graph(nodes=(1,))
        with pytest.raises(ValueError):
            g.is_edge(2,1)
        with pytest.raises(ValueError):
            g.is_edge(1,2)
        with pytest.raises(ValueError):
            g.is_edge(2,3)

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
        assert not g.is_edge(1,1)
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
        assert not g.is_edge(1,1)
        assert not g.is_edge(2,2)
        assert not g.is_edge(1,2)
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
        assert g.is_edge(1,2)
        assert g.is_edge(2,1)
        assert not g.is_edge(1,1)
        assert not g.is_edge(2,2)
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
        assert g.is_edge(1, "test1")
        assert g.is_edge(1, 2)
        assert g.is_edge(2, "test1")
        assert g.is_edge("a", ("a", "b", "c"))
        assert not g.is_edge(1, "a")
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
    
    def test_create_complete_graph(self) -> None:
        # invalid k
        with pytest.raises(ValueError):
            Graph.create_complete_graph(-2)
        
        # empty graph
        g = Graph.create_complete_graph(0)
        assert len(g) == 0
        assert g.num_edges() == 0

        # 1, 2, and several nodes
        for k in (1, 2, 12):
            g = Graph.create_complete_graph(k)
            assert len(g) == k
            # this formula holds for edge cases of 1 and 2 nodes as well
            assert g.num_edges() == (k-1)*k/2
            for node in range(k):
                for other_node in range(node + 1, k):
                    if node != other_node:
                        assert g.is_edge(node, other_node)
                    else:
                        assert not g.is_edge(node, other_node)
    
    def test_create_spindly_tree(self) -> None:
        # invalid k
        with pytest.raises(ValueError):
            Graph.create_spindly_tree(-2)
        
        # empty graph
        g = Graph.create_spindly_tree(0)
        assert len(g) == 0
        assert g.num_edges() == 0

        # 1, 2, and several nodes
        for k in (1, 2, 12):
            g = Graph.create_spindly_tree(k)
            assert len(g) == k
            # this formula holds for edge case of 1 node as well
            assert g.num_edges() == k-1
            for node in range(k):
                for other_node in range(node + 1, k):
                    if node + 1 == other_node:
                        assert g.is_edge(node, other_node)
                    else:
                        assert not g.is_edge(node, other_node)