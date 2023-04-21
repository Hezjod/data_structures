from static_array import StaticArray
from data_loss_warning import DataLossWarning


class DynamicArray:
    def __init__(self, item_type: type, *, initial_capacity: int = 4) -> None:
        if not isinstance(item_type, type):
            raise ValueError("item_type must be a class")

        if initial_capacity < 0:
            raise ValueError("Capacity can't be negative")

        self._size = 0
        self._item_type = item_type
        self._capacity = initial_capacity
        self._array = StaticArray(self._item_type, self._capacity)

    def _resize(self, new_capacity: int, *, ignore_warnings=False) -> None:
        if new_capacity < 0:
            raise ValueError("Capacity can't be negative")

        if new_capacity == self._capacity:
            return None

        if (not ignore_warnings) and new_capacity < self._size:
            raise DataLossWarning("You might loss some data due to this operation")

        new_array = StaticArray(self._item_type, new_capacity)
        for index in range(min(new_capacity, self._capacity)):
            new_array[index] = self._array[index]

        self._array = new_array
        self._capacity = new_capacity
        self._size = min(self._size, new_capacity)

    def append(self, item) -> None:
        if (not isinstance(item, self._item_type)) and (item is not None):
            raise TypeError(
                f"Invalid type ({type(item)}) for {self._item_type} StaticArray"
            )

        if self._size == self._capacity:
            self._resize(self._capacity * 2)

        self._array[self._size] = item
        self._size += 1

    def pop(self, index: int = -1):
        if not isinstance(index, int):
            raise TypeError(f"index must be of type int, not {type(index)}")

        if index < 0:
            index = self._size + index

        if index >= self._size:
            raise IndexError("DynamicArray index out of range")

        for i in range(index, self._size - 1):
            self._array[i] = self._array[i + 1]

        self._size -= 1

        self._array[self._size] = None

    def __getitem__(self, key: int | slice):
        if isinstance(key, slice):
            return self._list[key]

        if isinstance(key, int):
            if key not in range(0, self._size):
                raise IndexError("DynamicArray index out of range")
            return self._list[key]

        raise TypeError(
            f"DynamicArray indices must be integers or slices, not {type(key)}"
        )

    def __setitem__(self, key: int, item) -> None:
        if isinstance(key, slice):
            raise NotImplementedError

        if (not isinstance(item, self._item_type)) and (item is not None):
            raise TypeError(
                f"Invalid type ({type(item)}) for {self._item_type} StaticArray"
            )

        if key not in range(0, self._size):
            raise IndexError("StaticArray index out of range")

        self._list[key] = item

    def __str__(self) -> str:
        return self._array[: self._size].__str__()

    def __repr__(self) -> str:
        return self._array[: self._size].__repr__()

    def __len__(self) -> int:
        return self._size

    def index(self, item) -> int:
        if not isinstance(item, self._item_type):
            raise TypeError(
                f"Invalid type ({type(item)}) for {self._item_type} StaticArray"
            )
        return self._array.index(item)