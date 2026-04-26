# Defines a component that moves an actor to the mouse position.
import pygame

from game.components.component import Component
from game.components.transform_component import TransformComponent
from game.vector import Vector
from infrastructure.tick.tickable import Tickable


class MouseFollowComponent(Component, Tickable):
    """Moves an actor to the mouse position."""

    def __init__(self, actor):
        """Creates a mouse follow component.

        Args:
            actor: Owning actor.
        """
        super().__init__(actor)

    def tick(self, delta_time):
        """Updates the actor position from the mouse.

        Args:
            delta_time: Time passed since the previous frame.
        """
        transform = self.actor.get_component_of_type(TransformComponent)
        if transform is None:
            return

        mouse_position = pygame.mouse.get_pos()
        transform.position = Vector(mouse_position[0], mouse_position[1])
