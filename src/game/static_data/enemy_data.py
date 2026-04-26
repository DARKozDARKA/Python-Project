# Stores static values loaded for enemies.
from infrastructure.validation import ensure_positive_int


class EnemyData:
    """Stores enemy static data."""

    def __init__(self, damage, size, speed):
        """Creates enemy static data.

        Args:
            damage: Enemy damage value.
            size: Enemy size value.
            speed: Enemy speed value.
        """
        self.damage = damage
        self.size = size
        self.speed = speed

    @property
    def damage(self):
        return self._damage

    @damage.setter
    def damage(self, value):
        self._damage = ensure_positive_int(value, "damage")

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = ensure_positive_int(value, "size")

    @property
    def speed(self):
        return self._speed

    @speed.setter
    def speed(self, value):
        self._speed = ensure_positive_int(value, "speed")
