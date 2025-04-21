import re
from datetime import datetime
from typing import Dict


class ApacheLogParser:
    def __init__(self):
        # Common Log Format (CLF)
        self.clf_pattern = re.compile(
            r'(?P<host>\S+) (?P<user_ident>\S+) (?P<auth_user>\S+) \[(?P<timestamp>.*?)\] '
            r'"(?P<request>.*?)" (?P<status>\d+) (?P<bytes_sent>\S+)'
        )

        # Combined Log Format
        self.combined_pattern = re.compile(
            r'(?P<host>\S+) (?P<user_ident>\S+) (?P<auth_user>\S+) \[(?P<timestamp>.*?)\] '
            r'"(?P<request>.*?)" (?P<status>\d+) (?P<bytes_sent>\S+) '
            r'"(?P<referrer>.*?)" "(?P<user_agent>.*?)"'
        )

        # Extended Log Format with processing time
        self.extended_pattern = re.compile(
            r'(?P<host>\S+) (?P<user_ident>\S+) (?P<auth_user>\S+) \[(?P<timestamp>.*?)\] '
            r'"(?P<request>.*?)" (?P<status>\d+) (?P<bytes_sent>\S+) '
            r'"(?P<referrer>.*?)" "(?P<user_agent>.*?)" '
            r'(?P<processing_time>\S+)'
        )

    def parse(self, log_line: str) -> Dict:
        """Parse Apache log line into structured data"""
        match = self.extended_pattern.match(log_line) or \
                self.combined_pattern.match(log_line) or \
                self.clf_pattern.match(log_line)

        if not match:
            raise ValueError("Log line doesn't match any known Apache format")

        log_data = match.groupdict()

        # Clean and convert fields
        log_data['timestamp'] = self._parse_apache_timestamp(log_data['timestamp'])
        log_data['status'] = int(log_data['status'])
        log_data['bytes_sent'] = 0 if log_data['bytes_sent'] == '-' else int(log_data['bytes_sent'])
        log_data['processing_time'] = float(log_data.get('processing_time', 0))

        return log_data

    def _parse_apache_timestamp(self, timestamp_str: str) -> datetime:
        """Convert Apache timestamp to datetime object"""
        # Example: 10/Oct/2023:13:55:36 +0000
        try:
            return datetime.strptime(timestamp_str, "%d/%b/%Y:%H:%M:%S %z")
        except ValueError:
            # Fallback for formats without timezone
            return datetime.strptime(timestamp_str.split()[0], "%d/%b/%Y:%H:%M:%S")