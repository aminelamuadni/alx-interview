#!/usr/bin/python3
"""
Script to parse log data from standard input and compute metrics such as
total file size and HTTP status code occurrences, printing these metrics
every 10 lines or upon a keyboard interruption.
"""

import sys


def process_logs():
    """
    Processes logs from stdin, generating reports after every 10 lines and
    upon receiving a KeyboardInterrupt.
    """
    line_count = 0
    file_size = 0
    status_valid_codes = {}
    valid_codes = ('200', '301', '400', '401', '403', '404', '405', '500')
    try:
        for line in sys.stdin:
            line_count += 1
            line = line.split()
            try:
                file_size += int(line[-1])
                if line[-2] in valid_codes:
                    try:
                        status_valid_codes[line[-2]] += 1
                    except KeyError:
                        status_valid_codes[line[-2]] = 1
            except (IndexError, ValueError):
                pass
            if line_count == 10:
                print_report(file_size, status_valid_codes)
                line_count = 0
        print_report(file_size, status_valid_codes)
    except KeyboardInterrupt as e:
        print_report(file_size, status_valid_codes)
        raise


def print_report(file_size, status_codes):
    """
    Prints the cumulative file size and the count of each status code.
    """
    print("File size: {}".format(file_size))
    for code in sorted(status_codes):
        print("{}: {}".format(code, status_codes[code]))


if __name__ == "__main__":
    process_logs()
