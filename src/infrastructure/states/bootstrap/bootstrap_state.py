# Registers core services needed before game data is loaded.
from game.display_settings import DisplaySettings
from game.services.actor_factory import ActorFactory
from game.services.static_data_service import StaticDataService
from infrastructure.collision.collision_service import CollisionService
from infrastructure.rendering.rendering_service import RenderingService
from infrastructure.states.definition.state import State
from infrastructure.states.load_data.load_data_state import LoadDataState
from infrastructure.tick.tickable_service import TickableService


class BootstrapState(State):
    """Registers startup services."""

    def __init__(self, game_state_machine, services):
        """Creates the bootstrap state.

        Args:
            game_state_machine: Game state machine instance.
            services: Service container.
        """
        self._game_state_machine = game_state_machine
        self._services = services

    def enter(self):
        """Initializes services and moves to the load data state."""
        self._services.clear()
        self._services.register_single(
            DisplaySettings(
                800,
                600,
                "Pygame Window",
                (255, 255, 255),
                60,
            )
        )

        tickable_service = TickableService()
        collision_service = CollisionService()
        self._services.register_single(tickable_service)
        self._services.register_single(collision_service)
        self._services.register_single(RenderingService())
        self._services.register_single(ActorFactory(self._services))
        self._services.register_single(StaticDataService())
        tickable_service.register(collision_service)

        self._game_state_machine.enter(LoadDataState)

    def exit(self):
        """Ends the bootstrap state."""
        pass
