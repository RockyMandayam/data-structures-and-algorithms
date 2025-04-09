from dsa.graphs.digraph import Digraph
from dsa.graphs.transformations.transformations import reverse


def test_reverse() -> None:
    dg = Digraph(nodes=3, edges=((0, 1), (2, 1)))
    dg_reversed = reverse(dg)
    assert len(dg_reversed) == 3
    assert all(i in dg_reversed for i in range(3))
    assert dg_reversed.num_edges() == 2
    assert set(dg_reversed[0]) == set()
    assert set(dg_reversed[1]) == set([0, 2])
    assert set(dg_reversed[2]) == set()
    assert dg_reversed.is_edge((1, 0))
    assert dg_reversed.is_edge((1, 2))
    assert not dg_reversed.is_edge((0, 1))
    assert not dg_reversed.is_edge((2, 1))
    assert dg_reversed.get_degree(0) == 1
    assert dg_reversed.get_degree(1) == 2
    assert dg_reversed.get_degree(2) == 1
    assert dg_reversed.get_in_degree(0) == 1
    assert dg_reversed.get_in_degree(1) == 0
    assert dg_reversed.get_in_degree(2) == 1
    assert dg_reversed.get_out_degree(0) == 0
    assert dg_reversed.get_out_degree(1) == 2
    assert dg_reversed.get_out_degree(2) == 0
