from collections.abc import Iterable, Hashable, Mapping, Iterator
from typing import Any

class Graph:
    """Represents an undireccted graph.
    
    At first, I was going to have nodes just be ints, but if I later want to have node attributes, that
    becomes annoying. I could create a node class, but I'm going to follow networkx library's approach of just having a node be
    any hashable object (except that None is not allowed)

    Restrictions:
        - No multple/parallel edges
        - No self-loops
    
    Attributes:
        nodes (Mapping[Hashable, Mapping]): Map from node (a Hashable) to its attributes (a Mapping).
        neighbors (Mapping[Hashable, set]): Map from node to its neighbors (a set is used for neighbors - no duplicates!)
        num_edges (int): number of edges
        name (str): name of graph
    """

    def __init__(
        self,
        nodes: Mapping[Hashable, Mapping] | Iterable[Hashable] | None = None,
        edges: Mapping[tuple[Hashable, Hashable], Mapping] | Iterable[tuple[Hashable, Hashable]] | None = None,
        name: str | None = None,
        skip_duplicate_edges: bool = False
    ) -> None:
        if nodes is None:
            nodes = {}
        if edges is None:
            edges = {}
        if None in nodes:
            raise ValueError("None is not a valid node")
        if None in edges:
            raise ValueError("None is not a valid edge")
        
        if not nodes and edges:
            raise ValueError("Must provide nodes when providing edges")
        
        if nodes and not isinstance(nodes, Mapping):
            # nodes is Iterable[Hashable]; convert to Mapping format
            # use temp nodes_map name to not override 'nodes' name
            nodes_map: Mapping[Hashable, Mapping] = {}
            for node in nodes:
                if node in nodes_map:
                    raise ValueError(f"Found duplicate node {node=}; duplicate nodes not allowed")
                nodes_map[node] = {}
            nodes = nodes_map
        # if nodes is passed in as a map, it can't have any duplicates

        if edges:
            if not isinstance(edges, Mapping):
                # edges is Iterable[tuple[Hashable, Hashable]]; convert to Mapping[tuple[Hashable, Hashable], Mapping] format
                # use temp 'edges_map' name to not override 'edges' name
                edges_map: Mapping[(Hashable, Hashable), Mapping] = {}
                for u, v in edges:
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