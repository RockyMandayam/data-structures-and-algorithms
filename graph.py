from collections.abc import Iterable, Hashable, Mapping, Iterator, Collection, Sequence
from typing import Any

class Graph:
    """Represents an undirected graph.
    
    At first, I was going to have nodes just be ints, but if I later want to have node attributes, that
    becomes annoying. I could create a node class, but I'm going to follow networkx library's approach of just having a node be
    any hashable object (except that None is not allowed).

    NOTE: for now, there is some "leakage" where mutable data can be exposed, e.g., via __iter__ and get_nodes.

    Restrictions:
        - No multple/parallel edges
        - No self-loops
    
    Attributes:
        _nodes (Mapping[Hashable, Mapping]): Map from node (a Hashable) to its attributes (a Mapping).
        _edges
        _neighbors (Mapping[Hashable, set]): Map from node to its neighbors (a set is used for neighbors - no duplicates!)
        _name (str): name of graph
    """

    def __init__(
        self,
        nodes: Mapping[Hashable, Mapping] | Iterable[Hashable] | int | None = None,
        edges: Mapping[tuple[Hashable, Hashable], Mapping] | Sequence[tuple[Hashable, Hashable]] | None = None,
        name: str | None = None,
        skip_duplicate_edges: bool = False,
    ) -> None:
        self.name = name or ""
        self._nodes = self._construct_and_validate_nodes(nodes)
        self._edges = Graph._construct_and_validate_edges(self._nodes, edges, skip_duplicate_edges)

        # adjacency list representation is easier for some tasks
        neighbors: Mapping[Hashable, set] = {node: set() for node in self._nodes}
        for u, v in self._edges:
            neighbors[u].add(v)
            neighbors[v].add(u)
        # NOTE: we are storing redundant info in edges and neighbors,
        # since each data structure is useful for different tasks
        # edges contains more info though, since it contains edge attributes
        self._neighbors = neighbors
    
    def _construct_and_validate_nodes(
        self,
        nodes: Mapping[Hashable, Mapping] | Iterable[Hashable] | int | None
    ) -> Mapping[Hashable, Mapping]:
        """Construct nodes Mapping by converting input nodes to the right format, and validate."""
        # handle None case
        if nodes is None:
            nodes = {}
        # handle int case: convert to iterable from 0...n-1
        if isinstance(nodes, int):
            if nodes < 0:
                raise ValueError("Graph must have a non-negative number of nodes.")
            nodes = range(nodes)
        # handle Iterable[Hashable] case: convert to mapping (Mapping is also Iterable, so instead of checking
        # isinstance of Iterable, check not isinstance of Mapping)
        if nodes and not isinstance(nodes, Mapping):
            # nodes is Iterable[Hashable]; convert to Mapping format
            # use temp nodes_map name to not override 'nodes' name
            nodes_map: Mapping[Hashable, Mapping] = {}
            for node in nodes:
                if node in nodes_map:
                    raise ValueError(f"Found duplicate node {node=}; duplicate nodes not allowed")
                nodes_map[node] = {}
            nodes = nodes_map
        # validate nodes
        if None in nodes:
            raise ValueError("None is not a valid node.")
        return nodes
    
    @staticmethod
    def _construct_and_validate_edges(
        nodes: Mapping[Hashable, Mapping],
        edges: Mapping[tuple[Hashable, Hashable], Mapping] | Sequence[tuple[Hashable, Hashable]] | None,
        skip_duplicate_edges: bool
    ) -> Mapping[tuple[Hashable, Hashable], Mapping]:
        """Construct edges Mapping by converting input edges to the right format, and validate."""
        # handle None case
        if edges is None:
            edges = {}
        # handle Iterable[tuple] case: convert to Mapping[tuple[Hashable, Hashable], Mapping] format
        # use temp 'edges_map' name to not override 'edges' name
        if edges and not isinstance(edges, Mapping):
            edges_map: Mapping[tuple(Hashable, Hashable), Mapping] = {(u,v): {} for (u,v) in edges}
            # easier way to check for duplicates than checking iteratively while adding edges
            if not skip_duplicate_edges and len(edges_map) != len(edges):
                raise ValueError("Duplicate edges not allowed")
            edges = edges_map
        # validate edges
        # if edges is already a Mapping, it can have duplicates (by having (u,v) and (v,u) which represent
        # the same edge), and it can have a self-loop. Check for these here. But it can't have "explicit duplicates"
        # in that it can't repeat (u,v) twice
        validated_edges = {}
        for u, v in edges:
            if u == v:
                raise ValueError(f"Found self-loop for node {u}; self-loops are not allowed.")
            if (v,u) in validated_edges:
                if skip_duplicate_edges:
                    continue
                else:
                    raise ValueError(f"Found duplicate edge {(u,v)}; duplicate edges not allowed")
            validated_edges[(u,v)] = edges[(u,v)]
        edges = validated_edges
        for u, v in edges:
            if u not in nodes:
                raise ValueError(f"Unknown node {u} found in edges.")
            if v not in nodes:
                raise ValueError(f"Unknown node {v} found in edges.")
        return edges
    
    
    def get_node_attribute(self, node: Hashable, key: Any) -> Any:
        # TODO maybe return copy
        return self._nodes[node][key]
    
    def get_node_attributes(self, node: Hashable) -> Mapping:
        # TODO maybe return copy
        return self._nodes[node]
    
    def __len__(self) -> int:
        return len(self._nodes)
    
    def num_edges(self) -> int:
        return len(self._edges)
    
    def __str__(self) -> str:
        num_nodes = len(self)
        return f"Graph '{self.name}' with {num_nodes} node{'s' if num_nodes != 1 else ''} and {self.num_edges()} edge{'s' if self.num_edges() != 1 else ''}"
    
    def __iter__(self) -> Iterator:
        return iter(self._nodes)
    
    def __contains__(self, node: Hashable) -> bool:
        return node in self._nodes
    
    def __getitem__(self, node: Hashable) -> Iterable[Hashable]:
        return self._neighbors[node]
    
    def get_nodes(self) -> Collection[Hashable]:
        return self._nodes
    
    def get_edges(self) -> Collection[Hashable]:
        return self._edges
    
    def is_edge(self, edge: tuple[Hashable, Hashable]) -> bool:
        """Returns True if edge= is an edge in this graph; False otherwise"""
        u, v = edge
        if u not in self._neighbors:
            raise ValueError(f"Node {u} not found.")
        if v not in self._neighbors:
            raise ValueError(f"Node {v} not found.")
        return v in self._neighbors[u] or u in self._neighbors[v]
    
    def are_edges(self, edges: Iterable[tuple[Hashable, Hashable]]) -> bool:
        """Returns True if all edges are in the graph; False otherwise"""
        return all(self.is_edge((u, v)) for u, v in edges)
    
    def add_node(self, node: Hashable, attributes: Mapping | None = None) -> None:
        """Adds node if not present and not None; errors if already present"""
        if node is None:
            raise ValueError("None is not a valid node.")
        if node in self._nodes:
            raise ValueError(f"Node {node=} already present in graph")
        self._nodes[node] = attributes
    
    def add_edge(self, u: Hashable, v: Hashable, attributes: Mapping | None = None) -> None:
        """Adds edge if not present; errors if also present"""
        if self.is_edge((u, v)):
            raise ValueError(f"Edge ({u}, {v}) already exists.")
        self._edges[(u,v)] = attributes
        self._neighbors[u].add(v)
