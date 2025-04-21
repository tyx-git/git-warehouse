import re
from datetime import datetime
from typing import Dict, Any, Optional
import yaml
from pathlib import Path


class ApacheLogProcessor:
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or "config/log_patterns/apache.yaml"
        self.patterns = self._load_patterns()
        self.compiled_patterns = self._compile_patterns()

    def _load_patterns(self) -> Dict[str, Dict]:
        """Load log patterns from configuration file"""
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def _compile_patterns(self) -> Dict[str, re.Pattern]:
        """Compile regex patterns for each log format"""
        compiled = {}
        for format_name, config in self.patterns.items():
            # Convert Apache log format to regex pattern
            pattern = config['pattern']
            pattern = pattern.replace('%h', r'(?P<remote_addr>\S+)')
            pattern = pattern.replace('%l', r'(?P<remote_user>\S+)')
            pattern = pattern.replace('%u', r'(?P<user>\S+)')
            pattern = pattern.replace('%t', r'\[(?P<time_local>[^\]]+)\]')
            pattern = pattern.replace('%r', r'"(?P<request>[^"]*)"')
            pattern = pattern.replace('%>s', r'(?P<status>\d+)')
            pattern = pattern.replace('%b', r'(?P<body_bytes_sent>\d+|-)')
            pattern = pattern.replace('%{Referer}i', r'"(?P<http_referer>[^"]*)"')
            pattern = pattern.replace('%{User-Agent}i', r'"(?P<http_user_agent>[^"]*)"')
            pattern = pattern.replace('%D', r'(?P<request_time>\d+)')
            
            compiled[format_name] = re.compile(pattern)
        return compiled

    def _parse_datetime(self, time_str: str) -> datetime:
        """Parse Apache datetime format"""
        try:
            return datetime.strptime(time_str, "%d/%b/%Y:%H:%M:%S %z")
        except ValueError:
            # Try without timezone
            return datetime.strptime(time_str.split()[0], "%d/%b/%Y:%H:%M:%S")

    def _convert_field(self, field_name: str, value: str, field_type: str) -> Any:
        """Convert field value to appropriate type"""
        if value == '-':
            return None
        
        if field_type == 'string':
            return value
        elif field_type == 'integer':
            return int(value)
        elif field_type == 'float':
            return float(value)
        elif field_type == 'datetime':
            return self._parse_datetime(value)
        else:
            return value

    def process_line(self, line: str) -> Optional[Dict[str, Any]]:
        """Process a single log line"""
        for format_name, pattern in self.compiled_patterns.items():
            match = pattern.match(line)
            if match:
                result = {}
                fields = self.patterns[format_name]['fields']
                
                for field in fields:
                    field_name = field['name']
                    field_type = field['type']
                    value = match.group(field_name)
                    
                    if value is not None:
                        result[field_name] = self._convert_field(
                            field_name, value, field_type
                        )
                
                # Add additional derived fields
                if 'request' in result:
                    request_parts = result['request'].split()
                    if len(request_parts) >= 2:
                        result['method'] = request_parts[0]
                        result['url'] = request_parts[1]
                        result['protocol'] = request_parts[2] if len(request_parts) > 2 else None
                
                return result
        
        return None

    def validate_line(self, line: str) -> bool:
        """Validate if a line matches any of the patterns"""
        return any(pattern.match(line) for pattern in self.compiled_patterns.values())

    def get_supported_formats(self) -> list:
        """Get list of supported log formats"""
        return list(self.patterns.keys())
