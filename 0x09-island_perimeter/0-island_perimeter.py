#!/usr/bin/python3
"""
This module provides a function to calculate the perimeter of an island in a
grid.
The grid consists of '1's (land) and '0's (water), and the perimeter is
calculated based on the presence of water or grid edges adjacent to the land
cells.
"""


def island_perimeter(grid):
    """
    Calculate the perimeter of an island in a grid.

    Args:
    grid (list of list of int): The grid representation of the map, where 1 is
    land and 0 is water.

    Returns:
    int: The total perimeter of the island surrounded by water or grid edges.
    """
    rows = len(grid)
    cols = len(grid[0])
    perimeter = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                # North
                if r == 0 or grid[r - 1][c] == 0:
                    perimeter += 1
                # South
                if r == rows - 1 or grid[r + 1][c] == 0:
                    perimeter += 1
                # West
                if c == 0 or grid[r][c - 1] == 0:
                    perimeter += 1
                # East
                if c == cols - 1 or grid[r][c + 1] == 0:
                    perimeter += 1

    return perimeter
