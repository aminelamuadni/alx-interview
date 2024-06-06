#!/usr/bin/python3
"""
This module contains a function makeChange which solves the coin change problem
using dynamic programming.
It aims to find the minimum number of coins needed to make a given total from a
list of coin denominations.
"""


def makeChange(coins, total):
    """
    Calculates the minimum number of coins needed to make change for a given
    total.

    Args:
        coins (list): A list of coin denominations available.
        total (int): The total amount for which change needs to be made.

    Returns:
        int: The minimum number of coins needed to make change for the given
             total.
             Returns -1 if it is not possible to make change for the given
             total.
    """
    if total <= 0:
        return 0
    dp = [float('inf')] * (total + 1)
    dp[0] = 0

    for coin in coins:
        for j in range(coin, total + 1):
            if dp[j - coin] != float('inf'):
                dp[j] = min(dp[j], dp[j - coin] + 1)

    return -1 if dp[total] == float('inf') else dp[total]
