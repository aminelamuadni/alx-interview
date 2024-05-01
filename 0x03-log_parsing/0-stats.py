#!/usr/bin/python3
"""
Script to parse log data from standard input and compute metrics such as
total file size and HTTP status code occurrences, printing these metrics
every 10 lines or upon a keyboard interruption.
"""

import sys
import signal


def process_logs():
    """
    Processes logs from stdin, generating reports after every 10 lines and
    upon receiving a KeyboardInterrupt.
    """
    line_count = 0
    file_size = 0
    status_codes = {}
    valid_codes = {'200', '301', '400', '401', '403', '404', '405', '500'}

    def print_report():
        """
        Prints the cumulative file size and the count of each status code.
        """
        print(f"File size: {file_size}")
        for code in sorted(status_codes):
            if status_codes[code] > 0:
                print(f"{code}: {status_codes[code]}")

    try:
        for line in sys.stdin:
            parts = line.strip().split()
            if len(parts) >= 2 and parts[-2] in valid_codes:
                try:
                    size = int(parts[-1])
                    file_size += size
                    if parts[-2] in status_codes:
                        status_codes[parts[-2]] += 1
                    else:
                        status_codes[parts[-2]] = 1
                except ValueError:
                    continue
            line_count += 1
            if line_count == 10:
                print_report()
                line_count = 0
                file_size = 0
                status_codes.clear()
    except KeyboardInterrupt:
        print_report()
        sys.exit(0)


if __name__ == "__main__":
    process_logs()
