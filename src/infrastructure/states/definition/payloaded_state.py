# Defines the base interface for a state that enters with payload.
from infrastructure.states.definition.exitable_state import ExitableState


class PayloadedState(ExitableState):
    """Represents a state that accepts payload on enter."""

    def enter(self, payload):
        """Starts the state with payload.

        Args:
            payload: Value passed to the state.
        """
        raise NotImplementedError()
