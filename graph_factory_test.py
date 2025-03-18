import random

from graphs.graph import Graph

class GraphFactoryTest:
    def test_create_complete_graph(self) -> None:
        # invalid k
        with pytest.raises(ValueError):
            Graph.create_complete_graph(-2)
        
        # empty graph
        g = Graph.create_complete_graph(0)
        assert len(g) == 0
        assert g.num_edges() == 0

        # 1, 2, and several nodes
        # TODO why is this so slow with 2**big_number
        for k in (1, 2, random.randint(3, 2**8)):
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
    
    def test_create_b_ary_tree(self) -> None:
        # invalid b, depth
        with pytest.raises(ValueError):
            GraphFactory.create_b_ary_tree(-1, 2)
        with pytest.raises(ValueError):
            Graph(2, -1)
        
        # depth 0
        g = GraphFactory.create_b_ary_tree(2, 0)
        assert len(g) == 1

        # b=1, depth=1
        g = GraphFactory.create_b_ary_tree(1, 1)
        assert len(g) == 2
        assert g.num_edges() == 1

        # b=2, depth=1
        g = GraphFactory.create_b_ary_tree(2, 1)
        assert len(g) == 3
        assert g.num_edges() == 2
        assert g.is_edge(0, 1)
        assert g.is_edge(0, 2)

        # b=1, depth=2
        g = GraphFactory.create_b_ary_tree(1, 2)
        assert len(g) == 3
        assert g.num_edges() == 2
        assert g.is_edge(0, 1)
        assert g.is_edge(1, 2)

        # b=2, depth=2
        g = GraphFactory.create_b_ary_tree(2, 2)
        assert len(g) == 7
        assert g.num_edges(6)
        assert g.is_edge(0, 1)
        assert g.is_edge(0, 2)
        assert g.is_edge(1, 3)
        assert g.is_edge(1, 4)
        assert g.is_edge(2, 5)
        assert g.is_edge(2, 6)

        # test b and depth chosen at random in arbitrary range
        for b in (3, random.randint(4, 10)):
            for depth in (3, random.randint(4, 10)):
                g = GraphFactory.create_b_ary_tree(b, depth)
                assert len(g) == (b**(depth+1)-1)/(depth-1)
                assert g.num_edges() == len(g) - 1
    
    def test_create_nearly_spindly_b_ary_tree(self) -> None:
        # invalid b, n
        with pytest.raises(ValueError):
            GraphFactory.create_nearly_spindly_b_ary_tree(0, 2)
        with pytest.raises(ValueError):
            GraphFactory.create_nearly_spindly_b_ary_tree(1, -1)
        
        # n=0
        g = GraphFactory.create_nearly_spindly_b_ary_tree(random.randint(1,10), 0)
        assert len(g) == 0


        # n=1
        g = GraphFactory.create_nearly_spindly_b_ary_tree(random.randint(1,10), 1)
        assert len(g) == 1

        # n=2
        g = GraphFactory.create_nearly_spindly_b_ary_tree(random.randint(1,10), 2)
        assert len(g) == 2
        assert g.num_edges() == 1
        
        # 8 node binary example in docstring
        g = GraphFactory.create_nearly_spindly_b_ary_tree(2, 8)
        assert len(g) == 8
        assert g.num_edges() == 7
        exp_edges = [(0,1), (0,2), (1,3), (1,4), (3,5), (3,6), (5,7)]
        assert g.are_edges(exp_edges)

        # same but with 9 nodes
        g = GraphFactory.create_nearly_spindly_b_ary_tree(2, 9)
        assert len(g) == 9
        assert g.num_edges() == 8
        exp_edges.append((5,8))
        assert g.are_edges(exp_edges)

        # 10 node 3-ary example in docstring
        g = GraphFactory.create_nearly_spindly_b_ary_tree(3, 10)
        assert len(g) == 10
        assert g.num_edges() == 9
        exp_edges = [(0,1), (0,2), (0,3), (1,4), (1,5), (1,6), (4,7), (4,8), (4,9)]
        assert g.are_edges(exp_edges)

        # same with 11 nodes
        g = GraphFactory.create_nearly_spindly_b_ary_tree(3, 11)
        assert len(g) == 11
        assert g.num_edges() == 10
        exp_edges.append((7,10))
        assert g.are_edges(exp_edges)

        # same with 12 nodes
        g = GraphFactory.create_nearly_spindly_b_ary_tree(3, 12)
        assert len(g) == 12
        assert g.num_edges() == 11
        exp_edges.append((7,11))
        assert g.are_edges(exp_edges)
