# Runs the pygame loop and creates the initial actors.
import pygame

from game.actors.enemy import Enemy
from game.actors.player import Player
from game.display_settings import DisplaySettings
from game.services.actor_factory import ActorFactory
from game.services.static_data_service import StaticDataService
from infrastructure.rendering.rendering_service import RenderingService
from infrastructure.states.definition.state import State
from infrastructure.tick.tickable_service import TickableService


class GameLoopState(State):
    """Runs the main pygame loop."""

    def __init__(self, game_state_machine, services):
        """Creates the game loop state.

        Args:
            game_state_machine: Game state machine instance.
            services: Service container.
        """
        self._game_state_machine = game_state_machine
        self._services = services
        self._actor_factory = None

    def enter(self):
        """Runs the frame loop until the window is closed."""
        display_settings = self._services.single(DisplaySettings)
        tickable_service = self._services.single(TickableService)
        rendering_service = self._services.single(RenderingService)
        static_data_service = self._services.single(StaticDataService)
        self._actor_factory = self._services.single(ActorFactory)

        pygame.init()
        screen = pygame.display.set_mode(
            (display_settings.width, display_settings.height)
        )
        pygame.display.set_caption(display_settings.title)
        clock = pygame.time.Clock()
        running = True

        self.create_actors(static_data_service)

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            delta_time = clock.tick(display_settings.fps) / 1000.0
            tickable_service.tick(delta_time)
            screen.fill(display_settings.background_color)
            rendering_service.render(screen)
            pygame.display.flip()

        self.exit()

    def create_actors(self, static_data_service):
        if len(self._actor_factory.actors) == 0:
            self._actor_factory.create_actor(
                Player,
                static_data_service.player_data.health,
                static_data_service.player_data.size,
            )
            self._actor_factory.create_actor(
                Enemy,
                100,
                100,
                1,
                0.5,
                static_data_service.enemy_data.damage,
                static_data_service.enemy_data.size,
                static_data_service.enemy_data.speed,
            )
            self._actor_factory.create_actor(
                Enemy,
                700,
                120,
                -0.8,
                1,
                static_data_service.enemy_data.damage,
                static_data_service.enemy_data.size,
                static_data_service.enemy_data.speed,
            )
            self._actor_factory.create_actor(
                Enemy,
                150,
                500,
                1,
                -0.6,
                static_data_service.enemy_data.damage,
                static_data_service.enemy_data.size,
                static_data_service.enemy_data.speed,
            )

    def exit(self):
        """Ends the game loop state."""
        if self._actor_factory is not None:
            while len(self._actor_factory.actors) > 0:
                self._actor_factory.destroy_actor(
                    self._actor_factory.actors[0]
                )

        pygame.quit()
