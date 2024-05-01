#!/usr/bin/python3
"""
Script to parse log data from standard input and compute metrics such as
total file size and HTTP status code occurrences, printing these metrics
every 10 lines or upon a keyboard interruption.
"""


def process_logs():
    """
    Processes logs from stdin, generating reports after every 10 lines and
    upon receiving a KeyboardInterrupt.
    """
    stdin = __import__('sys').stdin
    line_count = 0
    file_size = 0
    status_codes = {}
    valid_codes = {'200', '301', '400', '401', '403', '404', '405', '500'}

    try:
        for line in stdin:
            parts = line.split()
            try:
                if parts[-2] in valid_codes:
                    file_size += int(parts[-1])
                    if parts[-2] in status_codes:
                        status_codes[parts[-2]] += 1
                    else:
                        status_codes[parts[-2]] = 1
            except (IndexError, ValueError):
                continue
            line_count += 1
            if line_count == 10:
                print_report(file_size, status_codes)
                line_count = 0
        print_report(file_size, status_codes)
    except KeyboardInterrupt:
        print_report(file_size, status_codes)
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
