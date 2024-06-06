#!/usr/bin/python3
"""
This module determines the minimum number of coins needed for a given total
using various denominations.
"""


def makeChange(coins, total):
    """
    Calculates the minimum number of coins needed to make change for a given
    total.

    Args:
        coins (list): List of coin denominations available.
        total (int): The total amount to make change for.

    Returns:
        int: The minimum number of coins needed to make change for the given
             total.
             Returns -1 if it is not possible to make change for the total
             using the given coins.
    """
    if total <= 0:
        return 0
    if not coins:
        return -1

    coinCounts = [float('inf')] * (total + 1)
    coinCounts[0] = 0

    for coin in coins:
        for amount in range(coin, total + 1):
            if coinCounts[amount - coin] != float('inf'):
                coinCounts[amount] = min(coinCounts[amount],
                                         coinCounts[amount - coin] + 1)

    return coinCounts[total] if coinCounts[total] != float('inf') else -1
