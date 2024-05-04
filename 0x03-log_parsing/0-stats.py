#!/usr/bin/python3

"""
Log Parsing Script

This script reads stdin line by line, computes metrics, and prints statistics
every 10 lines or upon keyboard interruption (CTRL + C).

PEP 8 style guide (version 1.7.x) is followed.
"""

import sys
import re
import signal


def parse_log_entry(log_line):
    """
    Parses a log line and extracts relevant information.

    Args:
        log_line (str): The log line to parse.

    Returns:
        dict: A dictionary containing the parsed information.
    """
    log_format = (
        r'(\S+) - \[(\d+\-\d+\-\d+ \d+:\d+:\d+\.\d+)\] "(\S+ \S+ \S+)" '
        r'(\d+) (\d+)'
    )
    match = re.match(log_format, log_line)
    if match:
        return {
            'status_code': match.group(4),
            'file_size': int(match.group(5))
        }
    return None


def display_stats(total_size, status_code_counts):
    """
    Displays the accumulated statistics.

    Args:
        total_size (int): The total file size.
        status_code_counts (dict): A dictionary of status code counts.
    """
    print("File size: {}".format(total_size))
    for code in sorted(status_code_counts):
        count = status_code_counts[code]
        if count > 0:
            print("{}: {}".format(code, count))


def process_metrics(log_line, total_size, status_code_counts):
    """
    Processes the metrics based on the parsed log entry.

    Args:
        log_line (str): The log line to process.
        total_size (int): The current total file size.
        status_code_counts (dict): A dictionary of status code counts.

    Returns:
        int: The updated total file size.
    """
    entry = parse_log_entry(log_line)
    if entry:
        status_code = entry['status_code']
        file_size = entry['file_size']
        total_size += file_size
        if status_code in status_code_counts:
            status_code_counts[status_code] += 1
    return total_size


def main():
    """
    Main function to run the log parsing script.
    """
    total_size = 0
    status_code_counts = {
        '200': 0, '301': 0, '400': 0, '401': 0,
        '403': 0, '404': 0, '405': 0, '500': 0
    }
    line_count = 0

    def signal_handler(signal, frame):
        display_stats(total_size, status_code_counts)
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    try:
        for log_line in sys.stdin:
            total_size = process_metrics(
                log_line, total_size, status_code_counts
            )
            line_count += 1
            if line_count % 10 == 0:
                display_stats(total_size, status_code_counts)
    except KeyboardInterrupt:
        display_stats(total_size, status_code_counts)


if __name__ == '__main__':
    main()
