#!/usr/bin/python3
"""
This script continuously reads from standard input, parsing formatted log
entries. It tracks and aggregates the total size of logged data and counts
occurrences of HTTP status codes. After every 10 lines or upon receiving a
SIGINT (Ctrl + C), it prints these statistics.
"""

import sys
import re
import signal

# Compile a regex pattern to match the expected format of log entries.
log_pattern = re.compile(
    r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - \[(.*?)\] "GET /projects/260 '
    r'HTTP/1\.1" (\d{3}) (\d+)'
)

# Initialize variables to store the total size and count of status codes.
total_size = 0
status_codes = {}


def parse_log_line(line):
    """Parse a log line to extract data if it matches the expected format."""
    match = log_pattern.match(line)
    if match:
        return match.groups()
    return None


def process(line):
    """Process a log entry to update total file size and status code counts."""
    global total_size
    data = parse_log_line(line)
    if data:
        ip, date, status, size = data
        total_size += int(size)
        if status in status_codes:
            status_codes[status] += 1
        else:
            status_codes[status] = 1


def print_statistics():
    """Prints aggregated statistics for file size and status codes."""
    print(f"File size: {total_size}")
    for status in sorted(status_codes.keys()):
        print(f"{status}: {status_codes[status]}")


def signal_handler(sig, frame):
    """Handle SIGINT to print statistics before terminating the program."""
    print_statistics()
    sys.exit(0)


# Set signal handler for SIGINT to ensure stats are printed on interruption.
signal.signal(signal.SIGINT, signal_handler)
