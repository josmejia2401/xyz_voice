from __future__ import annotations
from abc import ABC, abstractmethod
from random import randrange
from typing import List


class Subject(ABC):
    @abstractmethod
    def attach(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def detach(self, observer: Observer) -> None:
        pass

    @abstractmethod
    def notify(self, payload) -> None:
        pass


class ConcreteSubject(Subject):
    _state: int = None
    _observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        self._observers.append(observer)

    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)

    def notify(self, payload) -> None:
        for observer in self._observers:
            observer.update(self, payload)

    def some_business_logic(self, payload) -> None:
        self._state = randrange(0, 10)
        self.notify(payload)

class Observer(ABC):
    @abstractmethod
    def update(self, subject: Subject, payload) -> None:
        pass