from graphs.graph import Graph

class GraphFactory:
    
    @staticmethod
    def create_complete_graph(k: int) -> "Graph":
        """Creates a complete graph with k nodes where each node is an int (k must be non-negative)."""
        if k < 0:
            raise ValueError("k must be non-negative.")
        nodes = tuple(range(k))
        edges = []
        for u in range(k):
            for v in range(u+1, k):
                edges.append((u,v))
        return Graph(nodes, edges)
    
    @staticmethod
    def create_spindly_tree(k: int) -> "Graph":
        """Creates a 'spindly tree' (i.e., no branching, all nodes in one line) with k nodes where each node
        is an int (k must be non-negative)."""
        if k < 0:
            raise ValueError("k must be non-negative")
        nodes = tuple(range(k))
        edges = list((i, i+1) for i in range(k-1))
        return Graph(nodes, edges)
