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
    continuation_bytes = 0

    for byte in data:
        mask = 1 << 7

        if continuation_bytes == 0:
            while mask & byte:
                continuation_bytes += 1
                mask >>= 1

            if continuation_bytes == 0:  # 1-byte character
                continue

            if continuation_bytes == 1 or continuation_bytes > 4:
                return False
        else:
            if not (byte & (1 << 7)) or (byte & (1 << 6)):
                return False

        continuation_bytes -= 1

    return continuation_bytes == 0
