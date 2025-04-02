from collections.abc import Iterable

from dsa.graphs.graph import Graph


class GraphFactory:
    @staticmethod
    def concat_int_graphs(graphs: Iterable[Graph]) -> Graph:
        """Given graphs with non-negative int nodes, "concatenate" graphs to create a new graph which just includes all the given
        graphs put together but disconnected - since nodes will conflict, make them distinct by adding an offset
        to each graph so its nodes are all values which are higher than the previous nodes. See example below.

        E.g., graphs = [create_complete_graph(3), create_spindly_tree(5)]
        So graphs[0] has nodes 0,1,2 and edges (0,1),(0,2),(1,2).
        And graphs[1] has nodes 0,1,2,3 and edges (0,1),(1,2),(2,3),(3,4)
        The concatenated graph is:
        nodes: 0,1,2,3,4,5,6,7 where 0,1,2 are from dsa.graphs[0] and 3,4,5,6,7 are from dsa.graphs[1]
        edges: (0,1),(0,2),(1,2) from dsa.graphs[0] and (3,4),(4,5),(5,6),(6,7) from dsa.graphs[1]
        """
        num_nodes = 0
        edges = []
        for g in graphs:
            assert all(isinstance(node, int) for node in g)
            edges.extend([(u + num_nodes, v + num_nodes) for (u, v) in g.get_edges()])
            num_nodes += len(g)
        return Graph(nodes=range(num_nodes), edges=edges)

    @staticmethod
    def create_complete_graph(k: int) -> Graph:
        """Creates a complete graph with k nodes where each node is an int (k must be non-negative)."""
        if k < 0:
            raise ValueError("k must be non-negative.")
        nodes = tuple(range(k))
        edges = []
        for u in range(k):
            for v in range(u + 1, k):
                edges.append((u, v))
        return Graph(nodes, edges)

    @staticmethod
    def create_spindly_tree(k: int) -> Graph:
        """Creates a 'spindly tree' (i.e., no branching, all nodes in one line) with k nodes where each node
        is an int (k must be non-negative)."""
        if k < 0:
            raise ValueError("k must be non-negative")
        nodes = tuple(range(k))
        edges = list((i, i + 1) for i in range(k - 1))
        return Graph(nodes, edges)

    @staticmethod
    def create_b_ary_tree(b: int, depth: int) -> Graph:
        """Creates an b-ary tree with the given depth.

        E.g., b=2, depth=2
                    0
            1               2
        3       4       5       6

        Args:
            b: Positive branching factor
            depth: Non-negative 0-indexed depth (depth of 0 means graph with one node)

        Returns:
            Graph: nary tree
        """
        if b <= 0:
            raise ValueError("b must be postiive.")
        if depth < 0:
            raise ValueError("depth must be non-negative.")
        # b-ary tree has b^0 + b^1 + ... + b^(depth) nodes
        # that geometric series sums to (b**(depth+1)-1)/(b-1)
        n = (b ** (depth + 1) - 1) // (b - 1) if b != 1 else depth + 1
        # edges: go node by node and add its child
        # child = b*parent + k for k in 1, ..., b
        # 0->1, 0->2
        #   1->3, 1->4
        #   2->5, 2->6
        # 0->1, 0->2, 1->3
        #   1->4, 1->5, 1->6
        #   2->7, 2->8, 2-> 9
        edges = []
        for parent in range(n):
            for k in range(1, b + 1):
                child = b * parent + k
                if child < n:
                    edges.append((parent, child))
        return Graph(nodes=n, edges=edges)

    @staticmethod
    def create_nearly_spindly_b_ary_tree(b: int, n: int) -> Graph:
        """Creates a "nearly" spindly tree by "fattening" by one node at each level.

        Example with 8 nodes, 2-ary tree:
        the "left branch" is 0, 1, 3, 5, 7, ... and 0, 1, 3 have one right child leaf
                                0
                        1           2
                3           4
            5       6
        7

        Example with 10 nodes, 3-ary tree:
                                0
                    1               2       3
            4           5   6
        7     8  9

        """
        if b <= 0:
            raise ValueError("b must be positive.")
        if n < 0:
            raise ValueError("n must be non-negative")
        nodes = tuple(range(n))

        edges = []
        for child_of_zero in range(1, b + 1):
            if child_of_zero < n:
                edges.append((0, child_of_zero))
        for node_on_long_branch in range(1, n, b):
            for child in range(node_on_long_branch + b, node_on_long_branch + b + b):
                if child < n:
                    edges.append((node_on_long_branch, child))
        return Graph(nodes=nodes, edges=edges)

    @staticmethod
    def create_look_ahead_graph(n: int, look_ahead: int) -> Graph:
        """Create "look ahead" graph, described below, with n nodes and a "look ahead" distance of look_ahead.

        (This is like a DAG structure if you draw it out, but it's undirected, not driected)

        E.g., n=5, look_ahead=2
        0, 1, 2, 3, 4
        0->1, 0->2
        1->2, 1->3
        2->3, 2->4
        3->4
        """
        if n < 0:
            raise ValueError("n must be non-negative")
        if look_ahead < 0:
            raise ValueError("look_ahead must be non-negative")
        nodes = list(range(n))
        edges = []
        for parent in nodes:
            for child in range(parent + 1, parent + look_ahead + 1):
                if child < n:
                    edges.append((parent, child))
        return Graph(nodes=nodes, edges=edges)

    @staticmethod
    def create_cycle(n: int) -> Graph:
        """Creates a circuit (cycle) of n nodes.

        n must be at least 3, since to create a valid circuit (closed walk that does not repeat edges),
        you need at least 3 nodes.
        """
        if n < 3:
            raise ValueError("n must be at least 3")
        return Graph(nodes=range(n), edges=[(i, (i + 1) % n) for i in range(n)])
