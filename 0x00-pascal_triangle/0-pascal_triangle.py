#!/usr/bin/python3
"""
This module provides a function to generate Pascal's triangle with a given
number of rows.
"""


def pascal_triangle(n):
    """
    Generates a Pascal's triangle with n number of rows.

    Args:
        n (int): The number of rows in the Pascal's triangle.

    Returns:
        list: A list of lists representing the Pascal's triangle.

    Example:
        >>> pascal_triangle(5)
        [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]
    """
    if n <= 0:
        return []

    # Initialize the triangle with the first row
    triangle = [[1]]

    for i in range(1, n):
        row = [1]
        # Calculate the values for the middle of the row
        for j in range(1, i):
            row.append(triangle[i - 1][j - 1] + triangle[i - 1][j])
        # The last row element is always 1
        row.append(1)
        # Add the completed row to the triangle
        triangle.append(row)

    return triangle
