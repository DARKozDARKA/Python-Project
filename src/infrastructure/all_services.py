# Fake static DI.
from infrastructure.service import Service


class AllServices:
    """Stores global singleton-style services."""

    _instance = None

    def __init__(self):
        """Creates the service container."""
        self._services = {}

    @classmethod
    def container(cls):
        """Returns the shared service container.

        Returns:
            AllServices: Shared container instance.
        """
        if cls._instance is None:
            cls._instance = AllServices()
        return cls._instance

    def clear(self):
        """Removes all registered services."""
        self._services.clear()

    def register_single(self, implementation):
        """Registers a single service instance.

        Args:
            implementation: Service instance to register.
        """
        if not isinstance(implementation, Service):
            raise TypeError("Only Service objects can be registered.")
        self._services[implementation.__class__] = implementation

    def single(self, service_type):
        """Returns a registered service.

        Args:
            service_type: Service type to find.

        Returns:
            Service: Registered service instance.
        """
        return self._services[service_type]
