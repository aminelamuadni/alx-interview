#!/usr/bin/python3
"""
Log Parsing Script

This script reads stdin line by line, computes metrics, and prints statistics
every 10 lines or upon keyboard interruption (CTRL + C).

PEP 8 style guide (version 1.7.x) is followed.
"""

import sys
import signal
import re

# Define the regular expression pattern for log parsing
LOG_PATTERN = (
    r'(\S+) - \[(\d+\-\d+\-\d+ \d+:\d+:\d+\.\d+)\] '
    r'"(\S+ \S+ \S+)" (\d+) (\d+)'
)

# Initialize variables
total_size = 0
status_codes = {
    '200': 0, '301': 0, '400': 0, '401': 0,
    '403': 0, '404': 0, '405': 0, '500': 0
}


def parse_log_line(line):
    """
    Parse a log line and update metrics.

    Args:
        line (str): The log line to parse.
    """
    global total_size
    match = re.match(LOG_PATTERN, line)
    if match:
        status_code, file_size = match.group(4), int(match.group(5))
        total_size += file_size
        if status_code in status_codes:
            status_codes[status_code] += 1


def print_statistics():
    """Print the accumulated statistics."""
    print("File size: {}".format(total_size))
    for code in sorted(status_codes):
        count = status_codes[code]
        if count > 0:
            print("{}: {}".format(code, count))


def signal_handler(sig, frame):
    """Signal handler for keyboard interruption (CTRL + C)."""
    print_statistics()
    sys.exit(0)


def main():
    """Main function to run the log parsing script."""
    # Register the signal handler
    signal.signal(signal.SIGINT, signal_handler)

    # Read input from stdin line by line
    line_count = 0
    for line in sys.stdin:
        parse_log_line(line)
        line_count += 1
        if line_count % 10 == 0:
            print_statistics()

    # Print the final statistics
    print_statistics()


if __name__ == '__main__':
    main()
