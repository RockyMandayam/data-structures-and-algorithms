from collections.abc import Hashable, Iterable


class DisjointSets:
    """Weighted Quick Union implementation of Disjoint Sets abstract data type.

    Elements of sets must be Hashable and non-None. Each disjoint set is stored as a rooted tree.

    Attributes:
        parents (dict[Hashable, Hashable]): Map from element to its parent. If an element is the root, its parent will be None
        sizes (dict[Hashable, int]): Map from each root element to the size of that disjoint set tree
    """

    def __init__(self, elements: Iterable[Hashable]) -> None:
        self.parents = {element: None for element in elements}
        if None in self.parents:
            raise ValueError(f"None is not a valid element.")
        if len(self.parents) != len(elements):
            raise ValueError(f"Duplicate elements passed in; this is not allowed.")
        self.sizes = {element: 1 for element in self.parents}

    def __len__(self) -> int:
        return len(self.parents)

    def _validate_element(self, e: Hashable) -> None:
        if e is None:
            raise ValueError(f"None is not a valid element.")
        if e not in self.parents:
            raise ValueError(f"Unrecognized element {e=}")

    def _find_root(self, e: Hashable) -> Hashable:
        self._validate_element(e)

        # find root
        root = e
        while self.parents[root] is not None:
            root = self.parents[root]

        # path compression
        while self.parents[e] is not None:
            parent = self.parents[e]
            self.parents[e] = root
            e = parent

        return root

    def connect(self, e1: Hashable, e2: Hashable) -> None:
        # not calling is_connected to avoid duplicate work of finding roots
        self._validate_element(e1)
        self._validate_element(e2)
        root1 = self._find_root(e1)
        root2 = self._find_root(e2)
        if root1 == root2:
            return  # already connected
        size1 = self.sizes[root1]
        size2 = self.sizes[root2]
        # arbitrarily let tree 1 be the larger tree
        if self.sizes[root2] > self.sizes[root1]:
            root1, size1, root2, size2 = root2, size2, root1, size1
        self.parents[root2] = root1
        self.sizes[root1] = self.sizes[root1] + self.sizes[root2]
        del self.sizes[root2]

    def is_connected(self, e1: Hashable, e2: Hashable) -> bool:
        self._validate_element(e1)
        self._validate_element(e2)
        root1 = self._find_root(e1)
        root2 = self._find_root(e2)
        return root1 == root2
