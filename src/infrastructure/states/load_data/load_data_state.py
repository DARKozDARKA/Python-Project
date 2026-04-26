# Loads player and enemy data from configured json files.
import configparser
import json
import os

from game.services.static_data_service import StaticDataService
from game.static_data.enemy_data import EnemyData
from game.static_data.player_data import PlayerData
from infrastructure.states.definition.state import State
from infrastructure.states.game_loop.game_loop_state import GameLoopState


class LoadDataState(State):
    """Loads static data from json files."""

    def __init__(self, game_state_machine, services):
        """Creates the load data state.

        Args:
            game_state_machine: Game state machine instance.
            services: Service container.
        """
        self._game_state_machine = game_state_machine
        self._services = services

    def enter(self):
        """Loads configured json files and moves to the game loop state."""
        static_data_service = self._services.single(StaticDataService)
        project_folder_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..", "..", "..")
        )
        config_path = os.path.join(
            project_folder_path,
            "config",
            "settings.ini",
        )
        config = configparser.ConfigParser()
        config.read(config_path)
        player_data_path = os.path.join(
            project_folder_path,
            config["data"]["player_data_path"],
        )
        enemy_data_path = os.path.join(
            project_folder_path,
            config["data"]["enemy_data_path"],
        )

        with open(player_data_path, "r", encoding="utf-8") as player_data_file:
            player_data_json = json.load(player_data_file)

        with open(enemy_data_path, "r", encoding="utf-8") as enemy_data_file:
            enemy_data_json = json.load(enemy_data_file)

        static_data_service.player_data = PlayerData(
            player_data_json["health"],
            player_data_json["size"],
        )
        static_data_service.enemy_data = EnemyData(
            enemy_data_json["damage"],
            enemy_data_json["size"],
            enemy_data_json["speed"],
        )

        self._game_state_machine.enter(GameLoopState)

    def exit(self):
        """Ends the load data state."""
        pass
