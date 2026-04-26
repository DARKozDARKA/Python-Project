# Stores player and enemy data loaded from json files.
from game.static_data.enemy_data import EnemyData
from game.static_data.player_data import PlayerData
from infrastructure.service import Service


class StaticDataService(Service):
    """Stores loaded static game data."""

    def __init__(self):
        """Creates the static data service."""
        self.player_data = None
        self.enemy_data = None

    @property
    def player_data(self):
        return self._player_data

    @player_data.setter
    def player_data(self, value):
        if value is not None and not isinstance(value, PlayerData):
            raise TypeError("player_data must be a PlayerData object or None.")

        self._player_data = value

    @property
    def enemy_data(self):
        return self._enemy_data

    @enemy_data.setter
    def enemy_data(self, value):
        if value is not None and not isinstance(value, EnemyData):
            raise TypeError("enemy_data must be an EnemyData object or None.")

        self._enemy_data = value
