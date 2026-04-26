# Defines the enemy actor and its collision behavior.
from game.actors.actor import Actor
from game.components.collider_component import ColliderComponent
from game.components.move_component import MoveComponent
from game.components.sprite_renderer_component import SpriteRendererComponent
from game.components.transform_component import TransformComponent
from infrastructure.tick.tickable import Tickable
from infrastructure.validation import ensure_positive_int


class Enemy(Actor):
    """Represents an enemy actor."""

    def __init__(self, x, y, direction_x, direction_y, damage, size, speed):
        """Creates an enemy.

        Args:
            x: Initial x position.
            y: Initial y position.
            direction_x: Horizontal movement direction.
            direction_y: Vertical movement direction.
            damage: Damage dealt to the player.
            size: Enemy visual size.
            speed: Enemy movement speed.
        """
        super().__init__()
        self.damage = damage
        self.transform_component = self.add_component_of_type(
            TransformComponent,
            x,
            y,
        )
        self.move_component = self.add_component_of_type(
            MoveComponent,
            direction_x,
            direction_y,
            speed,
        )
        self.sprite_renderer_component = self.add_component_of_type(
            SpriteRendererComponent,
            (200, 50, 50),
            "box",
            size,
        )
        self.collider_component = self.add_component_of_type(
            ColliderComponent,
            size,
        )

    @property
    def damage(self):
        return self._damage

    @damage.setter
    def damage(self, value):
        self._damage = ensure_positive_int(value, "damage")

    @property
    def transform_component(self):
        return self._transform_component

    @transform_component.setter
    def transform_component(self, value):
        if not isinstance(value, TransformComponent):
            raise TypeError(
                "transform_component must be a TransformComponent."
            )

        self._transform_component = value

    @property
    def move_component(self):
        return self._move_component

    @move_component.setter
    def move_component(self, value):
        if not isinstance(value, MoveComponent):
            raise TypeError("move_component must be a MoveComponent.")

        self._move_component = value

    @property
    def sprite_renderer_component(self):
        return self._sprite_renderer_component

    @sprite_renderer_component.setter
    def sprite_renderer_component(self, value):
        if not isinstance(value, SpriteRendererComponent):
            raise TypeError(
                "sprite_renderer_component must be a SpriteRendererComponent."
            )

        self._sprite_renderer_component = value

    @property
    def collider_component(self):
        return self._collider_component

    @collider_component.setter
    def collider_component(self, value):
        if not isinstance(value, ColliderComponent):
            raise TypeError(
                "collider_component must be a ColliderComponent."
            )

        self._collider_component = value

    def on_collision_enter(self, other_actor):
        """Handles the start of a collision.

        Args:
            other_actor: Actor that collided with the enemy.
        """
        super().on_collision_enter(other_actor)

        if other_actor.__class__.__name__ == "Player":
            self.destroy()
