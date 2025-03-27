import pytest

from dsa.disjoint_sets.disjoint_sets import DisjointSets


class TestDisjointSets:
    def test_init(self) -> None:
        DisjointSets([])
        DisjointSets([1, 2, "hello world", (True, 0.0)])
        with pytest.raises(ValueError):
            DisjointSets([None])
        with pytest.raises(ValueError):
            DisjointSets([1, 1])  # duplicates

    def test_connect_and_is_connected(self) -> None:
        ds = DisjointSets(range(5))
        for i in range(5):
            for j in range(5):
                if i == j:
                    # call twice to make sure calling the same exact is_connected repeatedly doesn't cause issues
                    assert ds.is_connected(i, j)
                    assert ds.is_connected(i, j)
                else:
                    assert not ds.is_connected(i, j)
                    assert not ds.is_connected(i, j)

        ds.connect(0, 4)
        for _ in range(2):
            # run these twice to make sure calling the same is_connected sequence repeatedly doesn't cause issues
            assert ds.is_connected(0, 4)
            assert ds.is_connected(4, 0)
            assert not ds.is_connected(0, 1)
            assert not ds.is_connected(0, 2)
            assert not ds.is_connected(0, 3)
            assert not ds.is_connected(4, 1)
            assert not ds.is_connected(4, 2)
            assert not ds.is_connected(4, 3)

        # make sure calling the same exact connect repeatedly doesn't cause issues
        ds.connect(2, 1)
        ds.connect(2, 1)
        assert ds.is_connected(2, 1)
        assert ds.is_connected(4, 0)
        assert ds.is_connected(3, 3)
        assert not ds.is_connected(1, 3)
        assert not ds.is_connected(3, 1)

        # make sure calling the same connect with order switched repeatedly doesn't cause issues
        ds.connect(3, 1)
        ds.connect(1, 3)
        assert ds.is_connected(0, 4)
        assert ds.is_connected(2, 1)
        assert ds.is_connected(3, 1)
        assert not ds.is_connected(3, 4)

        # connect them all
        ds.connect(3, 4)
        for i in range(5):
            for j in range(5):
                assert ds.is_connected(j, i)
