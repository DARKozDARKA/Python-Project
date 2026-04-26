import os
from unittest import TestCase, main

import pygame

from game.components.sprite_renderer_component import SpriteRendererComponent
from game.components.transform_component import TransformComponent
from game.services.actor_factory import ActorFactory
from game.services.static_data_service import StaticDataService
from infrastructure.all_services import AllServices
from infrastructure.collision.collision_service import CollisionService
from infrastructure.game_state_machine import GameStateMachine
from infrastructure.rendering.rendering_service import RenderingService
from infrastructure.states.bootstrap.bootstrap_state import BootstrapState
from infrastructure.states.game_loop.game_loop_state import GameLoopState
from infrastructure.states.load_data.load_data_state import LoadDataState
from infrastructure.tick.tickable import Tickable
from infrastructure.tick.tickable_service import TickableService


class CountingTickable(Tickable):
    def __init__(self):
        self.count = 0

    def tick(self, delta_time):
        self.count += 1


class RenderActor:
    def __init__(self):
        self._transform = TransformComponent(self, 30, 40)

    def get_component_of_type(self, component_type):
        if component_type is TransformComponent:
            return self._transform

        return None


class StatesAndServicesTests(TestCase):
    def setUp(self):
        AllServices._instance = None
        os.environ["SDL_VIDEODRIVER"] = "dummy"
        pygame.init()

    def tearDown(self):
        pygame.quit()
        AllServices._instance = None

    def test_all_services_register_and_return_singletons(self):
        services = AllServices.container()
        tickable_service = TickableService()

        services.register_single(tickable_service)

        self.assertIs(services.single(TickableService), tickable_service)

        services.clear()
        self.assertEqual(services._services, {})

    def test_tickable_service_ticks_registered_objects(self):
        service = TickableService()
        tickable = CountingTickable()

        service.register(tickable)
        service.tick(0.016)
        service.unregister(tickable)
        service.tick(0.016)

        self.assertEqual(tickable.count, 1)

    def test_rendering_service_draws_registered_renderers(self):
        service = RenderingService()
        actor = RenderActor()
        renderer = SpriteRendererComponent(actor, (0, 0, 0), "box", 10)
        screen = pygame.Surface((100, 100))

        service.register(renderer)
        service.render(screen)
        service.unregister(renderer)

        self.assertEqual(screen.get_at((30, 40))[:3], (0, 0, 0))

    def test_bootstrap_state_registers_core_services(self):
        services = AllServices.container()

        class DummyMachine:
            def __init__(self):
                self.entered_state = None

            def enter(self, state_type):
                self.entered_state = state_type

        machine = DummyMachine()
        state = BootstrapState(machine, services)

        state.enter()

        self.assertIsInstance(
            services.single(TickableService),
            TickableService,
        )
        self.assertIsInstance(
            services.single(CollisionService),
            CollisionService,
        )
        self.assertIsInstance(
            services.single(RenderingService),
            RenderingService,
        )
        self.assertIsInstance(
            services.single(ActorFactory),
            ActorFactory,
        )
        self.assertIsInstance(
            services.single(StaticDataService),
            StaticDataService,
        )
        self.assertIs(machine.entered_state, LoadDataState)

    def test_load_data_state_reads_configured_json_files(self):
        services = AllServices.container()
        services.register_single(StaticDataService())

        class DummyMachine:
            def __init__(self):
                self.entered_state = None

            def enter(self, state_type):
                self.entered_state = state_type

        machine = DummyMachine()
        state = LoadDataState(machine, services)
        state.enter()
        static_data_service = services.single(StaticDataService)

        self.assertEqual(static_data_service.player_data.health, 3)
        self.assertEqual(static_data_service.player_data.size, 20)
        self.assertEqual(static_data_service.enemy_data.damage, 1)
        self.assertEqual(static_data_service.enemy_data.size, 30)
        self.assertEqual(static_data_service.enemy_data.speed, 120)
        self.assertIs(machine.entered_state, GameLoopState)

    def test_game_state_machine_registers_states_on_creation(self):
        services = AllServices.container()
        machine = GameStateMachine(services)
        state_types = set(machine._states.keys())

        self.assertIn(BootstrapState, state_types)
        self.assertIn(LoadDataState, state_types)
        self.assertIn(GameLoopState, state_types)
        self.assertIsNone(machine.active_state)


if __name__ == "__main__":
    main()
