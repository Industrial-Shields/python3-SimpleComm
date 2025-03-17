"""
Private utils for SimpleComm library
"""



def _check_integer_is_valid(integer: int, n_bytes: int, signed: bool) -> None:
    """
    Validates that an integer fits within the specified range based on the number of bytes
    and whether it is signed or unsigned.

    Args:
        integer (int): The integer value to validate.
        n_bytes (int): The number of bytes that the integer should occupy.
        signed (bool): A flag indicating whether the integer is signed (True) or unsigned (False).

    Raises:
        AttributeError: If the integer is outside the valid range for the specified number of bytes.
    """
    if not signed:
        min_value = 0
        max_value = 2 ** (8 * n_bytes)
    else:
        min_value = -2 ** (8 * n_bytes - 1)
        max_value = 2 ** (8 * n_bytes - 1) - 1
    if integer < min_value or integer > max_value:
        err = f"The argument must fit between {min_value} and {max_value}. " \
            f"It's current value is {integer}"
        raise AttributeError(err)
