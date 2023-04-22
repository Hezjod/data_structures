from __future__ import annotations
from typing import Iterator, TypeVar, Generic, Iterable, TYPE_CHECKING, overload

if TYPE_CHECKING:
    __class__: type

T = TypeVar("T")


class StaticArray(Generic[T]):
    def __init__(self, item_type: type[T], length: int) -> None:
        if length < 0:
            raise ValueError("length has to be bigger or equal to 0")

        if not isinstance(item_type, type):
            raise ValueError("item_type must be a class")

        self._item_type: type[T] = item_type
        self._length: int = length
        self._array: list[T | None] = [None] * length

    @overload
    def __getitem__(self, key: int) -> T | None:
        ...

    @overload
    def __getitem__(self, key: slice) -> StaticArray[T | None]:
        ...

    def __getitem__(self, key: int | slice) -> T | None | StaticArray[T | None]:
        if isinstance(key, slice):
            return StaticArray.from_iter(self._item_type, self._array[key])

        if isinstance(key, int):
            if key not in range(0, self._length):
                raise IndexError(f"{__class__.__name__} index out of range")
            return self._array[key]

        raise TypeError(
            f"{__class__.__name__} indices must be integers or slices, not {type(key).__name__}"
        )

    def __setitem__(self, key: int, item: T | None) -> None:
        if not isinstance(key, int):
            raise TypeError(
                f"{__class__.__name__} indices must be integers, not {type(key)}"
            )

        if (not isinstance(item, self._item_type)) and (item is not None):
            raise TypeError(
                f"Invalid type ({type(item).__name__}) for {self._item_type.__name__} {__class__.__name__}"
            )

        if key not in range(0, self._length):
            raise IndexError(f"{__class__.__name__} index out of range")

        self._array[key] = item

    def __delitem__(self, key: int | slice) -> None:
        if not isinstance(key, int):
            raise TypeError(
                f"{__class__.__name__} indices must be integers, not {type(key)}"
            )

        self._array[key] = None

    def __repr__(self) -> str:
        return self._array.__repr__()

    def __str__(self) -> str:
        return self._array.__str__()

    def __iter__(self) -> Iterator[T | None]:
        return iter(self._array)

    def index(self, item: T | None) -> int:
        if (not isinstance(item, self._item_type)) and (item is not None):
            raise TypeError(
                f"invalid type ({type(item).__name__}) for {self._item_type.__name__} {__class__.__name__}"
            )
        return self._array.index(item)

    def clear(self) -> None:
        self._array = [None] * self._length

    @staticmethod
    def from_iter(item_type: type[T], arr: Iterable[T | None]) -> StaticArray[T | None]:
        items: list[T | None] = list(iter(arr))

        new_static_array: StaticArray[T | None] = StaticArray(item_type, len(items))
        for index, item in enumerate(items):
            if (not isinstance(item, item_type)) and (item is not None):
                raise TypeError(
                    f"Invalid type ({type(item)}) for {item_type} {__class__.__name__}"
                )
            new_static_array[index] = item

        return new_static_array

    def __len__(self) -> int:
        return self._length
