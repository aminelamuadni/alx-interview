#!/usr/bin/python3
"""
This module provides a function to compute the minimum operations
required to reach exactly n 'H' characters in a text file using
'Copy All' and 'Paste' operations.
"""


def minOperations(n):
    if n <= 1:
        return 0

    operations = 0
    factor = 2

    while n > 1:
        while n % factor == 0:
            operations += factor
            n //= factor
        factor += 1
        if factor * factor > n and n > 1:
            operations += n
            break

    return operations
