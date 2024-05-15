#!/usr/bin/python3
import sys

"""
This module solves the N Queens problem using a backtracking algorithm. It
takes a single command-line argument, the size of the board N, where N must be
an integer greater than or equal to 4, and prints all possible arrangements of
N queens on an N x N chessboard where no two queens threaten each other.
"""


def print_usage_and_exit():
    """
    Prints the usage of the script and exits. This function is called when
    there is an error with command-line arguments.
    """
    print("Usage: nqueens N")
    sys.exit(1)


def is_valid_position(board, row, col):
    """
    Checks if it's safe to place a queen at board[row][col]. This function
    verifies that no other queens are placed in the same column or diagonal.

    :param board: list, current positions of queens on the board
    :param row: int, row index where the queen is being placed
    :param col: int, column index where the queen is being placed
    :return: bool, True if safe, False otherwise
    """
    for i in range(row):
        if (board[i] == col or
           board[i] - i == col - row or
           board[i] + i == col + row):
            return False
    return True


def solve_nqueens(n, row, board, solutions):
    """
    Recursively attempts to place queens on the board and records all solutions
    where queens do not threaten each other.

    :param n: int, the size of the chessboard and number of queens
    :param row: int, current row to try placing a queen
    :param board: list, current positions of queens on the board
    :param solutions: list, list to hold all of the board configurations that
    solve the problem
    """
    if row == n:
        solutions.append([[i, board[i]] for i in range(n)])
        return

    for col in range(n):
        if is_valid_position(board, row, col):
            board[row] = col
            solve_nqueens(n, row + 1, board, solutions)
            board[row] = -1  # Backtrack


def main():
    """
    Main function to handle command-line inputs and trigger the backtracking
    solution process.
    """
    if len(sys.argv) != 2:
        print_usage_and_exit()

    try:
        n = int(sys.argv[1])
    except ValueError:
        print("N must be a number")
        sys.exit(1)

    if n < 4:
        print("N must be at least 4")
        sys.exit(1)

    board = [-1] * n
    solutions = []
    solve_nqueens(n, 0, board, solutions)

    for solution in solutions:
        print(solution)


if __name__ == "__main__":
    main()
