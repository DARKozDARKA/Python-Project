from unittest import TestCase, main

from game.display_settings import DisplaySettings
from game.static_data.enemy_data import EnemyData
from game.static_data.player_data import PlayerData
from game.vector import Vector
from infrastructure.validation import ensure_color
from infrastructure.validation import ensure_positive_int


class ValidationAndVectorTests(TestCase):
    def test_vector_math_operators(self):
        first = Vector(10, 5)
        second = Vector(4, 1)

        added = first + second
        subtracted = first - second
        multiplied = first * 2
        divided = first / 5

        self.assertEqual(added.x, 14)
        self.assertEqual(added.y, 6)
        self.assertEqual(subtracted.x, 6)
        self.assertEqual(subtracted.y, 4)
        self.assertEqual(multiplied.x, 20)
        self.assertEqual(multiplied.y, 10)
        self.assertEqual(divided.x, 2)
        self.assertEqual(divided.y, 1)

    def test_vector_division_by_zero_raises_error(self):
        with self.assertRaises(ValueError):
            _ = Vector(1, 2) / 0

    def test_display_settings_validate_values(self):
        settings = DisplaySettings(800, 600, "Game", (255, 255, 255), 60)

        self.assertEqual(settings.width, 800)
        self.assertEqual(settings.height, 600)
        self.assertEqual(settings.title, "Game")
        self.assertEqual(settings.background_color, (255, 255, 255))
        self.assertEqual(settings.fps, 60)

        with self.assertRaises(ValueError):
            settings.fps = 0

    def test_static_data_classes_store_values(self):
        player_data = PlayerData(3, 20)
        enemy_data = EnemyData(1, 30, 120)

        self.assertEqual(player_data.health, 3)
        self.assertEqual(player_data.size, 20)
        self.assertEqual(enemy_data.damage, 1)
        self.assertEqual(enemy_data.size, 30)
        self.assertEqual(enemy_data.speed, 120)

    def test_validation_helpers_raise_for_bad_values(self):
        with self.assertRaises(ValueError):
            ensure_positive_int(0, "health")

        with self.assertRaises(ValueError):
            ensure_color((300, 0, 0), "color")


if __name__ == "__main__":
    main()
