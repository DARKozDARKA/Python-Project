# Defines a health component used by damageable actors.
from game.components.component import Component
from infrastructure.validation import ensure_non_negative_int
from infrastructure.validation import ensure_positive_int


class HealthComponent(Component):
    """Represents health data for an actor."""

    def __init__(self, actor, max_health):
        """Creates a health component.

        Args:
            actor: Owning actor.
            max_health: Maximum health.
        """
        super().__init__(actor)
        self.max_health = max_health
        self.current_health = max_health

    @property
    def max_health(self):
        return self._max_health

    @max_health.setter
    def max_health(self, value):
        self._max_health = ensure_positive_int(value, "max_health")

    @property
    def current_health(self):
        return self._current_health

    @current_health.setter
    def current_health(self, value):
        value = ensure_non_negative_int(value, "current_health")
        if value > self.max_health:
            raise ValueError(
                "current_health cannot be greater than max_health."
            )

        self._current_health = value

    def take_damage(self, damage):
        """Reduces the current health.

        Args:
            damage: Damage amount.
        """
        damage = ensure_non_negative_int(damage, "damage")
        self.current_health = max(self.current_health - damage, 0)
