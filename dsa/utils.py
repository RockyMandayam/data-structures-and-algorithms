from collections.abc import Sequence
from typing import Any


# TODO: test this
def get_key_to_index(seq: Sequence[Any]) -> dict[Any, int]:
    # NOTE: clobbers duplicates with latest value
    key_to_index = {}
    for index, key in enumerate(seq):
        key_to_index[key] = index
    return key_to_index
