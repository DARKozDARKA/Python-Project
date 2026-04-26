from unittest import TestCase, main

from game.actors.enemy import Enemy
from game.actors.player import Player
from game.components.transform_component import TransformComponent
from game.services.actor_factory import ActorFactory
from infrastructure.all_services import AllServices
from infrastructure.collision.collision_service import CollisionService
from infrastructure.rendering.rendering_service import RenderingService
from infrastructure.tick.tickable_service import TickableService


class CollisionAndEntityTests(TestCase):
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

    def test_player_loses_health_and_enemy_is_destroyed_on_collision(self):
        factory, services = self.create_factory()
        collision_service = services.single(CollisionService)

        player = factory.create_actor(Player, 3, 20)
        enemy = factory.create_actor(Enemy, 400, 300, 1, 0, 1, 30, 120)

        collision_service.tick(0.016)

        self.assertEqual(player.health_component.current_health, 2)
        self.assertTrue(enemy.destroyed)
        self.assertNotIn(enemy, factory.actors)

    def test_player_is_destroyed_after_losing_all_health(self):
        factory, services = self.create_factory()
        collision_service = services.single(CollisionService)
        player = factory.create_actor(Player, 3, 20)

        for _ in range(3):
            enemy = factory.create_actor(Enemy, 400, 300, 1, 0, 1, 30, 120)
            collision_service.tick(0.016)
            collision_service.tick(0.016)
            self.assertTrue(enemy.destroyed)

        self.assertTrue(player.destroyed)
        self.assertNotIn(player, factory.actors)

    def test_enemy_move_component_updates_transform(self):
        enemy = Enemy(10, 15, 1, -0.5, 1, 30, 100)

        enemy.move_component.tick(0.5)
        transform = enemy.get_component_of_type(TransformComponent)

        self.assertEqual(transform.position.x, 60)
        self.assertEqual(transform.position.y, -10)


if __name__ == "__main__":
    main()
