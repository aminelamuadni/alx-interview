#!/usr/bin/python3
"""
Function that validates if a data set represents a valid UTF-8 encoding.
"""


def validUTF8(data):
    """
    Check if data is a valid UTF-8 encoding.
    Args:
    - data: List of integers representing bytes.
    Returns:
    - True if data is a valid UTF-8 encoding, otherwise False.
    """
    n_bytes = 0

    for num in data:
        # Mask to extract the least significant 8 bits
        num &= 0xFF

        if n_bytes == 0:
            # Get the number of leading 1s in the first byte
            if (num >> 7) == 0:
                n_bytes = 0
            elif (num >> 5) == 0b110:
                n_bytes = 1
            elif (num >> 4) == 0b1110:
                n_bytes = 2
            elif (num >> 3) == 0b11110:
                n_bytes = 3
            else:
                return False
        else:
            # For subsequent bytes, they should all start with 10xxxxxx
            if (num >> 6) != 0b10:
                return False
        n_bytes -= 1

    return n_bytes == 0
