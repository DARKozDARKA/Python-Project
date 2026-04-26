# Stores renderer components and draws them every frame.
from game.components.sprite_renderer_component import SpriteRendererComponent
from infrastructure.service import Service


class RenderingService(Service):
    """Stores and renders sprite renderer components."""

    def __init__(self):
        """Creates the rendering service."""
        self._renderers = []

    def register(self, renderer):
        """Registers a renderer.

        Args:
            renderer: Renderer to register.
        """
        if not isinstance(renderer, SpriteRendererComponent):
            raise TypeError(
                "Only SpriteRendererComponent objects can be registered."
            )

        self._renderers.append(renderer)

    def unregister(self, renderer):
        """Unregisters a renderer.

        Args:
            renderer: Renderer to unregister.
        """
        if renderer in self._renderers:
            self._renderers.remove(renderer)

    def render(self, screen):
        """Renders every registered renderer.

        Args:
            screen: Pygame surface to draw on.
        """
        for renderer in self._renderers[:]:
            renderer.render(screen)
