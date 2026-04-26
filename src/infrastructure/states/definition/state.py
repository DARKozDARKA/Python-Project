# Defines the base interface for a state without payload.
from infrastructure.states.definition.exitable_state import ExitableState


class State(ExitableState):
    """Represents a state without payload."""

    def enter(self):
        """Starts the state."""
        raise NotImplementedError()
