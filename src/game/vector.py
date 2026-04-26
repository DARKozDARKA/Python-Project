# Defines a simple 2D vector used for game positions and movement.
from infrastructure.validation import ensure_number


class Vector:
    """Represents a 2D vector."""

    def __init__(self, x, y):
        """Creates a vector.

        Args:
            x: Horizontal value.
            y: Vertical value.
        """
        self.x = x
        self.y = y

    @property
    def x(self):
        return self._x

    @x.setter
    def x(self, value):
        self._x = ensure_number(value, "x")

    @property
    def y(self):
        return self._y

    @y.setter
    def y(self, value):
        self._y = ensure_number(value, "y")

    def __add__(self, other):
        """Returns the sum of two vectors.

        Args:
            other: Vector to add.

        Returns:
            Vector: Added vector.
        """
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        """Returns the difference of two vectors.

        Args:
            other: Vector to subtract.

        Returns:
            Vector: Subtracted vector.
        """
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, value):
        """Returns the vector scaled by a number.

        Args:
            value: Number to multiply by.

        Returns:
            Vector: Scaled vector.
        """
        value = ensure_number(value, "value")
        return Vector(self.x * value, self.y * value)

    def __truediv__(self, value):
        """Returns the vector divided by a number.

        Args:
            value: Number to divide by.

        Returns:
            Vector: Divided vector.
        """
        value = ensure_number(value, "value")
        if value == 0:
            raise ValueError("value cannot be 0.")

        return Vector(self.x / value, self.y / value)
