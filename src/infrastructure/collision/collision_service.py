# Checks box collisions between registered collider components.
from game.components.collider_component import ColliderComponent
from game.components.transform_component import TransformComponent
from infrastructure.service import Service
from infrastructure.tick.tickable import Tickable


class CollisionService(Service, Tickable):
    """Checks collisions between registered colliders."""

    def __init__(self):
        """Creates the collision service."""
        self._colliders = []
        self._active_collisions = []

    def register(self, collider):
        """Registers a collider.

        Args:
            collider: Collider to register.
        """
        if not isinstance(collider, ColliderComponent):
            raise TypeError(
                "Only ColliderComponent objects can be registered."
            )

        self._colliders.append(collider)

    def unregister(self, collider):
        """Unregisters a collider.

        Args:
            collider: Collider to unregister.
        """
        if collider in self._colliders:
            self._colliders.remove(collider)

        active_collisions = []
        for collision in self._active_collisions:
            if collider not in collision:
                active_collisions.append(collision)

        self._active_collisions = active_collisions

    def tick(self, delta_time):
        """Checks every collider pair.

        Args:
            delta_time: Time passed since the previous frame.
        """
        current_collisions = []
        colliders = self._colliders[:]

        for first_index in range(len(colliders)):
            first_collider = colliders[first_index]

            for second_index in range(first_index + 1, len(colliders)):
                second_collider = colliders[second_index]

                if first_collider not in self._colliders:
                    continue

                if second_collider not in self._colliders:
                    continue

                if not self._are_colliding(first_collider, second_collider):
                    continue

                collision_pair = self._get_collision_pair(
                    first_collider,
                    second_collider,
                )
                current_collisions.append(collision_pair)

                if collision_pair not in self._active_collisions:
                    first_collider.actor.on_collision_enter(
                        second_collider.actor
                    )
                    second_collider.actor.on_collision_enter(
                        first_collider.actor
                    )

        self._active_collisions = current_collisions

    def _get_collision_pair(self, first_collider, second_collider):
        if id(first_collider) < id(second_collider):
            return (first_collider, second_collider)

        return (second_collider, first_collider)

    def _are_colliding(self, first_collider, second_collider):
        first_transform = first_collider.actor.get_component_of_type(
            TransformComponent
        )
        second_transform = second_collider.actor.get_component_of_type(
            TransformComponent
        )

        if first_transform is None or second_transform is None:
            return False

        distance = first_transform.position - second_transform.position

        return self._are_boxes_colliding(
            distance.x,
            distance.y,
            first_collider.size,
            second_collider.size,
        )

    def _are_boxes_colliding(
        self,
        delta_x,
        delta_y,
        first_size,
        second_size,
    ):
        first_half_size = first_size / 2
        second_half_size = second_size / 2

        if abs(delta_x) > first_half_size + second_half_size:
            return False

        if abs(delta_y) > first_half_size + second_half_size:
            return False

        return True
