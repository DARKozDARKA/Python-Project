# Defines a component that stores an actor position.
from game.components.component import Component
from game.vector import Vector


class TransformComponent(Component):
    """Stores the actor position."""

    def __init__(self, actor, x, y):
        """Creates a transform component.

        Args:
            actor: Owning actor.
            x: Initial x value.
            y: Initial y value.
        """
        super().__init__(actor)
        self.position = Vector(x, y)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, value):
        if not isinstance(value, Vector):
            raise TypeError("position must be a Vector.")

        self._position = value
