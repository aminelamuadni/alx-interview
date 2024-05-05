#!/usr/bin/python3

"""This module reads from standard input and computes metrics."""

import sys
import signal


def print_stats(file_size, status_codes):
    """Prints calculated metrics in the required format."""
    print("File size:", file_size)
    for code in sorted(status_codes.keys()):
        print(code, ":", status_codes[code])


def signal_handler(sig, frame):
    """Handles keyboard interruption (CTRL + C)."""
    print_stats(file_size, status_codes)
    sys.exit(0)


if __name__ == "__main__":
    file_size = 0
    status_codes = {}
    line_count = 0

    signal.signal(signal.SIGINT, signal_handler)

    for line in sys.stdin:
        parts = line.split()
        if len(parts) != 10:
            continue

        try:
            status_code = int(parts[8])
            content_size = int(parts[9])
        except (ValueError, IndexError):
            continue

        if status_code in [200, 301, 400, 401, 403, 404, 405, 500]:
            file_size += content_size
            status_codes[status_code] = status_codes.get(status_code, 0) + 1

            line_count += 1
            if line_count % 10 == 0:
                print_stats(file_size, status_codes)

        else:
            continue

    print_stats(file_size, status_codes)
