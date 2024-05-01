#!/usr/bin/python3

"""A script for parsing HTTP request logs."""

import re


def parse_log_entry(log_line):
    """Extracts sections of a line of an HTTP request log."""
    log_patterns = (
        r'\s*(?P<ip>\S+)\s*',
        r'\s*\[(?P<date>\d+\-\d+\-\d+ \d+:\d+:\d+\.\d+)\]',
        r'\s*"(?P<request>[^"]*)"',
        r'\s*(?P<status_code>\S+)',
        r'\s*(?P<file_size>\d+)'
    )
    log_format = '{}\\-{}{}{}{}\\s*'.format(log_patterns[0], log_patterns[1],
                                            log_patterns[2], log_patterns[3],
                                            log_patterns[4])
    log_match = re.fullmatch(log_format, log_line)
    if log_match is not None:
        entry_data = {
            'status_code': log_match.group('status_code'),
            'file_size': int(log_match.group('file_size')),
        }
        return entry_data


def display_stats(total_size, status_code_counts):
    """Prints the accumulated statistics of the HTTP request log."""
    print('File size: {:d}'.format(total_size), flush=True)
    for code in sorted(status_code_counts.keys()):
        count = status_code_counts.get(code, 0)
        if count > 0:
            print('{:s}: {:d}'.format(code, count), flush=True)


def process_metrics(log_line, total_size, status_code_counts):
    """Updates the metrics from a given HTTP request log.

    Args:
        log_line (str): The line of input from which to retrieve the metrics.

    Returns:
        int: The new total file size.
    """
    entry_data = parse_log_entry(log_line)
    code = entry_data.get('status_code', '0')
    if code in status_code_counts.keys():
        status_code_counts[code] += 1
    return total_size + entry_data['file_size']


def main():
    """Starts the log parser."""
    line_count = 0
    total_size = 0
    status_code_counts = {
        '200': 0,
        '301': 0,
        '400': 0,
        '401': 0,
        '403': 0,
        '404': 0,
        '405': 0,
        '500': 0,
    }
    try:
        while True:
            log_line = input()
            total_size = process_metrics(
                log_line,
                total_size,
                status_code_counts,
            )
            line_count += 1
            if line_count % 10 == 0:
                display_stats(total_size, status_code_counts)
    except (KeyboardInterrupt, EOFError):
        display_stats(total_size, status_code_counts)


if __name__ == '__main__':
    main()
