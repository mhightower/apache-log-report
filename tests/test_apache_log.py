import apache_log_process
import re


def test_file_access():
    assert apache_log_process.file_access_check("data/log_file_small")


def test_output():
    apache_log_process.formatted_output(1, 2, 3, 4, 5, 6, 7, 8, 9)


APACHE_COMBINED_PLUS_LOG_LINE = '175.205.95.170 - - [18/Apr/2017:15:04:36 -0500] "GET /kms//wscore/check/json/ HTTP/1.0" 200 5035 "https://app.wellspring.com/kms/querybuilder/results/csv/" "Mozilla/5.0 (Macintosh; PPC Mac OS X 10_5_2; rv:1.9.2.20) Gecko/2011-08-07 23:25:19 Firefox/13.0" 2358'
APACHE_PROCESS_RESULT = {
    "client": "175.205.95.170",
    "remote_user": "-",
    "auth_remote_user": "-",
    "datetime": "18/Apr/2017:15:04:36 -0500",
    "method": "GET",
    "request": "/kms//wscore/check/json/",
    "version": "HTTP/1.0",
    "status": "200",
    "size_response_in_bytes": "5035",
    "referer": "https://app.wellspring.com/kms/querybuilder/results/csv/",
    "user_agent": "Mozilla/5.0 (Macintosh; PPC Mac OS X 10_5_2; rv:1.9.2.20) Gecko/2011-08-07 23:25:19 Firefox/13.0",
    "request_time_in_ms": "2358",
}
APACHE_COMMON_LOG_LINE = '127.0.0.1 - frank [10/Oct/2000:13:55:36 -0700] "GET /apache_pb.gif HTTP/1.0" 200 2326'


def test_process_apache_line():
    assert (
        apache_log_process.process_apache_line(
            APACHE_COMBINED_PLUS_LOG_LINE,
            re.compile(apache_log_process.APACHE_COMBINED_PLUS_PATTERN),
        )
        == APACHE_PROCESS_RESULT
    )
    assert (
        apache_log_process.process_apache_line(
            APACHE_COMMON_LOG_LINE,
            re.compile(apache_log_process.APACHE_COMBINED_PLUS_PATTERN),
        )
        == {}
    )


def test_fail_processing_apache_line():
    assert (
        apache_log_process.process_apache_line(
            APACHE_COMMON_LOG_LINE,
            re.compile(apache_log_process.APACHE_COMBINED_PLUS_PATTERN),
        )
        == {}
    )


APACHE_LOG_RESPONSE_0_BYTES = "-"
APACHE_LOG_RESPONSE_20_BYTES = "20"


def test_response_data_size():
    assert apache_log_process.response_data_size(
        APACHE_LOG_RESPONSE_0_BYTES
        ) == "0"
    assert apache_log_process.response_data_size(
        APACHE_LOG_RESPONSE_20_BYTES
        ) == "20"
