# Defines the base interface for objects updated every frame.
class Tickable:
    """Represents an object that can be updated every frame."""

    def tick(self, delta_time):
        """Updates the object.

        Args:
            delta_time: Time passed since the previous frame.
        """
        raise NotImplementedError()
