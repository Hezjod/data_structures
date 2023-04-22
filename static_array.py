from __future__ import annotations
from typing import Iterator, TypeVar, Generic, Iterable, Type

T = TypeVar("T", bound=type)


class StaticArray(Generic[T]):
    def __init__(self, item_type: T, size: int) -> None:
        if size <= 0:
            raise ValueError("size has to be bigger than 0")

        if not isinstance(item_type, type):
            raise ValueError("item_type must be a class")

        self._item_type: T = item_type
        self._size: int = size
        self._list: list[T | None] = [None] * size

    def __getitem__(self, key: int | slice) -> T | None | StaticArray[T]:
        if isinstance(key, slice):
            return StaticArray.from_iter(self._item_type, self._list[key])

        if isinstance(key, int):
            if key not in range(0, self._size):
                raise IndexError(f"{type(self).__name__} index out of range")
            return self._list[key]

        raise TypeError(
            f"StaticArray indices must be integers or slices, not {type(key).__name__}"
        )

    def __setitem__(self, key: int, item) -> None:
        if isinstance(key, slice):
            raise TypeError("you can't change StaticArray with a slice")

        if (not isinstance(item, self._item_type)) and (item is not None):
            raise TypeError(
                f"Invalid type ({type(item).__name__}) for {self._item_type.__name__} StaticArray"
            )

        if key not in range(0, self._size):
            raise IndexError(f"{type(self).__name__} index out of range")

        self._list[key] = item

    def __repr__(self) -> str:
        return self._list.__repr__()

    def __str__(self) -> str:
        return self._list.__str__()

    def __iter__(self) -> Iterator[T | None]:
        return iter(self._list)

    def index(self, item) -> int:
        if not isinstance(item, self._item_type):
            raise TypeError(
                f"Invalid type ({type(item).__name__}) for {self._item_type.__name__} StaticArray"
            )
        return self._list.index(item)

    def clear(self) -> None:
        self._list = [None] * self._size

    @staticmethod
    def from_iter(item_type: T, arr: Iterable[T | None]) -> StaticArray[T]:
        items = list(iter(arr))
        if len(items) == 0:
            raise ValueError("can't create StaticArray from empty iterable")

        new_static_array = StaticArray(item_type, len(items))
        for index, item in enumerate(items):
            if (not isinstance(item, item_type)) and (item is not None):
                raise TypeError(
                    f"Invalid type ({type(item)}) for {item_type} StaticArray"
                )
            new_static_array[index] = item

        return new_static_array
