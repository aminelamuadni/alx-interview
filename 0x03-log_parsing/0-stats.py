#!/usr/bin/python3
"""Reads from stdin and computes metrics."""

import sys
import re
import signal

total_file_size = 0
status_code_counts = {
    200: 0, 301: 0, 400: 0, 401: 0,
    403: 0, 404: 0, 405: 0, 500: 0
}
line_pattern = re.compile(
    r'^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}) - \['
    r'(.*?)\] "GET \/projects\/260 HTTP\/1\.1" (\d{3}) (\d+)$'
)
line_count = 0


def print_metrics():
    """Print metrics based on current counts."""
    print(f"File size: {total_file_size}")
    for code in sorted(status_code_counts):
        if status_code_counts[code] > 0:
            print(f"{code}: {status_code_counts[code]}")


def signal_handler(sig, frame):
    """Handle CTRL+C signal."""
    print_metrics()
    sys.exit(0)


signal.signal(signal.SIGINT, signal_handler)

try:
    for line in sys.stdin:
        match = line_pattern.match(line)
        if match:
            try:
                status_code = int(match.group(3))
                file_size = int(match.group(4))

                if status_code in status_code_counts:
                    total_file_size += file_size
                    status_code_counts[status_code] += 1
                    line_count += 1

            except ValueError:
                pass

            if line_count % 10 == 0:
                print_metrics()
                line_count = 0

except KeyboardInterrupt:
    print_metrics()
    sys.exit(0)

# Print final metrics if any lines were read
if line_count % 10 != 0 or line_count == 0:
    print_metrics()
