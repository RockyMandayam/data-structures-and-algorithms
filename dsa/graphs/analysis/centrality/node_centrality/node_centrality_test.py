import pytest

from dsa.graphs.analysis.centrality.node_centrality.node_centrality import (
    get_degree_centrality,
    get_eigvec_centralities,
    get_in_degree_centrality,
    get_out_degree_centrality,
)
from dsa.graphs.digraph import Digraph
from dsa.graphs.digraph_factory import DigraphFactory
from dsa.graphs.graph import Graph
from dsa.graphs.graph_factory import GraphFactory


def test_get_degree_centrality() -> None:
    g = Graph(nodes=4)
    for u in range(4):
        assert get_degree_centrality(g, u, normalized=False) == 0
        assert get_degree_centrality(g, u, normalized=True) == 0

    g = GraphFactory.create_spindly_tree(5)
    for u in (0, 4):
        assert get_degree_centrality(g, u, normalized=False) == 1
        assert get_degree_centrality(g, u, normalized=True) == pytest.approx(1 / 4)
    for u in (1, 2, 3):
        assert get_degree_centrality(g, u, normalized=False) == 2
        assert get_degree_centrality(g, u, normalized=True) == pytest.approx(2 / 4)

    g = GraphFactory.create_complete_graph(4)
    for u in range(4):
        assert get_degree_centrality(g, u, normalized=False) == 3
        assert get_degree_centrality(g, u, normalized=True) == pytest.approx(1)

    g = Graph(nodes=4, edges=((0, 1), (1, 2), (2, 3), (0, 2)))
    assert get_degree_centrality(g, 0, normalized=False) == 2
    assert get_degree_centrality(g, 0, normalized=True) == pytest.approx(2 / 3)
    assert get_degree_centrality(g, 1, normalized=False) == 2
    assert get_degree_centrality(g, 1, normalized=True) == pytest.approx(2 / 3)
    assert get_degree_centrality(g, 2, normalized=False) == 3
    assert get_degree_centrality(g, 2, normalized=True) == pytest.approx(3 / 3)
    assert get_degree_centrality(g, 3, normalized=False) == 1
    assert get_degree_centrality(g, 3, normalized=True) == pytest.approx(1 / 3)

    g = Graph(
        nodes=6, edges=((0, 1), (0, 2), (1, 3), (1, 5), (2, 5), (3, 4), (3, 5), (4, 5))
    )
    assert get_degree_centrality(g, 0, normalized=False) == 2
    assert get_degree_centrality(g, 0, normalized=True) == pytest.approx(2 / 5)
    assert get_degree_centrality(g, 1, normalized=False) == 3
    assert get_degree_centrality(g, 1, normalized=True) == pytest.approx(3 / 5)
    assert get_degree_centrality(g, 2, normalized=False) == 2
    assert get_degree_centrality(g, 2, normalized=True) == pytest.approx(2 / 5)
    assert get_degree_centrality(g, 3, normalized=False) == 3
    assert get_degree_centrality(g, 3, normalized=True) == pytest.approx(3 / 5)
    assert get_degree_centrality(g, 4, normalized=False) == 2
    assert get_degree_centrality(g, 4, normalized=True) == pytest.approx(2 / 5)
    assert get_degree_centrality(g, 5, normalized=False) == 4
    assert get_degree_centrality(g, 5, normalized=True) == pytest.approx(4 / 5)


def test_get_eigenvector_centralities() -> None:
    # examples from: https://www2.stat.duke.edu/~pdh10/Teaching/567/Notes/l6_centrality_paused.pdf
    # star graph
    g = Graph(nodes=5, edges=((0, 2), (1, 2), (2, 3), (2, 4)))
    centralities = get_eigvec_centralities(g, normalization="l2")
    assert centralities == pytest.approx(
        [0.3535534, 0.3535534, 0.7071068, 0.3535534, 0.3535534]
    )
    # Y graph
    g = Graph(nodes=5, edges=((0, 1), (1, 2), (2, 3), (2, 4)))
    centralities = get_eigvec_centralities(g, normalization="l2")
    assert centralities == pytest.approx(
        [0.2705981, 0.5, 0.6532815, 0.3535534, 0.3535534]
    )


def test_get_in_degree() -> None:
    dg = Digraph(nodes=4)
    for u in range(4):
        assert get_in_degree_centrality(dg, u, normalized=False) == 0
        assert get_in_degree_centrality(dg, u, normalized=True) == 0

    dg = DigraphFactory.create_spindly_tree(5)
    assert get_in_degree_centrality(dg, 0, normalized=False) == 0
    assert get_in_degree_centrality(dg, 0, normalized=True) == pytest.approx(0)
    for u in (1, 2, 3, 4):
        assert get_in_degree_centrality(dg, u, normalized=False) == 1
        assert get_in_degree_centrality(dg, u, normalized=True) == pytest.approx(1 / 4)

    dg = DigraphFactory.create_complete_digraph(4)
    for u in range(4):
        assert get_in_degree_centrality(dg, u, normalized=False) == 3
        assert get_in_degree_centrality(dg, u, normalized=True) == pytest.approx(1)


def test_get_out_degree() -> None:
    dg = Digraph(nodes=4)
    for u in range(4):
        assert get_out_degree_centrality(dg, u, normalized=False) == 0
        assert get_out_degree_centrality(dg, u, normalized=True) == 0

    dg = DigraphFactory.create_spindly_tree(5)
    for u in (0, 1, 2, 3):
        assert get_out_degree_centrality(dg, u, normalized=False) == 1
        assert get_out_degree_centrality(dg, u, normalized=True) == pytest.approx(1 / 4)
    assert get_out_degree_centrality(dg, 4, normalized=False) == 0
    assert get_out_degree_centrality(dg, 4, normalized=True) == pytest.approx(0)

    dg = DigraphFactory.create_complete_digraph(4)
    for u in range(4):
        assert get_out_degree_centrality(dg, u, normalized=False) == 3
        assert get_out_degree_centrality(dg, u, normalized=True) == pytest.approx(1)
