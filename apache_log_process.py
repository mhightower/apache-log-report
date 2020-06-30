#!/usr/bin/env python3

import getopt
import os
import sys
import re
from time import process_time
from statistics import mean

PYTHON_MIN_VERSION = 3, 6
APACHE_COMBINED = '%h %l %u %t "%r" %>s %b "%{Referer}i" "%{User-agent}i"'
APACHE_COMBINED_PLUS = APACHE_COMBINED + '%D'
APACHE_COMBINED_PLUS_PATTERN = r'^(?P<client>\S+) (?P<remote_user>\S+) (?P<auth_remote_user>\S+) \[(?P<datetime>\S+ \S+)\] "(?P<method>\S+) (?P<request>\S+) (?P<version>\S+)" (?P<status>\S+) (?P<size_response_in_bytes>\S+) "(?P<referer>\S+)" "(?P<user_agent>.*)" (?P<request_time_in_ms>\S+)'
COMMAND_HELP = f'{sys.argv[0]} <log_file>'


def argument_check(argv):
    """
    Check for proper arguments\n
    Added standard help options for users without access to documentation.\n
    """
    try:
        opts, args = getopt.getopt(argv, "?hi:", ["input=", "help="])
        if len(args) == 0:
            raise getopt.GetoptError('Missing Apache log file')
    except getopt.GetoptError:
        sys.stderr.write(f'{COMMAND_HELP}\n')
        sys.exit(os.EX_NOINPUT)
    for opt, _ in opts:
        if opt in ['-h', '-?', '--help']:
            sys.stderr.write(f'{COMMAND_HELP}\n')
            sys.exit(os.EX_USAGE)


def formatted_output(
    lines_parsed,
    duration_of_log,
    requested_pages,
    most_frequent_visitor,
    min_load_time,
    avg_page_load,
    max_load_time,
    error_count,
    total_data
):
    """
    Print results with definitions in proper sequence
    """
    print('Number of lines parsed:', lines_parsed)
    print('Duration of log file:', duration_of_log)
    print('')
    print('Most requested page:', requested_pages)
    print('Most frequent visitor:', most_frequent_visitor)
    print('')
    print('Min page load time:', min_load_time)
    print('Average page load time:', avg_page_load)
    print('Max page load time:', max_load_time)
    print('')
    print('Number of errors:', error_count)
    print('Total data transferred:', total_data)


def file_access_check(file_path):
    """
    Check access to file\n
    WARNING: Exits by default\n
    """
    if not os.access(file_path, os.R_OK):
        sys.stderr.write(f'{file_path} file not found\n')
        sys.exit(os.EX_NOINPUT)
    return True


def process_apache_line(line, apache_pattern):
    """
    Process Apache line based on given regex pattern
    """
    try:
        rtn = apache_pattern.match(line).groupdict()
    except AttributeError:
        rtn = {}
    return rtn


def response_data_size(response_data_size: str):
    """
    Handles response size 0 bytes showing up as - string \n
    http://httpd.apache.org/docs/current/mod/mod_log_config.html#formats
    """
    return response_data_size if response_data_size.isnumeric() else '0'


def main(argv):
    """
    Main Apache Log Report function
    """

    # Sanity Check
    if not sys.version_info >= (PYTHON_MIN_VERSION):
        sys.stderr.write('Invalid Python version. Please use Python >= 3.6\n')
        sys.exit(os.EX_UNAVAILABLE)
    argument_check(argv)
    apache_log_file = argv[0]
    file_access_check(apache_log_file)

    # Process log file

    log_line_count = 0
    total_response_data_size = 0
    requested_pages = {}
    visitors = {}
    page_load_time_in_ms = []
    request_status_ok = ['200', '201', '202', '204']
    request_errors = 0

    start_process = process_time()
    apache_re_pattern = re.compile(APACHE_COMBINED_PLUS_PATTERN)
    with open(apache_log_file, 'r') as apache_log:
        for line in apache_log:
            line_output = process_apache_line(line, apache_re_pattern)

            # Sanity check for empty lines
            if len(line_output) == 0:
                sys.stderr.writelines('Missing line in log')
                continue

            # Total response data process
            total_response_data_size += int(
                response_data_size(
                    line_output['size_response_in_bytes']
                    )
                )

            # Request page process
            if line_output['request'] in requested_pages.keys():
                requested_pages[line_output['request']] += 1
            else:
                requested_pages[line_output['request']] = 1

            # Frequent Visitor process
            if line_output['client'] in visitors.keys():
                visitors[line_output['client']] += 1
            else:
                visitors[line_output['client']] = 1

            # Page Load store
            page_load_time_in_ms.append(int(line_output['request_time_in_ms']))

            # Errors
            if not line_output['status'] in request_status_ok:
                request_errors += 1

            log_line_count += 1

    stop_process = process_time()
    formatted_output(
        log_line_count,
        stop_process - start_process,
        max(requested_pages, key=requested_pages.get),
        max(visitors, key=visitors.get),
        min(page_load_time_in_ms),
        mean(page_load_time_in_ms),
        max(page_load_time_in_ms),
        request_errors,
        total_response_data_size
        )
    sys.exit(os.EX_OK)


if __name__ == "__main__":
    main(sys.argv[1:])
