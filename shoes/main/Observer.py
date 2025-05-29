from __future__ import annotations

from django.contrib.auth.models import User
from django.core.mail import send_mail

from abc import ABC, abstractmethod
from random import randrange
from typing import List

from django.db import transaction
class ObserverManager:
    _instance = None

    def __init__(self):

        self.subject = ConcreteSubject()

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = ObserverManager()
        return cls._instance
def create_email(observer, product):
    message = f"{observer.user.username}, {product.sh_name} з'явився в наявності!"
    subject_of_mail = f"Продукт знову в наявності!"
    sender = "martamykhailyna608@gmail.com"
    send_mail(subject_of_mail, message, sender, [observer.user.email])

class Subject(ABC):

    @abstractmethod
    def attach(self, observer: Observer) -> List:
        """
        Attach an observer to the subject.
        """
        pass

    @abstractmethod
    def detach(self, observer: Observer) -> List:
        """
        Detach an observer from the subject.
        """
        pass

    @abstractmethod
    def notify(self, product) -> None:
        """
        Notify all observers about an event.
        """
        pass


class ConcreteSubject(Subject):
    """
    The Subject owns some important state and notifies observers when the state
    changes.
    """

    _state: int = 0
    last_state: int = 0

    _observers: List[Observer] = []

    def attach(self, observer: Observer) -> None:
        print("Subject: Attached an observer.")
        self._observers.append(observer)
        self.last_state = self._state


    def detach(self, observer: Observer) -> None:
        self._observers.remove(observer)


    def notify(self, product) -> None:
        print(f"Subject: 1My state has just changed to: {self._state}")
        print(f"Subject: My last state has just changed to: {self.last_state}")
        print("Subject: Notifying observers...")

        for observer in self._observers:
            if observer:
                print(f'{observer}')
                observer.update(self, product)
            else: print('no observers')
            print(f"Subject: 2My last state has just changed to: {self.last_state}")
        print(f"Subject: My state has just changed to: {self._state}")
        self.last_state = self._state



class Observer(ABC):
    """
    The Observer interface declares the update method, used by subjects.
    """
    @abstractmethod
    def __init__(self, user):
        self.user = user
    @abstractmethod
    def update(self, subject: Subject, product) -> None:
        """
        Receive update from subject.
        """
        pass


"""
Concrete Observers react to the updates issued by the Subject they had been
attached to.
"""

class ConcreteObserver(Observer):
    def __init__(self, user):
        self.user = user

    def update(self, subject: Subject, product) -> None:
        if subject.last_state and subject._state > 0:
            print(f"Subject: 3My last state has just changed to: {subject.last_state}")
            print(f"Subject: My state has just changed to: {subject._state}")
            print("\nSubject: I'm doing something important.")
            create_email(self, product)
            print("ConcreteObserverA: Reacted to the event")
        else:
            print(f"NO EMAIL: last_state = {subject.last_state}, state = {subject._state}")
