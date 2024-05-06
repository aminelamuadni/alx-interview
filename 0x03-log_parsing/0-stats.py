#!/usr/bin/python3
"""
Log Parsing Script

This script reads from stdin line by line, computes metrics, and prints
statistics every 10 lines or upon keyboard interruption (CTRL + C).
"""

import sys


def parse_logs():
    """
    Parse logs from stdin and compute metrics.

    Reads each line from stdin, parses the log line, and computes metrics
    based on the parsed data. Prints statistics every 10 lines or upon
    keyboard interruption (CTRL + C).
    """
    line_count = 0
    file_size = 0
    status_codes = {}
    valid_status_codes = ('200', '301', '400', '401', '403', '404', '405',
                          '500')
    try:
        for line in sys.stdin:
            line_count += 1
            line = line.split()
            try:
                file_size += int(line[-1])
                if line[-2] in valid_status_codes:
                    try:
                        status_codes[line[-2]] += 1
                    except KeyError:
                        status_codes[line[-2]] = 1
            except (IndexError, ValueError):
                pass
            if line_count == 10:
                print_stats(file_size, status_codes)
                line_count = 0
        print_stats(file_size, status_codes)
    except KeyboardInterrupt as e:
        print_stats(file_size, status_codes)
        raise


def print_stats(file_size, status_codes):
    """
    Print computed statistics.

    Args:
        file_size (int): Total file size.
        status_codes (dict): Dictionary containing counts of each status code.
    """
    print("File size: {}".format(file_size))
    for key, value in sorted(status_codes.items()):
        print("{}: {}".format(key, value))


if __name__ == '__main__':
    parse_logs()
