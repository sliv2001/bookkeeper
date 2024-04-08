"""
Модуль содержит описание абстрактного репозитория

Репозиторий реализует хранение объектов, присваивая каждому объекту уникальный
идентификатор в атрибуте prim_key (primary key). Объекты, которые могут быть сохранены
в репозитории, должны поддерживать добавление атрибута prim_key и не должны
использовать его для иных целей.
"""

from abc import ABC, abstractmethod
from typing import Generic, TypeVar, Protocol, Any, Callable


class Model(Protocol):  # pylint: disable=too-few-public-methods
    """
    Модель должна содержать атрибут prim_key
    """
    prim_key: int


T = TypeVar('T', bound=Model)


class AbstractRepository(ABC, Generic[T]):
    """
    Абстрактный репозиторий.
    Абстрактные методы:
    add
    get
    get_all
    update
    delete
    """

    @abstractmethod
    def add(self, obj: T) -> int:
        """
        Добавить объект в репозиторий, вернуть id объекта,
        также записать id в атрибут prim_key.
        """

    @abstractmethod
    def get(self, prim_key: int) -> T | None:
        """ Получить объект по id """

    @abstractmethod
    def get_all(self, where: Callable[[Any], bool] = lambda x: True) -> Any:
        """
        Получить все записи по некоторому условию
        where - условие в виде словаря {'название_поля': значение}
        если условие не задано (по умолчанию), вернуть все записи
        """

    @abstractmethod
    def update(self, obj: T) -> None:
        """ Обновить данные об объекте. Объект должен содержать поле prim_key. """

    @abstractmethod
    def delete(self, prim_key: int) -> None:
        """ Удалить запись """

# TODO describe why separate repos
