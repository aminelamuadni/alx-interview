#!/usr/bin/python3
"""Reads from stdin and computes metrics."""

import sys
import re
import signal

total_file_size = 0
status_code_counts = {}
valid_status_codes = {200, 301, 400, 401, 403, 404, 405, 500}
line_pattern = re.compile(
    r'(\S+) - \[(.*?)\] "GET /projects/260 HTTP/1\.1" (\d+) (\d+)'
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
        try:
            match = line_pattern.match(line)
            if match:
                line_count += 1
                status_code = int(match.group(3))
                file_size = int(match.group(4))

                # Update total file size
                total_file_size += file_size

                # Update status code count
                status_code_counts[status_code] = (
                    status_code_counts.get(status_code, 0) + 1
                )

                if line_count % 10 == 0:
                    print_metrics()
        except Exception:
            # Suppress all exceptions
            pass

except KeyboardInterrupt:
    print_metrics()
    sys.exit(0)

# Print final metrics if any lines were read
if line_count % 10 != 0 or line_count == 0:
    print_metrics()
