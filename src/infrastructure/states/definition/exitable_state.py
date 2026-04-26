# Defines the base interface for a state that can be exited.
class ExitableState:
    """Represents a state that can be exited."""

    def exit(self):
        """Ends the state."""
        raise NotImplementedError()
