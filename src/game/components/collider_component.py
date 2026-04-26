# Defines a simple box collider component for actors.
from game.components.component import Component
from infrastructure.validation import ensure_positive_number


class ColliderComponent(Component):
    """Represents a box collider."""

    def __init__(self, actor, size):
        """Creates a collider component.

        Args:
            actor: Owning actor.
            size: Collider size.
        """
        super().__init__(actor)
        self.size = size

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = ensure_positive_number(value, "size")
