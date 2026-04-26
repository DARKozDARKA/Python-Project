# Creates actors and registers their components in engine services.
from game.components.collider_component import ColliderComponent
from game.components.sprite_renderer_component import SpriteRendererComponent
from infrastructure.collision.collision_service import CollisionService
from infrastructure.rendering.rendering_service import RenderingService
from infrastructure.service import Service
from infrastructure.tick.tickable import Tickable
from infrastructure.tick.tickable_service import TickableService
from infrastructure.validation import ensure_list


class ActorFactory(Service):
    """Creates and destroys actors."""

    def __init__(self, services):
        """Creates an actor factory.

        Args:
            services: Service container.
        """
        self._services = services
        self.actors = []

    @property
    def actors(self):
        return self._actors

    @actors.setter
    def actors(self, value):
        self._actors = ensure_list(value, "actors")

    def create_actor(self, actor_class, *args):
        """Creates an actor and registers its systems.

        Args:
            actor_class: Actor class to create.
            *args: Extra values passed to the actor constructor.

        Returns:
            Actor: Created actor.
        """
        actor = actor_class(*args)
        actor.add_destroy_callback(self._unregister_actor)
        actor.add_component_added_callback(self._register_component)
        actor.add_component_removed_callback(self._unregister_component)

        if isinstance(actor, Tickable):
            tickable_service = self._services.single(TickableService)
            tickable_service.register(actor)

        for component in actor.components:
            self._register_component(component)

        self.actors.append(actor)
        actor.start()
        return actor

    def _register_component(self, component):
        if isinstance(component, Tickable):
            tickable_service = self._services.single(TickableService)
            tickable_service.register(component)

        if isinstance(component, ColliderComponent):
            collision_service = self._services.single(CollisionService)
            collision_service.register(component)

        if isinstance(component, SpriteRendererComponent):
            rendering_service = self._services.single(RenderingService)
            rendering_service.register(component)

    def _unregister_component(self, component):
        if isinstance(component, Tickable):
            tickable_service = self._services.single(TickableService)
            tickable_service.unregister(component)

        if isinstance(component, ColliderComponent):
            collision_service = self._services.single(CollisionService)
            collision_service.unregister(component)

        if isinstance(component, SpriteRendererComponent):
            rendering_service = self._services.single(RenderingService)
            rendering_service.unregister(component)

    def _unregister_actor(self, actor):
        if isinstance(actor, Tickable):
            tickable_service = self._services.single(TickableService)
            tickable_service.unregister(actor)

        if actor in self.actors:
            self.actors.remove(actor)

    def destroy_actor(self, actor):
        """Destroys an actor.

        Args:
            actor: Actor to destroy.
        """
        actor.destroy()
