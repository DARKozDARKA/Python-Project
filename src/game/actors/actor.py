# Defines the base actor class and its component lifecycle.
from infrastructure.validation import ensure_bool
from infrastructure.validation import ensure_callable
from infrastructure.validation import ensure_list


class Actor:
    """Represents a base actor in the game world."""

    def __init__(self):
        """Creates an actor."""
        self.started = False
        self.ended = False
        self.destroyed = False
        self.components = []
        self._destroy_callbacks = []
        self._component_added_callbacks = []
        self._component_removed_callbacks = []

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

    @property
    def destroyed(self):
        return self._destroyed

    @destroyed.setter
    def destroyed(self, value):
        self._destroyed = ensure_bool(value, "destroyed")

    @property
    def components(self):
        return self._components

    @components.setter
    def components(self, value):
        self._components = ensure_list(value, "components")

    def start(self):
        """Starts the actor and its components."""
        if self.started:
            return

        self.started = True

        for component in self.components[:]:
            component.start()

    def end(self):
        """Ends the actor and its components."""
        if self.ended:
            return

        components = self.components[:]
        for component in components:
            self._remove_component(component)

        self.ended = True

    def add_destroy_callback(self, callback):
        """Adds a callback that runs when the actor is destroyed.

        Args:
            callback: Function to call on destroy.
        """
        self._destroy_callbacks.append(
            ensure_callable(callback, "callback")
        )

    def add_component_added_callback(self, callback):
        """Adds a callback for component creation.

        Args:
            callback: Function to call after a component is added.
        """
        self._component_added_callbacks.append(
            ensure_callable(callback, "callback")
        )

    def add_component_removed_callback(self, callback):
        """Adds a callback for component removal.

        Args:
            callback: Function to call after a component is removed.
        """
        self._component_removed_callbacks.append(
            ensure_callable(callback, "callback")
        )

    def add_component_of_type(self, component_type, *args):
        """Creates and adds a component.

        Args:
            component_type: Component class to create.
            *args: Extra values passed to the component constructor.

        Returns:
            Component: Created component.
        """
        component = component_type(self, *args)
        self.components.append(component)

        callbacks = self._component_added_callbacks[:]
        for callback in callbacks:
            callback(component)

        if self.started and not self.ended:
            component.start()

        return component

    def remove_component_of_type(self, component_type):
        """Removes the first component of the requested type.

        Args:
            component_type: Component type to remove.

        Returns:
            Component | None: Removed component or None.
        """
        for component in self.components:
            if isinstance(component, component_type):
                self._remove_component(component)
                return component

        return None

    def _remove_component(self, component):
        if component not in self.components:
            return

        self.components.remove(component)

        if not component.ended:
            component.end()

        callbacks = self._component_removed_callbacks[:]
        for callback in callbacks:
            callback(component)

    def get_component_of_type(self, component_type):
        """Returns the first component of the requested type.

        Args:
            component_type: Component type to find.

        Returns:
            Component | None: Found component or None.
        """
        for component in self.components:
            if isinstance(component, component_type):
                return component

        return None

    def on_collision_enter(self, other_actor):
        """Handles the start of a collision.

        Args:
            other_actor: Actor that collided with this actor.
        """
        for component in self.components[:]:
            component.on_collision_enter(other_actor)

    def destroy(self):
        """Destroys the actor."""
        if self.destroyed:
            return

        self.end()
        self.destroyed = True

        callbacks = self._destroy_callbacks[:]
        for callback in callbacks:
            callback(self)
