from __future__ import annotations
from typing import Iterator, TypeVar, Generic, Iterable

T = TypeVar("T")


class StaticArray(Generic[T]):
    def __init__(self, item_type: type[T], size: int) -> None:
        if size <= 0:
            raise ValueError("size has to be bigger than 0")

        if not isinstance(item_type, type):
            raise ValueError("item_type must be a class")

        self._item_type: type[T] = item_type
        self._size: int = size
        self._list: list[T | None] = [None] * size

    def __getitem__(self, key: int | slice) -> T | None | StaticArray[T | None]:
        if isinstance(key, slice):
            return StaticArray.from_iter(self._item_type, self._list[key])

        if isinstance(key, int):
            if key not in range(0, self._size):
                raise IndexError(f"{__class__.__name__} index out of range")
            return self._list[key]

        raise TypeError(
            f"{__class__.__name__} indices must be integers or slices, not {type(key).__name__}"
        )

    def __setitem__(self, key: int, item: T | None) -> None:
        if not isinstance(key, int):
            raise TypeError(f"StaticArray indices must be integers, not {type(key)}")

        if (not isinstance(item, self._item_type)) and (item is not None):
            raise TypeError(
                f"Invalid type ({type(item).__name__}) for {self._item_type.__name__} StaticArray"
            )

        if key not in range(0, self._size):
            raise IndexError(f"{__class__.__name__} index out of range")

        self._list[key] = item

    def __repr__(self) -> str:
        return self._list.__repr__()

    def __str__(self) -> str:
        return self._list.__str__()

    def __iter__(self) -> Iterator[T | None]:
        return iter(self._list)

    def index(self, item: T | None) -> int:
        if (not isinstance(item, self._item_type)) and (item is not None):
            raise TypeError(
                f"Invalid type ({type(item).__name__}) for {self._item_type.__name__} {__class__.__name__}"
            )
        return self._list.index(item)

    def clear(self) -> None:
        self._list = [None] * self._size

    @staticmethod
    def from_iter(item_type: type[T], arr: Iterable[T | None]) -> StaticArray[T | None]:
        items: list[T | None] = list(iter(arr))
        if len(items) == 0:
            raise ValueError(
                f"can't create {__class__.__name__} from an empty iterable"
            )

        new_static_array: StaticArray[T | None] = StaticArray(item_type, len(items))
        for index, item in enumerate(items):
            if (not isinstance(item, item_type)) and (item is not None):
                raise TypeError(
                    f"Invalid type ({type(item)}) for {item_type} {__class__.__name__}"
                )
            new_static_array[index] = item

        return new_static_array
