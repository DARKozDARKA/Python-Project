# Stores screen setup values used by the pygame window.
from infrastructure.service import Service
from infrastructure.validation import ensure_color
from infrastructure.validation import ensure_positive_int
from infrastructure.validation import ensure_string


class DisplaySettings(Service):
    """Stores display configuration values."""

    def __init__(self, width, height, title, background_color, fps):
        """Creates display settings.

        Args:
            width: Window width.
            height: Window height.
            title: Window title.
            background_color: Window background color.
            fps: Target frames per second.
        """
        self.width = width
        self.height = height
        self.title = title
        self.background_color = background_color
        self.fps = fps

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        self._width = ensure_positive_int(value, "width")

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = ensure_positive_int(value, "height")

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = ensure_string(value, "title")

    @property
    def background_color(self):
        return self._background_color

    @background_color.setter
    def background_color(self, value):
        self._background_color = ensure_color(value, "background_color")

    @property
    def fps(self):
        return self._fps

    @fps.setter
    def fps(self, value):
        self._fps = ensure_positive_int(value, "fps")
