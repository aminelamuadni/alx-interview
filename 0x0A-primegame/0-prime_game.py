#!/usr/bin/python3
"""
Module for the "Prime Game" where players Maria and Ben strategically remove
prime numbers and their multiples from a set of integers. The module calculates
the winner across multiple game rounds.
"""


def sieve_of_eratosthenes(max_n):
    """
    Generate list of primes up to max_n using the Sieve of Eratosthenes.
    """
    is_prime = [True] * (max_n + 1)
    for p in range(2, int(max_n ** 0.5) + 1):
        if is_prime[p]:
            for i in range(p * p, max_n + 1, p):
                is_prime[i] = False
    return [p for p in range(2, max_n + 1) if is_prime[p]]


def simulate_round(n, primes):
    """
    Simulate a single round of the game for given n using precomputed primes.
    """
    remaining_numbers = set(range(1, n + 1))
    turn = 0  # 0 for Maria, 1 for Ben
    while True:
        move_made = False
        for prime in primes:
            if prime in remaining_numbers:
                multiples = set(range(prime, n + 1, prime))
                remaining_numbers.difference_update(multiples)
                turn = 1 - turn
                move_made = True
                break
        if not move_made:
            break
    return "Maria" if turn == 1 else "Ben"


def isWinner(x, nums):
    """
    Determine the winner after x rounds with different values of n in nums.
    """
    max_n = max(nums)
    primes = sieve_of_eratosthenes(max_n)
    results = {"Maria": 0, "Ben": 0}
    for n in nums:
        winner = simulate_round(n, primes)
        results[winner] += 1

    if results["Maria"] > results["Ben"]:
        return "Maria"
    elif results["Ben"] > results["Maria"]:
        return "Ben"
    else:
        return None
