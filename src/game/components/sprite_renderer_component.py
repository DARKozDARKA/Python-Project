# Defines a component that draws a simple shape for an actor.
import pygame

from game.components.component import Component
from game.components.transform_component import TransformComponent
from infrastructure.validation import ensure_color
from infrastructure.validation import ensure_positive_number
from infrastructure.validation import ensure_string


class SpriteRendererComponent(Component):
    """Draws a simple shape for an actor."""

    def __init__(self, actor, color, shape, size):
        """Creates a sprite renderer component.

        Args:
            actor: Owning actor.
            color: RGB color.
            shape: Shape name.
            size: Shape size.
        """
        super().__init__(actor)
        self.color = color
        self.shape = shape
        self.size = size

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = ensure_color(value, "color")

    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, value):
        value = ensure_string(value, "shape")
        if value not in ["box", "circle"]:
            raise ValueError("shape must be 'box' or 'circle'.")

        self._shape = value

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = ensure_positive_number(value, "size")

    def render(self, screen):
        """Draws the shape on the screen.

        Args:
            screen: Pygame surface to draw on.
        """
        transform = self.actor.get_component_of_type(TransformComponent)
        if transform is None:
            return

        position = transform.position

        if self.shape == "box":
            pygame.draw.rect(
                screen,
                self.color,
                pygame.Rect(
                    int(position.x - self.size / 2),
                    int(position.y - self.size / 2),
                    self.size,
                    self.size,
                ),
            )
            return

        pygame.draw.circle(
            screen,
            self.color,
            (int(position.x), int(position.y)),
            self.size,
        )
