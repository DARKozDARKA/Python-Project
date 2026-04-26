# Defines the player actor and its collision behavior.
from game.actors.actor import Actor
from game.components.collider_component import ColliderComponent
from game.components.health_component import HealthComponent
from game.components.mouse_follow_component import MouseFollowComponent
from game.components.sprite_renderer_component import SpriteRendererComponent
from game.components.transform_component import TransformComponent


class Player(Actor):
    """Represents the player actor."""

    def __init__(self, health, size):
        """Creates a player.

        Args:
            health: Player health value.
            size: Player visual size.
        """
        super().__init__()
        self.transform_component = self.add_component_of_type(
            TransformComponent,
            400,
            300,
        )
        self.health_component = self.add_component_of_type(
            HealthComponent,
            health,
        )
        self.mouse_follow_component = self.add_component_of_type(
            MouseFollowComponent,
        )
        self.sprite_renderer_component = self.add_component_of_type(
            SpriteRendererComponent,
            (0, 0, 0),
            "circle",
            size,
        )
        self.collider_component = self.add_component_of_type(
            ColliderComponent,
            size * 2,
        )

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
    def health_component(self):
        return self._health_component

    @health_component.setter
    def health_component(self, value):
        if not isinstance(value, HealthComponent):
            raise TypeError("health_component must be a HealthComponent.")

        self._health_component = value

    @property
    def mouse_follow_component(self):
        return self._mouse_follow_component

    @mouse_follow_component.setter
    def mouse_follow_component(self, value):
        if not isinstance(value, MouseFollowComponent):
            raise TypeError(
                "mouse_follow_component must be a MouseFollowComponent."
            )

        self._mouse_follow_component = value

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
            other_actor: Actor that collided with the player.
        """
        super().on_collision_enter(other_actor)

        if other_actor.__class__.__name__ == "Enemy":
            self.health_component.take_damage(other_actor.damage)

            if self.health_component.current_health == 0:
                self.destroy()
