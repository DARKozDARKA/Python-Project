# Defines a component that moves an actor in a fixed direction.
from game.components.component import Component
from game.components.transform_component import TransformComponent
from game.vector import Vector
from infrastructure.validation import ensure_positive_number
from infrastructure.tick.tickable import Tickable


class MoveComponent(Component, Tickable):
    """Moves an actor in a fixed direction."""

    def __init__(self, actor, direction_x, direction_y, speed):
        """Creates a move component.

        Args:
            actor: Owning actor.
            direction_x: Horizontal direction.
            direction_y: Vertical direction.
            speed: Movement speed.
        """
        super().__init__(actor)
        self.direction = Vector(direction_x, direction_y)
        self.speed = speed

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        if not isinstance(value, Vector):
            raise TypeError("direction must be a Vector.")

        self._direction = value

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        self._speed = ensure_positive_number(value, "speed")

    def tick(self, delta_time):
        """Updates the actor position.

        Args:
            delta_time: Time passed since the previous frame.
        """
        transform = self.actor.get_component_of_type(TransformComponent)
        if transform is None:
            return

        movement = self.direction * self.speed * delta_time
        transform.position = transform.position + movement
