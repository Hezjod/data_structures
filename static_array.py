from typing import Iterator


class StaticArray:
    def __init__(self, item_type: type, size: int) -> None:
        if not isinstance(item_type, type):
            raise ValueError("item_type must be a class")

        self._item_type = item_type
        self._size = size
        self._list = [None] * size

    def __getitem__(self, key: int | slice):
        if isinstance(key, slice):
           return self._list[key]

        if isinstance(key, int):
            if key not in range(0, self._size):
                raise IndexError("StaticArray index out of range")
            return self._list[key]

        raise TypeError(f"list indices must be integers or slices, not {type(key)}")

    def __setitem__(self, key: int, item) -> None:
        if isinstance(key, slice):
            raise NotImplementedError

        if not isinstance(item, self._item_type):
            raise TypeError(
                f"Invalid type ({type(item)}) for {self._item_type} StaticArray"
            )

        if key not in range(0, self._size):
            raise IndexError("StaticArray index out of range")

        self._list[key] = item

    def __repr__(self) -> str:
        return self._list.__repr__()

    def __str__(self) -> str:
        return self._list.__str__()

    def __iter__(self) -> Iterator:
        return iter(self._list)


