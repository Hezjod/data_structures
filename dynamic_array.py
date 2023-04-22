from __future__ import annotations
from typing import Generic, TypeVar, Iterator

from static_array import StaticArray
from data_loss_warning import DataLossWarning

T = TypeVar("T")


class DynamicArray(Generic[T]):
    def __init__(self, item_type: type[T], *, initial_capacity: int = 4) -> None:
        if not isinstance(item_type, type):
            raise ValueError("item_type must be a class")

        if initial_capacity < 0:
            raise ValueError("capacity can't be negative")

        self._length: int = 0
        self._item_type: type[T] = item_type
        self._capacity: int = initial_capacity
        self._array: StaticArray[T] = StaticArray(self._item_type, self._capacity)

    def _resize(self, new_capacity: int, *, ignore_warnings=False) -> None:
        if new_capacity < 0:
            raise ValueError("capacity can't be negative")

        if new_capacity == self._capacity:
            return

        if (not ignore_warnings) and new_capacity < self._length:
            raise DataLossWarning("you might loss some data due to this operation")

        new_array: StaticArray[T] = StaticArray(self._item_type, new_capacity)
        for index in range(min(new_capacity, self._capacity)):
            new_array[index] = self._array[index]

        self._array = new_array
        self._capacity = new_capacity
        self._length = min(self._length, new_capacity)

    def append(self, item: T) -> None:
        if not isinstance(item, self._item_type):
            raise TypeError(
                f"invalid type ({type(item)}) for {self._item_type} StaticArray"
            )

        if self._length == self._capacity:
            self._resize(self._capacity * 2)

        self._array[self._length] = item
        self._length += 1

    def pop(self, index: int = -1) -> T:
        if not isinstance(index, int):
            raise TypeError(f"index must be of type int, not {type(index)}")

        if index < 0:
            index = self._length + index

        if index >= self._length:
            raise IndexError("DynamicArray index out of range")

        removed = self._array[index]

        for i in range(index, self._length - 1):
            self._array[i] = self._array[i + 1]

        self._length -= 1

        self._array[self._length] = None

        return removed  # type: ignore # returning None is impossible here

    def __getitem__(self, key: int | slice) -> T | DynamicArray[T]:
        if isinstance(key, slice):
            raise NotImplementedError
            return self._list[key]

        if isinstance(key, int):
            if key not in range(0, self._length):
                raise IndexError(f"{__class__.__name__} index out of range")
            return self._array[key]  # type: ignore # returning None is impossible here

        raise TypeError(
            f"{__class__.__name__} indices must be integers or slices, not {type(key)}"
        )

    def __setitem__(self, key: int, item) -> None:
        if isinstance(key, slice):
            raise NotImplementedError

        if (not isinstance(item, self._item_type)) and (item is not None):
            raise TypeError(
                f"invalid type ({type(item)}) for {self._item_type} StaticArray"
            )

        if key not in range(0, self._length):
            raise IndexError(f"{__class__.__name__} index out of range")

        self._array[key] = item

    def __str__(self) -> str:
        return self._array[: self._length].__str__()

    def __repr__(self) -> str:
        return self._array[: self._length].__repr__()

    def __len__(self) -> int:
        return self._length

    def index(self, item: T) -> int:
        if not isinstance(item, self._item_type):
            raise TypeError(
                f"Invalid type ({type(item)}) for {self._item_type} StaticArray"
            )
        return self._array.index(item)

    def __iter__(self) -> Iterator[T]:
        return iter(self._array[: self._length])  # type: ignore # returning None is impossible here
