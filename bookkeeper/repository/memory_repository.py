"""
Модуль описывает репозиторий, работающий в оперативной памяти
"""

from itertools import count
from typing import Any, Callable

from bookkeeper.repository.abstract_repository import AbstractRepository, T


class MemoryRepository(AbstractRepository[T]):
    """
    Репозиторий, работающий в оперативной памяти. Хранит данные в словаре.
    """

    def __init__(self) -> None:
        self._container: dict[int, T] = {}
        self._counter = count(1)

    def add(self, obj: T) -> int:
        if getattr(obj, 'prim_key', None) != 0:
            raise ValueError(f'trying to add object {obj} with filled `pk` attribute')
        prim_key = next(self._counter)
        self._container[prim_key] = obj
        obj.prim_key = prim_key
        return prim_key

    def get(self, prim_key: int) -> T | None:
        return self._container.get(prim_key)

    def get_all(self, where: Callable[[Any], bool] = lambda x: True) -> list[T]:
        return [obj for obj in self._container.values() if where(obj)]

    def update(self, obj: T) -> None:
        if obj.prim_key == 0:
            raise ValueError('attempt to update object with unknown primary key')
        self._container[obj.prim_key] = obj

    def delete(self, prim_key: int) -> None:
        self._container.pop(prim_key)
