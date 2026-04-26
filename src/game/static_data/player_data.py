# Stores static values loaded for the player.
from infrastructure.validation import ensure_positive_int


class PlayerData:
    """Stores player static data."""

    def __init__(self, health, size):
        """Creates player static data.

        Args:
            health: Player health value.
            size: Player size value.
        """
        self.health = health
        self.size = size

    @property
    def health(self):
        return self._health

    @health.setter
    def health(self, value):
        self._health = ensure_positive_int(value, "health")

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = ensure_positive_int(value, "size")
