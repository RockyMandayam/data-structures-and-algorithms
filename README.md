# data-structures-and-algorithms

Implementing data structures & algorithms to better my understanding. In particular, trying to implement them in ways that reveal the intuition and show similarities between the different algorithms.

Functionalities implemented (often with option to specify the type of algorithm, e.g., using DFS vs BFS, or an entirely different underlying algorithm for cycle detection in a graph):
    - graphs (undirected and directed)
        - centrality:
            - node centrality:
                - degree centrality, including in-degree and out-degree centralities for directed graphs
                - eigenvector centrality
        - traversals:
            - DFS (recursive and iterative implementation): returns traversal tree (via parents map), distances along this tree, preorder, postorder, connected components, and whether the graph is cyclic
            - BFS: returns traversal tree, distances along this tree, level order, connected components, and whether the graph is cyclic (for undirected graphs)
            - Dijkstra: returns traversal tree, distances, distance order, connected components,  and whether the graph is cyclic (for undirected graphs)
        - connected components: find connected components (undirected graph) or strongly connected components (directed graph)
        - cycles:
            - determine if graph is cyclic (can use a traversal-based algorithm or disjoint sets data structure based algorithm)
        - shortest paths:
            - find shortest paths from source to all other (connected) nodes
            - Bellman Ford algorithm for shortest paths with real weights (performs negative cycle detection)
            - Dijkstra for a more efficient serach when all edge weights are non-negative
            - BFS for most efficient search when you want to ignore edge weights where all edges are counted equally
        - topological sort: topologically sort a directed graph using DFS or BFS (Kahn's algorithm, not the normal BFS traversal)

TO DO:
    - connectedness:
        - find a bridge / all bridges
        - find an articulation point / all articulation points
    - undirected <-> directed
        - strong orientation
        - moralizing graph and related topics
    - spectral theory
    - walks
        - Eulerian walks and circuits
        - all walks of length n
            - with and without cycles?
        - shortest paths
            - A star algorithm
            - multiple sources shortest paths
            - all sources all shortest paths (Floyd-Warshall)
    - centrality
        - node centrality
            - betweenness centrality
            - shortest paths centrality
        - graph centrality
    - spanning trees
        - a (not necessarily minimum) spanning tree
        - MST
            - prim's algorithm
            - kruskal's algorithm
    - graphlets
    - max flow / min cut
    - bipartite graphs
        - detection using 2-coloring vs odd-length cycle
        - using DFS vs BFS
        - Kuhn's algorithm, Hungarian algorithm
        - using disjoint sets (weighted quick union data structure)?
    