#!/usr/bin/python3
"""
This script reads standard input line by line to parse log entries,
accumulates totals for file sizes and HTTP status codes, and prints these
statistics after every 10 lines or upon receiving a KeyboardInterrupt.
"""

import sys
import signal


def print_statistics(status_codes, total_size):
    """Prints the total file size and status code frequencies."""
    print(f"File size: {total_size}")
    for code, count in sorted(status_codes.items()):
        if count > 0:
            print(f"{code}: {count}")


def handle_interrupt(signal, frame):
    """Handles the SIGINT signal to print statistics before exiting."""
    print_statistics(status_codes, total_size)
    sys.exit(0)


# Prepare the environment
status_codes = {code: 0 for code in
                ["200", "301", "400", "401", "403", "404", "405", "500"]}
total_size = 0
line_count = 0

# Setup signal handler for graceful handling of KeyboardInterrupt
signal.signal(signal.SIGINT, handle_interrupt)

try:
    for line in sys.stdin:
        parts = line.strip().split()
        # Validate and parse line
        if len(parts) > 2 and parts[-2] in status_codes:
            try:
                size = int(parts[-1])
                total_size += size
                status_codes[parts[-2]] += 1
                line_count += 1
                if line_count == 10:
                    print_statistics(status_codes, total_size)
                    # Reset for next batch
                    line_count = 0
                    status_codes = {code: 0 for code in status_codes}
            except ValueError:
                # Ignore lines with invalid size input
                continue
finally:
    # Ensure final statistics are printed even if the loop exits unexpectedly
    print_statistics(status_codes, total_size)
