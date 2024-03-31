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
        if getattr(obj, 'pk', None) != 0:
            raise ValueError(f'trying to add object {obj} with filled `pk` attribute')
        pk = next(self._counter)
        self._container[pk] = obj
        obj.pk = pk
        return pk

    def get(self, pk: int) -> T | None:
        return self._container.get(pk)

    def get_all(self, where: Callable[[Any], bool] = lambda x: True) -> list[T]:
        return [obj for obj in self._container.values() if where(obj)]

    def update(self, obj: T) -> None:
        if obj.pk == 0:
            raise ValueError('attempt to update object with unknown primary key')
        self._container[obj.pk] = obj

    def delete(self, pk: int) -> None:
        self._container.pop(pk)
