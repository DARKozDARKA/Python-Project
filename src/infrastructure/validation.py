# Contains small validation helpers used across the project.
def ensure_bool(value, name):
    """Validates that a value is a boolean."""
    if not isinstance(value, bool):
        raise TypeError(f"{name} must be a boolean.")

    return value


def ensure_number(value, name):
    """Validates that a value is a number."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a number.")

    return value


def ensure_positive_number(value, name):
    """Validates that a value is a positive number."""
    ensure_number(value, name)

    if value <= 0:
        raise ValueError(f"{name} must be greater than 0.")

    return value


def ensure_positive_int(value, name):
    """Validates that a value is a positive integer."""
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{name} must be an integer.")

    if value <= 0:
        raise ValueError(f"{name} must be greater than 0.")

    return value


def ensure_non_negative_int(value, name):
    """Validates that a value is a non-negative integer."""
    if not isinstance(value, int) or isinstance(value, bool):
        raise TypeError(f"{name} must be an integer.")

    if value < 0:
        raise ValueError(f"{name} cannot be negative.")

    return value


def ensure_string(value, name):
    """Validates that a value is a non-empty string."""
    if not isinstance(value, str):
        raise TypeError(f"{name} must be a string.")

    if value.strip() == "":
        raise ValueError(f"{name} cannot be empty.")

    return value


def ensure_color(value, name):
    """Validates that a value is an RGB color tuple."""
    if not isinstance(value, tuple) or len(value) != 3:
        raise TypeError(f"{name} must be a tuple with three numbers.")

    validated_color = []
    for color_value in value:
        ensure_non_negative_int(color_value, name)
        if color_value > 255:
            raise ValueError(f"{name} values must be between 0 and 255.")

        validated_color.append(color_value)

    return tuple(validated_color)


def ensure_callable(value, name):
    """Validates that a value is callable."""
    if not callable(value):
        raise TypeError(f"{name} must be callable.")

    return value


def ensure_list(value, name):
    """Validates that a value is a list."""
    if not isinstance(value, list):
        raise TypeError(f"{name} must be a list.")

    return value
