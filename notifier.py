
from abc import ABC, abstractmethod

"""
This module defines the abstract base class `Notifier` and its concrete 
implementation `ConsoleNotifier`.

Notifier:
    This abstract base class defines the interface for all notifiers. 
    It provides a single abstract method `notify`
    that should be implemented by subclasses.

ConsoleNotifier:
    This concrete implementation of `Notifier` provides a simple way to notify 
    messages by printing them to the console.
    It overrides the `notify` method to print the given message.

EmailNotifier:
    This is an example of a potential extension of the `Notifier` class.
    It could be implemented to send notifications
    via email. Additional methods and properties would need to be added to
      support the email functionality.

Usage:
    To use the `ConsoleNotifier`, create an instance of the class and call the
      `notify` method with a message to be printed.

Example:
    notifier = ConsoleNotifier()
    notifier.notify("Hello, world!")

"""


class Notifier(ABC):
    @abstractmethod
    def notify(self, message: str):
        pass


class ConsoleNotifier(Notifier):
    def notify(self, message: str):
        print(message)
