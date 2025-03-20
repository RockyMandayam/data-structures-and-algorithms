from collections.abc import Hashable, Sequence

from graphs.analysis.traversal.order import Order
from graphs.graph import Graph


def get_ordered_seed_nodes(
    g: Graph, seed_order: Order | Hashable | Sequence[Hashable] | None
) -> list[Hashable]:
    if isinstance(seed_order, Sequence) and (
        len(seed_order) != len(g) or set(seed_order) != set(g.get_nodes())
    ):
        raise ValueError(
            f"When providing seed_order as sequence, it must include every node in g exactly once. Received {seed_order=}. Expected {g.get_nodes()=}"
        )
    seed_nodes = list(g.get_nodes())
    if seed_order is None:
        return seed_nodes
    if isinstance(seed_order, Order):
        seed_nodes.sort(reverse=(seed_order == Order.REVERSE_SORTED))
    elif isinstance(seed_order, Hashable):
        seed_nodes = [
            seed_order,
            *[node for node in g.get_nodes() if node != seed_order],
        ]
    elif isinstance(seed_order, Sequence):
        if len(seed_order) != len(g) or set(seed_order) != set(g.get_nodes()):
            raise ValueError(
                f"When providing seed_order as sequence, it must include every node in g exactly once. Received {seed_order=}. Expected {g.get_nodes()=}"
            )
        seed_nodes = seed_order
    return seed_nodes
