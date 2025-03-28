import math
from collections.abc import Collection, Hashable, Iterable, Iterator, Mapping, Sequence
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
        name (str): name of graph
        _nodes (Mapping[Hashable, Mapping]): Map from node (a Hashable) to its attributes (a Mapping).
        _edges (Mapping[tuple[Hashable, Hashable], tuple[float, Mapping]]): Map from edge (tuple of nodes (u,v)) to
            a tuple of the weight of the edge (float) and its attributes (Mapping)
            - NOTE: an edge (u,v) will be present as (u,v) or (v,u) but not both
        _neighbors (Mapping[Hashable, set]): Map from node to its neighbors (a set is used for neighbors - no duplicates!)
            - _neighbors will have the exact same nodes as _nodes, even nodes with no neighbors
            - NOTE: this does contain redundant information that is already present, but this adjacency set is useful for fast
                lookup of neighbors. Note that an edge (u,v) will manifest as v being a neighbor u and u being a neighbor of v
    """

    DEFAULT_EDGE_WEIGHT: float = 1

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
        self.name = name or ""
        self._nodes = Graph._construct_and_validate_nodes(nodes)
        self._edges = Graph._construct_and_validate_edges(
            self._nodes, edges, skip_duplicate_edges
        )
        self._incident_edges = Graph._construct_incident_edges(self._nodes, self._edges)

    @staticmethod
    def _construct_and_validate_nodes(
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
                    raise ValueError(
                        f"Found duplicate node {node=}; duplicate nodes not allowed"
                    )
                nodes_map[node] = {}
            nodes = nodes_map
        # validate nodes
        if None in nodes:
            raise ValueError("None is not a valid node.")
        return nodes

    @staticmethod
    def _construct_and_validate_edges(
        nodes: Mapping[Hashable, Mapping],
        edges: Mapping[tuple[Hashable, Hashable], tuple[float, Mapping]]
        | Mapping[tuple[Hashable, Hashable], Mapping]
        | Mapping[tuple[Hashable, Hashable], float]
        | Sequence[tuple[tuple[Hashable, Hashable], float]]
        | Sequence[tuple[Hashable, Hashable]]
        | None,
        skip_duplicate_edges: bool,
    ) -> Mapping[tuple[Hashable, Hashable], Mapping]:
        """Construct edges Mapping by converting input edges to the right format, and validate."""
        # handle None case
        if edges is None:
            edges = {}
        # handle Sequence[tuple[tuple[Hashable, Hashable], float]]: convert to
        # Sequence[tuple[tuple[Hashable, Hashable], float]]
        if (
            isinstance(edges, Sequence)
            and edges
            and edges[0]
            and isinstance(edges[0][0], Hashable)
        ):
            edges = [(edge, Graph.DEFAULT_EDGE_WEIGHT) for edge in edges]
        # handle Mapping[tuple[Hashable, Hashable], float]: convert to
        # Mapping[tuple[Hashable, Hashable], tuple[float, Mapping]] format
        if (
            isinstance(edges, Mapping)
            and edges
            and (
                isinstance(next(iter(edges.values())), float)
                or isinstance(next(iter(edges.values())), int)
            )
        ):
            edges = {edge: (weight, {}) for edge, weight in edges.items()}
        # handle Mapping[tuple[Hashable, Hashable], Mapping]: convert to
        # Mapping[tuple[Hashable, Hashable], tuple[float, Mapping]] format
        if (
            isinstance(edges, Mapping)
            and edges
            and isinstance(next(iter(edges.values())), Mapping)
        ):
            edges = {
                edge: (Graph.DEFAULT_EDGE_WEIGHT, attrs)
                for edge, attrs in edges.items()
            }
        # handle Sequence[tuple[tuple[Hashable, Hashable], float]]: convert to
        # Mapping[tuple[Hashable, Hashable], tuple[float, Mapping]] format
        if isinstance(edges, Sequence):
            edges_map: Mapping[tuple[Hashable, Hashable], tuple[float, Mapping]] = {
                (u, v): (weight, {}) for ((u, v), weight) in edges
            }
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
                raise ValueError(
                    f"Found self-loop for node {u}; self-loops are not allowed."
                )
            if (v, u) in validated_edges:
                if skip_duplicate_edges:
                    continue
                else:
                    raise ValueError(
                        f"Found duplicate edge {(u,v)}; duplicate edges not allowed"
                    )
            validated_edges[(u, v)] = edges[(u, v)]
        edges = validated_edges
        for u, v in edges:
            if u not in nodes:
                raise ValueError(f"Unknown node {u} found in edges.")
            if v not in nodes:
                raise ValueError(f"Unknown node {v} found in edges.")
        return edges

    @staticmethod
    def _construct_incident_edges(
        nodes: Mapping[Hashable, Mapping],
        edges: Mapping[tuple[Hashable, Hashable], tuple[float, Mapping]],
    ) -> Mapping[Hashable, set]:
        neighbors: Mapping[Hashable, set] = {node: set() for node in nodes}
        for u, v in edges:
            neighbors[u].add((u, v))
            # don't reverse order (u,v vs v,u) - keep one consistent grouth truth for edge in self._edges
            neighbors[v].add((u, v))
        return neighbors

    def get_node_attrs(self, node: Hashable) -> Mapping:
        if node not in self._nodes:
            raise ValueError(f"Unknown node {node=}")
        return self._nodes[node]

    def get_node_attr(self, node: Hashable, key: Any) -> Any:
        attrs = self.get_node_attrs(node)
        if key not in attrs:
            raise ValueError(f"Unknown node attribute key {key=}")
        return attrs[key]

    def __len__(self) -> int:
        return len(self._nodes)

    def num_edges(self) -> int:
        return len(self._edges)

    def __str__(self) -> str:
        num_nodes = len(self)
        return f"Graph '{self.name}' with {num_nodes} node{'s' if num_nodes != 1 else ''} and {self.num_edges()} edge{'s' if self.num_edges() != 1 else ''}"

    def __iter__(self) -> Iterator:
        return iter(self.get_nodes())

    def __contains__(self, node: Hashable) -> bool:
        return node in self._nodes

    def __getitem__(self, node: Hashable) -> Iterable[Hashable]:
        # KeyError desired if node not in self._incident_edges
        neighbors = []
        for u, v in self._incident_edges[node]:
            neighbors.append(v if u == node else u)
        return neighbors

    def get_nodes(self) -> Collection[Hashable]:
        return self._nodes

    def get_edges(self, node: Hashable = None) -> Collection[tuple[Hashable, Hashable]]:
        """If node is not None, gets all edges incident on node; otherwise, gets all edges in graph.

        Since nodes are not allowed to be None, None is used to request for all edges in the graph.
        """
        if node is None:
            return self._edges
        return self._incident_edges[node]

    def is_edge(self, edge: tuple[Hashable, Hashable]) -> bool:
        """Returns True if edge= is an edge in this graph; False otherwise"""
        u, v = edge
        if u not in self._nodes:
            raise ValueError(f"Unknown node {u=}")
        if v not in self._nodes:
            raise ValueError(f"Unknown node {v=}")
        return (u, v) in self._edges or (v, u) in self._edges

    def are_edges(self, edges: Iterable[tuple[Hashable, Hashable]]) -> bool:
        """Returns True if all edges are in the graph; False otherwise"""
        return all(self.is_edge((u, v)) for u, v in edges)

    def get_weight(self, edge: tuple[Hashable, Hashable]) -> None:
        if not self.is_edge(edge):
            raise ValueError(f"Unknown edge {edge=}")
        u, v = edge
        if (v, u) in self._edges:
            u, v = v, u
        return self._edges[(u, v)][0]

    def add_node(self, node: Hashable, attributes: Mapping | None = None) -> None:
        """Adds node if not present and not None; errors if already present"""
        if node is None:
            raise ValueError("None is not a valid node.")
        if node in self._nodes:
            raise ValueError(f"Node {node=} already present in graph")
        self._nodes[node] = attributes
        self._incident_edges[node] = set()

    def add_nodes(self, nodes: Iterable[Hashable]) -> None:
        for node in nodes:
            self.add_node(node)

    def add_edge(
        self, edge: tuple[Hashable, Hashable], attributes: Mapping | None = None
    ) -> None:
        """Adds edge if not present; errors if also present"""
        u, v = edge
        if u not in self._nodes:
            raise ValueError(f"Unknown node {u=}")
        if v not in self._nodes:
            raise ValueError(f"Unknown node {v=}")
        if self.is_edge(edge):
            raise ValueError(f"Edge ({u}, {v}) already exists.")
        self._edges[edge] = (Graph.DEFAULT_EDGE_WEIGHT, attributes)
        self._incident_edges[u].add(edge)
        self._incident_edges[v].add(edge)

    def add_edges(self, edges: Iterable[tuple[Hashable, Hashable]]) -> None:
        for edge in edges:
            self.add_edge(edge)

    def set_weight(self, edge: tuple[Hashable, Hashable], weight: float) -> None:
        if not math.isfinite(weight):
            raise ValueError(f"Invalid {weight=}")
        if not self.is_edge(edge):
            raise ValueError(f"Unknown edge {edge=}")
        u, v = edge
        if (v, u) in self._edges:
            u, v = v, u
        # can't update tuple, need to reassign
        _, attrs = self._edges[(u, v)]
        self._edges[(u, v)] = (weight, attrs)
