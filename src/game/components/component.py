# Defines the base class for all actor components.
from infrastructure.validation import ensure_bool


class Component:
    """Represents a base component attached to an actor."""

    def __init__(self, actor):
        """Creates a component.

        Args:
            actor: Owning actor.
        """
        self.actor = actor
        self.started = False
        self.ended = False

    @property
    def actor(self):
        return self._actor

    @actor.setter
    def actor(self, value):
        if value is None:
            raise ValueError("actor cannot be None.")

        self._actor = value

    @property
    def started(self):
        return self._started

    @started.setter
    def started(self, value):
        self._started = ensure_bool(value, "started")

    @property
    def ended(self):
        return self._ended

    @ended.setter
    def ended(self, value):
        self._ended = ensure_bool(value, "ended")

    def start(self):
        """Starts the component."""
        if self.started:
            return

        self.started = True

    def end(self):
        """Ends the component."""
        if self.ended:
            return

        self.ended = True

    def on_collision_enter(self, other_actor):
        """Handles the start of a collision.

        Args:
            other_actor: Actor that collided with this component owner.
        """
        pass
