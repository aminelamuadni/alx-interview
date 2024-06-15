#!/usr/bin/python3
"""
This module implements a game between Maria and Ben where they remove prime
numbers and their multiples from a set of consecutive integers starting from 1
up to n. The player unable to make a move loses. The game is played across
multiple rounds with varying values of n, and the overall winner is the one who
wins the most rounds.
"""


def sieve_of_eratosthenes(max_n):
    """
    Generate list of primes up to max_n using the Sieve of Eratosthenes.
    """
    if max_n < 2:
        return []
    sieve = [True] * (max_n + 1)
    sieve[0] = sieve[1] = False
    for start in range(2, int(max_n ** 0.5) + 1):
        if sieve[start]:
            for i in range(start * start, max_n + 1, start):
                sieve[i] = False
    return [index for index, prime in enumerate(sieve) if prime]


def game_winner(n, primes):
    """
    Determine the winner of a single round given n and the list of primes.
    """
    remaining_primes = [p for p in primes if p <= n]
    return "Maria" if len(remaining_primes) % 2 == 1 else "Ben"


def isWinner(x, nums):
    """
    Determine who wins the most games after x rounds with different n values.
    """
    if x <= 0 or not nums or x != len(nums):
        return None

    max_n = max(nums)
    primes = sieve_of_eratosthenes(max_n)
    scores = {"Maria": 0, "Ben": 0}

    for n in nums:
        winner = game_winner(n, primes)
        scores[winner] += 1

    if scores["Maria"] > scores["Ben"]:
        return "Maria"
    elif scores["Ben"] > scores["Maria"]:
        return "Ben"
    return None
