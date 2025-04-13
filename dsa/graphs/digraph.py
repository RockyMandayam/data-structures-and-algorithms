from collections.abc import Hashable, Iterable, Mapping, Sequence

from dsa.graphs.graph import Graph


class Digraph(Graph):
    """Represents a directed graph.

    Restrictions:
        - No multple/parallel edges
        - No self-loops

    Attributes:
        name (str): name of graph
        _nodes (Mapping[Hashable, Mapping]): see Graph
        _edges (Mapping[tuple[Hashable, Hashable], tuple[float, Mapping]]): see Graph
        _incident_edges (Mapping[Hashable, set]): see Graph
        _out_edges (Mapping[Hashable, set]): Map from node to the out edges
        _in_edges (Mapping[Hashable, set]): Map from node to the in edges
    """

    def __init__(
        self,
        nodes: Mapping[Hashable, Mapping] | Iterable[Hashable] | int | None = None,
        edges: Mapping[tuple[Hashable, Hashable], tuple[float, Mapping]]
        | Mapping[tuple[Hashable, Hashable], Mapping]
        | Mapping[tuple[Hashable, Hashable], float]
        | Sequence[tuple[tuple[Hashable, Hashable], float]]
        | Sequence[tuple[Hashable, Hashable]]
        | None = None,
        name: str | None = None,
        skip_duplicate_edges: bool = False,
    ) -> None:
        # parent sets up _nodes, _edges, and _incident_edges
        super().__init__(nodes, edges, name, skip_duplicate_edges)
        # now we need to set up _out_edges and _in_edges
        self._out_edges: Mapping[Hashable, set] = {node: set() for node in self._nodes}
        self._in_edges: Mapping[Hashable, set] = {node: set() for node in self._nodes}
        for u, v in self._edges:
            self._out_edges[u].add((u, v))
            self._in_edges[v].add((u, v))

    @classmethod
    def _deduplicate_undirected_edges(
        cls,
        edges: Mapping[tuple[Hashable, Hashable], tuple],
        skip_duplicate_edges: bool,
    ) -> Mapping[tuple[Hashable, Hashable], tuple]:
        """Overrides parent method; do nothing, since in digraphs, you can have A->B and B->A"""
        return edges

    def __str__(self) -> str:
        return f"Directed {super().__str__()}"

    def __getitem__(self, node: Hashable) -> Sequence[Hashable]:
        """Override __getitem__ since we want only out-neighbors, not in-neighbors."""
        # KeyError desired if node not in self._out_edges
        return [v for (u, v) in self._out_edges[node]]

    def _get_canonical_edge(
        self, edge: tuple[Hashable, Hashable]
    ) -> tuple[Hashable, Hashable]:
        u, v = edge
        self._validate_node(u)
        self._validate_node(v)
        if (u, v) in self._edges:
            return (u, v)
        else:
            return None

    def add_node(self, node: Hashable) -> None:
        super().add_node(node)
        self._out_edges[node] = set()
        self._in_edges[node] = set()

    def add_edge(self, edge: tuple[Hashable, Hashable]) -> None:
        super().add_edge(edge)
        u, v = edge
        self._out_edges[u].add((u, v))
        self._in_edges[v].add((u, v))

    def remove_edge(self, edge: tuple[Hashable, Hashable]) -> None:
        """Removes edge if present; errors if not present"""
        super().remove_edge(edge)
        u, v = edge
        self._out_edges[u].remove((u, v))
        self._in_edges[v].remove((u, v))

    def get_out_degree(self, u: Hashable) -> int:
        self._validate_node(u)
        return len(self._out_edges[u])

    def get_in_degree(self, u: Hashable) -> int:
        self._validate_node(u)
        return len(self._in_edges[u])

    @property
    def A(self, node_order: list[Hashable] | None = None) -> list[list[int]]:
        # TODO cache for efficiency, but invalidate when graph is modified?
        if node_order is not None and len(node_order) != len(self):
            raise ValueError(
                f"If specifying node_order, it must include every node exactly once"
            )
        if node_order is None:
            try:
                nodes = sorted(self._nodes)
            except TypeError:
                raise ValueError(
                    "Must provide node_order since nodes are not sortable."
                )
        else:
            if len(node_order) != len(self):
                raise ValueError(
                    f"If specifying node_order, it must include every node exactly once"
                )
            nodes = node_order
        n = len(nodes)
        A = [[0 for _ in range(n)] for _ in range(n)]
        node_to_index = {}
        for index, node in enumerate(nodes):
            node_to_index[node] = index
        for u, v in self.get_edges():
            i, j = node_to_index[u], node_to_index[v]
            A[j][i] = 1
        return A
