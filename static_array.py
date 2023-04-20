class StaticArray:
    def __init__(self, item_type: type, size: int) -> None:
        self._item_type = item_type
        self._size = size
        self._list = [None] * size
    
    def __getitem__(self, index: int):
        if index not in range(0, self._size):
            raise IndexError("StaticArray index out of range")
        return self._list[index]


    def __setitem__(self, index: int, item) -> None:
        if not isinstance(item, self._item_type):
            raise TypeError(f"Invalid type ({type(item)}) for {self._item_type} StaticArray")
        if index not in range(0, self._size):
            raise IndexError("StaticArray index out of range")
        self._list[index] = item
    
    def __repr__(self) -> str:
        return self._list.__repr__()
    
    def __str__(self) -> str:
        return self._list.__str__()



