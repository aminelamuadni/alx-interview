#!/usr/bin/python3
"""
Log Parsing Script

This script reads stdin line by line, computes metrics, and prints statistics
every 10 lines or upon keyboard interruption (CTRL + C).

PEP 8 style guide (version 1.7.x) is followed.
"""

import sys
import re


def extract_input(line):
    """
    Extracts sections of a line of an HTTP request log.

    Args:
        line (str): The log line to extract information from.

    Returns:
        dict: A dictionary containing the extracted information.
    """
    pattern = (
        r'(\S+) - \[(\d+\-\d+\-\d+ \d+:\d+:\d+\.\d+)\] "(\S+ \S+ \S+)" '
        r'(\d+) (\d+)'
    )
    match = re.match(pattern, line)
    if match:
        return {
            'status_code': match.group(4),
            'file_size': int(match.group(5))
        }
    return None


def print_statistics(total_size, status_codes):
    """
    Prints the accumulated statistics.

    Args:
        total_size (int): The total file size.
        status_codes (dict): A dictionary of status code counts.
    """
    print("File size: {}".format(total_size))
    for code in sorted(status_codes):
        count = status_codes[code]
        if count > 0:
            print("{}: {}".format(code, count))


def update_metrics(line, total_size, status_codes):
    """
    Updates the metrics based on the extracted information from a log line.

    Args:
        line (str): The log line to update metrics from.
        total_size (int): The current total file size.
        status_codes (dict): A dictionary of status code counts.

    Returns:
        int: The updated total file size.
    """
    info = extract_input(line)
    if info:
        status_code = info['status_code']
        file_size = info['file_size']
        total_size += file_size
        if status_code in status_codes:
            status_codes[status_code] += 1
    return total_size


def run():
    """
    Runs the log parsing script.
    """
    total_size = 0
    status_codes = {
        '200': 0, '301': 0, '400': 0, '401': 0,
        '403': 0, '404': 0, '405': 0, '500': 0
    }
    line_count = 0

    try:
        for line in sys.stdin:
            total_size = update_metrics(line, total_size, status_codes)
            line_count += 1
            if line_count % 10 == 0:
                print_statistics(total_size, status_codes)
    except KeyboardInterrupt:
        print_statistics(total_size, status_codes)


if __name__ == '__main__':
    run()
