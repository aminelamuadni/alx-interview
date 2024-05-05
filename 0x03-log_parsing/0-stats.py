#!/usr/bin/python3
"""
This script reads from standard input (stdin) line by line, computes metrics
based on log entries, and outputs statistics every 10 lines or upon a keyboard
interruption (CTRL + C).
"""

import sys


if __name__ == '__main__':

    total_file_size, line_counter = 0, 0
    valid_codes = ["200", "301", "400", "401", "403", "404", "405", "500"]
    status_counts = {code: 0 for code in valid_codes}

    def display_stats(status_counts: dict, total_file_size: int) -> None:
        """
        Prints the accumulated statistics of file sizes and status code
        occurrences.

        Args:
            status_counts (dict): A dictionary holding counts of status codes.
            total_file_size (int): The total size of processed files.
        """
        print("File size: {:d}".format(total_file_size))
        for code, count in sorted(status_counts.items()):
            if count > 0:
                print("{}: {}".format(code, count))

    try:
        for line in sys.stdin:
            line_counter += 1
            parts = line.split()
            try:
                status_code = parts[-2]
                if status_code in status_counts:
                    status_counts[status_code] += 1
            except IndexError:
                pass  # In case the line is not in the expected format
            try:
                total_file_size += int(parts[-1])
            except (IndexError, ValueError):
                pass  # In case the file size is missing or non-numeric

            if line_counter % 10 == 0:
                display_stats(status_counts, total_file_size)
        display_stats(status_counts, total_file_size)
    except KeyboardInterrupt:
        display_stats(status_counts, total_file_size)
        raise
