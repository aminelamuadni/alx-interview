#!/usr/bin/python3
"""
Script that reads log data from standard input, parses each line to extract
metrics, and prints a summary every 10 lines or upon a keyboard interruption.
"""

import sys
import re
import signal

# Compile a regex pattern to match the expected log format exactly.
log_pattern = re.compile(
    r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - \[(.*?)\] "GET /projects/260 '
    r'HTTP/1\.1" (\d{3}) (\d+)'
)

# Valid status codes as a set for quick lookup.
valid_codes = {'200', '301', '400', '401', '403', '404', '405', '500'}

# Variables to hold the total size of files and count of status codes.
total_size = 0
status_counts = {}


def handle_line(line):
    global total_size
    match = log_pattern.match(line)
    if match:
        ip, status, size = match.groups()
        if status in valid_codes:
            total_size += int(size)
            if status in status_counts:
                status_counts[status] += 1
            else:
                status_counts[status] = 1


def print_statistics():
    print(f"File size: {total_size}")
    for code in sorted(status_counts.keys()):
        print(f"{code}: {status_counts[code]}")


def signal_handler(signum, frame):
    print_statistics()
    sys.exit(0)


def main():
    signal.signal(signal.SIGINT, signal_handler)
    line_count = 0
    try:
        for line in sys.stdin:
            handle_line(line)
            line_count += 1
            if line_count == 10:
                print_statistics()
                status_counts.clear()
                line_count = 0
    except KeyboardInterrupt:
        print_statistics()


if __name__ == "__main__":
    main()
