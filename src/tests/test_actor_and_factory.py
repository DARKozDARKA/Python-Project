from unittest import TestCase, main

from game.actors.actor import Actor
from game.components.collider_component import ColliderComponent
from game.components.component import Component
from game.components.sprite_renderer_component import SpriteRendererComponent
from game.components.transform_component import TransformComponent
from game.services.actor_factory import ActorFactory
from infrastructure.all_services import AllServices
from infrastructure.collision.collision_service import CollisionService
from infrastructure.rendering.rendering_service import RenderingService
from infrastructure.tick.tickable import Tickable
from infrastructure.tick.tickable_service import TickableService


class CountingComponent(Component, Tickable):
    def __init__(self, actor):
        super().__init__(actor)
        self.tick_count = 0

    def tick(self, delta_time):
        self.tick_count += 1


class FactoryActor(Actor):
    def __init__(self):
        super().__init__()
        self.transform_component = self.add_component_of_type(
            TransformComponent,
            10,
            20,
        )
        self.render_component = self.add_component_of_type(
            SpriteRendererComponent,
            (10, 20, 30),
            "box",
            12,
        )
        self.collider_component = self.add_component_of_type(
            ColliderComponent,
            12,
        )
        self.counting_component = self.add_component_of_type(
            CountingComponent,
        )


class ActorAndFactoryTests(TestCase):
    def setUp(self):
        AllServices._instance = None

    def tearDown(self):
        AllServices._instance = None

    def create_factory(self):
        services = AllServices.container()
        services.register_single(TickableService())
        services.register_single(CollisionService())
        services.register_single(RenderingService())
        factory = ActorFactory(services)
        services.register_single(factory)
        return factory, services

    def test_actor_component_lifecycle(self):
        actor = Actor()
        component = actor.add_component_of_type(CountingComponent)

        self.assertIs(
            actor.get_component_of_type(CountingComponent),
            component,
        )
        self.assertFalse(component.started)

        actor.start()
        self.assertTrue(actor.started)
        self.assertTrue(component.started)

        removed = actor.remove_component_of_type(CountingComponent)
        self.assertIs(removed, component)
        self.assertTrue(removed.ended)
        self.assertIsNone(actor.get_component_of_type(CountingComponent))

        actor.destroy()
        self.assertTrue(actor.destroyed)
        self.assertTrue(actor.ended)

    def test_actor_factory_registers_and_unregisters_components(self):
        factory, services = self.create_factory()
        tickable_service = services.single(TickableService)
        collision_service = services.single(CollisionService)
        rendering_service = services.single(RenderingService)

        actor = factory.create_actor(FactoryActor)

        self.assertIn(actor, factory.actors)
        self.assertIn(actor.counting_component, tickable_service._tickables)
        self.assertIn(actor.collider_component, collision_service._colliders)
        self.assertIn(actor.render_component, rendering_service._renderers)
        self.assertTrue(actor.started)

        actor.destroy()

        self.assertTrue(actor.destroyed)
        self.assertNotIn(actor, factory.actors)
        self.assertNotIn(
            actor.counting_component,
            tickable_service._tickables,
        )
        self.assertNotIn(
            actor.collider_component,
            collision_service._colliders,
        )
        self.assertNotIn(
            actor.render_component,
            rendering_service._renderers,
        )


if __name__ == "__main__":
    main()
