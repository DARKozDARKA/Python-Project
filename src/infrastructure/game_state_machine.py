# Creates and switches between the game states.
from infrastructure.states.bootstrap.bootstrap_state import BootstrapState
from infrastructure.states.game_loop.game_loop_state import GameLoopState
from infrastructure.states.load_data.load_data_state import LoadDataState


class GameStateMachine:
    """Controls switching between game states."""

    def __init__(self, services):
        """Creates the game state machine.

        Args:
            services: Service container.
        """
        self._states = {
            BootstrapState: BootstrapState(self, services),
            LoadDataState: LoadDataState(self, services),
            GameLoopState: GameLoopState(self, services),
        }
        self.active_state = None

    @property
    def active_state(self):
        return self._active_state

    @active_state.setter
    def active_state(self, value):
        self._active_state = value

    def enter(self, state_class):
        """Enters a state without payload.

        Args:
            state_class: State type to enter.
        """
        state = self._change_state(state_class)
        state.enter()

    def enter_with_payload(self, state_class, payload):
        """Enters a state with payload.

        Args:
            state_class: State type to enter.
            payload: Payload passed to the state.
        """
        state = self._change_state(state_class)
        state.enter(payload)

    def _change_state(self, state_class):
        if self.active_state is not None:
            self.active_state.exit()

        state = self._get_state(state_class)
        self.active_state = state
        return state

    def _get_state(self, state_class):
        return self._states[state_class]
