from collections.abc import Iterable, Hashable, Mapping, Iterator, Collection
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
        _neighbors (Mapping[Hashable, set]): Map from node to its neighbors (a set is used for neighbors - no duplicates!)
        _num_edges (int): number of edges
        _name (str): name of graph
    """

    def __init__(
        self,
        nodes: Mapping[Hashable, Mapping] | Iterable[Hashable] | int | None = None,
        edges: Mapping[tuple[Hashable, Hashable], Mapping] | Iterable[tuple[Hashable, Hashable]] | None = None,
        name: str | None = None,
        skip_duplicate_edges: bool = False
    ) -> None:
        if nodes is None:
            nodes = {}
        if edges is None:
            edges = {}
        
        if nodes:
            # if nodes is int, convert to iterable from 0...n-1
            if isinstance(nodes, int):
                if nodes < 0:
                    raise ValueError("Graph must have a non-negative number of nodes.")
                nodes = range(nodes)
            # if nodes is Iterable[Hashable], convert to mapping (Mapping is also Iterable, so instead of checking
            # isinstance of Iterable, check not isinstance of Mapping)
            if not isinstance(nodes, Mapping):
                # nodes is Iterable[Hashable]; convert to Mapping format
                # use temp nodes_map name to not override 'nodes' name
                nodes_map: Mapping[Hashable, Mapping] = {}
                for node in nodes:
                    if node is None:
                        raise ValueError("None is not a valid node.")
                    if node in nodes_map:
                        raise ValueError(f"Found duplicate node {node=}; duplicate nodes not allowed")
                    nodes_map[node] = {}
                nodes = nodes_map
            if None in nodes:
                raise ValueError("None is not a valid node")
            # if nodes is passed in as a map, it can't have any duplicates since map keys are unique
        
        if edges:
            if not isinstance(edges, Mapping):
                # edges is Iterable[tuple[Hashable, Hashable]]; convert to Mapping[tuple[Hashable, Hashable], Mapping] format
                # use temp 'edges_map' name to not override 'edges' name
                edges_map: Mapping[(Hashable, Hashable), Mapping] = {}
                for edge in edges:
                    if edge is None:
                        raise ValueError("Edges cannot be None.")
                    u, v = edge
                    if u == v:
                        raise ValueError(f"Found self-loop for node {u}; self-loops are not allowed.")
                    if (u,v) in edges_map or (v,u) in edges_map:
                        if skip_duplicate_edges:
                            # don't want to add (u,v) and (v,u), just skip this
                            continue
                        else:
                            raise ValueError(f"Found duplicate edge {(u,v)}; duplicate edges not allowed")
                    edges_map[(u,v)] = {}
                edges = edges_map
            if None in edges:
                raise ValueError("None is not a valid edge")
            # if edges is already a Mapping, it can have duplicates (by having (u,v) and (v,u) which represent
            # the same edge), and it can have a self-loop. So I have to check again for these here. But it can't
            # have "explicit duplicates" in that it can't repeat (u,v) twice
            cleaned_edges = {}
            for u, v in edges:
                if u == v:
                    raise ValueError(f"Found self-loop for node {u}; self-loops are not allowed.")
                if (u,v) in cleaned_edges or (v,u) in cleaned_edges:
                    if skip_duplicate_edges:
                        continue
                    else:
                        raise ValueError(f"Found duplicate edge {(u,v)}; duplicate edges not allowed")
                cleaned_edges[(u,v)] = edges[(u,v)]
            edges = cleaned_edges

            for u, v in edges:
                if u not in nodes:
                    raise ValueError(f"Unknown node {u} found in edges.")
                if v not in nodes:
                    raise ValueError(f"Unknown node {v} found in edges.")
        
        
        if not nodes and edges:
            raise ValueError("Must provide nodes when providing edges")

        # instead of just storing all edges, use adjacency list representation
        neighbors: Mapping[Hashable, set] = {node: set() for node in nodes}
        num_edges = 0
        neighbors = {node: set() for node in nodes}
        for u, v in edges:
            neighbors[u].add(v)
            neighbors[v].add(u)
            num_edges += 1
        
        self._nodes = nodes
        self._neighbors = neighbors
        self._num_edges = num_edges
        self.name = name or ""
    
    def get_node_attribute(self, node: Hashable, key: Any) -> Any:
        # TODO maybe return copy
        return self._nodes[node][key]
    
    def get_node_attributes(self, node: Hashable) -> Mapping:
        # TODO maybe return copy
        return self._nodes[node]
    
    def __len__(self) -> int:
        return len(self._nodes)
    
    def num_edges(self) -> int:
        return self._num_edges
    
    def __str__(self) -> str:
        num_nodes = len(self)
        return f"Graph '{self.name}' with {num_nodes} node{'s' if num_nodes != 1 else ''} and {self._num_edges} edge{'s' if self._num_edges != 1 else ''}"
    
    def __iter__(self) -> Iterator:
        return iter(self._nodes)
    
    def __contains__(self, node: Hashable) -> bool:
        return node in self._nodes
    
    def __getitem__(self, node: Hashable) -> Iterable[Hashable]:
        return self._neighbors[node]
    
    def get_nodes(self) -> Collection[Hashable]:
        return self._nodes
    
    def is_edge(self, u: Hashable, v: Hashable) -> bool:
        """Returns True if (u,v) is an edge in this graph; False otherwise"""
        if u not in self._neighbors:
            raise ValueError(f"Node {u} not found.")
        if v not in self._neighbors:
            raise ValueError(f"Node {v} not found.")
        return v in self._neighbors[u] or u in self._neighbors[v]
    
    def are_edges(self, edges: Iterable[tuple[Hashable, Hashable]]) -> bool:
        """Returns True if all edges are in the graph; False otherwise"""
        return all(self.is_edge(edge) for edge in edges)
