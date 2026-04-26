# Stores tickable objects and updates them every frame.
from infrastructure.service import Service
from infrastructure.tick.tickable import Tickable


class TickableService(Service):
    """Stores and updates tickable objects."""

    def __init__(self):
        """Creates the tickable service."""
        self._tickables = []

    def register(self, tickable):
        """Registers a tickable object.

        Args:
            tickable: Tickable object to register.
        """
        if not isinstance(tickable, Tickable):
            raise TypeError("Only Tickable objects can be registered.")
        self._tickables.append(tickable)

    def unregister(self, tickable):
        """Unregisters a tickable object.

        Args:
            tickable: Tickable object to unregister.
        """
        if tickable in self._tickables:
            self._tickables.remove(tickable)

    def tick(self, delta_time):
        """Ticks every registered object.

        Args:
            delta_time: Time passed since the previous frame.
        """
        for tickable in self._tickables[:]:
            tickable.tick(delta_time)
