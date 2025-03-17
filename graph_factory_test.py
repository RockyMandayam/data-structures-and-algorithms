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
