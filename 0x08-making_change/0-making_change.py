#!/usr/bin/python3
"""
This Python script determines the fewest number of coins required to meet a
specified total.
It uses a greedy algorithm tailored to coin denominations typically designed to
provide optimal solutions.
"""


def makeChange(coins, total):
    """
    Determine the minimum number of coins needed to achieve a given total using
    a greedy approach.

    Parameters:
    coins (list of int): Denominations of coins available for making change.
    total (int): The total amount of money for which change is to be made.

    Returns:
    int: The fewest number of coins needed to make up the given total. If it is
         not possible to make the exact total with the given denominations, the
         function returns -1.
    """
    if total <= 0:
        return 0
    if not coins:
        return -1

    coins.sort(reverse=True)
    num_coins = 0
    current_total = 0

    for coin in coins:
        while current_total + coin <= total:
            current_total += coin
            num_coins += 1
        if current_total == total:
            return num_coins

    return -1
