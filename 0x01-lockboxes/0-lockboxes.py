#!/usr/bin/python3

"""
This module contains a function to check if all the boxes in the given list can
be unlocked.
"""


def canUnlockAll(boxes):
    """
    Check if all the boxes in the given list can be unlocked.

    Args:
        boxes (list): A list of lists representing the lockboxes. Each inner
        list contains the keys to other boxes.

    Returns:
        bool: True if all boxes can be unlocked, False otherwise.
    """
    n = len(boxes)
    unlocked = [False] * n
    unlocked[0] = True
    stack = [0]

    while stack:
        current_box = stack.pop()
        for key in boxes[current_box]:
            if key < n and not unlocked[key]:
                unlocked[key] = True
                stack.append(key)

    return all(unlocked)
