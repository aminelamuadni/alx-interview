#!/usr/bin/python3
"""
Log Parsing Script

This script reads stdin line by line, computes metrics, and prints statistics
every 10 lines or upon keyboard interruption (CTRL + C).

PEP 8 style guide (version 1.7.x) is followed.
"""

import sys
import re


def parse_log_line(line):
    """
    Parses a log line and extracts relevant information.

    Args:
        line (str): The log line to parse.

    Returns:
        dict: A dictionary containing the extracted information.
    """
    log_pattern = (
        r'\s*(\S+)\s*',
        r'\s*\[(\d+\-\d+\-\d+ \d+:\d+:\d+\.\d+)\]',
        r'\s*"([^"]*)"',
        r'\s*(\S+)',
        r'\s*(\d+)'
    )
    log_format = '{}\\-{}{}{}{}\\s*'.format(*log_pattern)
    match = re.fullmatch(log_format, line)
    if match:
        return {
            'status_code': match.group(4),
            'file_size': int(match.group(5))
        }
    return None


def display_statistics(total_size, status_code_stats):
    """
    Displays the accumulated statistics.

    Args:
        total_size (int): The total file size.
        status_code_stats (dict): A dictionary of status code counts.
    """
    print('File size: {:d}'.format(total_size), flush=True)
    for code in sorted(status_code_stats):
        count = status_code_stats.get(code, 0)
        if count > 0:
            print('{:s}: {:d}'.format(code, count), flush=True)


def update_statistics(log_line, total_size, status_code_stats):
    """
    Updates the statistics based on the parsed log line.

    Args:
        log_line (str): The log line to process.
        total_size (int): The current total file size.
        status_code_stats (dict): A dictionary of status code counts.

    Returns:
        int: The updated total file size.
    """
    log_data = parse_log_line(log_line)
    if log_data:
        status_code = log_data['status_code']
        file_size = log_data['file_size']
        total_size += file_size
        if status_code in status_code_stats:
            status_code_stats[status_code] += 1
    return total_size


def run_log_parser():
    """
    Runs the log parsing script.
    """
    line_count = 0
    total_size = 0
    status_code_stats = {
        '200': 0, '301': 0, '400': 0, '401': 0,
        '403': 0, '404': 0, '405': 0, '500': 0
    }

    try:
        for log_line in sys.stdin:
            total_size = update_statistics(
                log_line, total_size, status_code_stats
            )
            line_count += 1
            if line_count % 10 == 0:
                display_statistics(total_size, status_code_stats)
    except (KeyboardInterrupt, EOFError):
        display_statistics(total_size, status_code_stats)


if __name__ == '__main__':
    run_log_parser()
