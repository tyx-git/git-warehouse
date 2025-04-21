from datetime import datetime, timedelta
from collections import Counter, defaultdict
from typing import Dict, List, Any, Tuple
import numpy as np
from src.collector.storage.buffer import LogBuffer


class ApacheAnalyzer:
    def __init__(self, buffer: LogBuffer):
        self.buffer = buffer

    def get_request_stats(self, hours: int = 24) -> Dict[str, Any]:
        """Get request statistics for the specified time period"""
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=hours)
        logs = self.buffer.get_by_time_range(start_time, end_time)

        if not logs:
            return {}

        # Basic statistics
        total_requests = len(logs)
        unique_hosts = len(set(log['data']['remote_addr'] for log in logs))
        
        # Status code distribution
        status_codes = Counter(log['data']['status'] for log in logs)
        status_distribution = [
            {'status': status, 'count': count}
            for status, count in status_codes.most_common()
        ]

        # Request methods
        methods = Counter(log['data'].get('method', '') for log in logs)
        method_distribution = [
            {'method': method, 'count': count}
            for method, count in methods.most_common()
        ]

        # Top resources
        resources = Counter(log['data'].get('url', '') for log in logs)
        top_resources = [
            {'resource': resource, 'count': count}
            for resource, count in resources.most_common(10)
        ]

        # Response time statistics
        response_times = [
            log['data'].get('request_time', 0)
            for log in logs
            if log['data'].get('request_time') is not None
        ]
        avg_response_time = np.mean(response_times) if response_times else 0
        max_response_time = max(response_times) if response_times else 0
        min_response_time = min(response_times) if response_times else 0

        # Hourly request distribution
        hourly_requests = defaultdict(int)
        for log in logs:
            hour = log['timestamp'].hour
            hourly_requests[hour] += 1

        return {
            'total_requests': total_requests,
            'unique_hosts': unique_hosts,
            'status_distribution': status_distribution,
            'method_distribution': method_distribution,
            'top_resources': top_resources,
            'response_time': {
                'avg': avg_response_time,
                'max': max_response_time,
                'min': min_response_time
            },
            'hourly_distribution': [
                {'hour': hour, 'count': count}
                for hour, count in sorted(hourly_requests.items())
            ]
        }

    def detect_anomalies(self, threshold: float = 3.0) -> List[Dict[str, Any]]:
        """Detect anomalous patterns in the logs"""
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=24)
        logs = self.buffer.get_by_time_range(start_time, end_time)

        if not logs:
            return []

        anomalies = []

        # Check for unusual status codes
        status_codes = Counter(log['data']['status'] for log in logs)
        total_requests = len(logs)
        for status, count in status_codes.items():
            if status >= 500 and count / total_requests > 0.1:  # More than 10% errors
                anomalies.append({
                    'type': 'high_error_rate',
                    'status': status,
                    'count': count,
                    'percentage': count / total_requests * 100
                })

        # Check for unusual response times
        response_times = [
            log['data'].get('request_time', 0)
            for log in logs
            if log['data'].get('request_time') is not None
        ]
        if response_times:
            mean = np.mean(response_times)
            std = np.std(response_times)
            for log in logs:
                if log['data'].get('request_time', 0) > mean + threshold * std:
                    anomalies.append({
                        'type': 'slow_response',
                        'url': log['data'].get('url', ''),
                        'response_time': log['data'].get('request_time', 0),
                        'timestamp': log['timestamp']
                    })

        # Check for unusual request patterns
        hourly_requests = defaultdict(int)
        for log in logs:
            hour = log['timestamp'].hour
            hourly_requests[hour] += 1

        mean_requests = np.mean(list(hourly_requests.values()))
        std_requests = np.std(list(hourly_requests.values()))
        for hour, count in hourly_requests.items():
            if count > mean_requests + threshold * std_requests:
                anomalies.append({
                    'type': 'unusual_traffic',
                    'hour': hour,
                    'count': count,
                    'expected': mean_requests
                })

        return anomalies

    def get_traffic_trends(self, days: int = 7) -> Dict[str, List[Dict[str, Any]]]:
        """Get traffic trends over multiple days"""
        end_time = datetime.now()
        start_time = end_time - timedelta(days=days)
        
        daily_stats = []
        for day in range(days):
            day_start = start_time + timedelta(days=day)
            day_end = day_start + timedelta(days=1)
            day_logs = self.buffer.get_by_time_range(day_start, day_end)
            
            stats = {
                'date': day_start.date(),
                'total_requests': len(day_logs),
                'unique_hosts': len(set(log['data']['remote_addr'] for log in day_logs)),
                'error_rate': len([l for l in day_logs if l['data']['status'] >= 500]) / len(day_logs) if day_logs else 0
            }
            daily_stats.append(stats)

        return {'daily_stats': daily_stats}

    def get_user_agent_stats(self, hours: int = 24) -> Dict[str, Any]:
        """Get user agent statistics"""
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=hours)
        logs = self.buffer.get_by_time_range(start_time, end_time)

        if not logs:
            return {}

        # Categorize user agents
        browsers = Counter()
        os_systems = Counter()
        devices = Counter()
        bots = Counter()

        for log in logs:
            ua = log['data'].get('http_user_agent', '').lower()
            
            # Browser detection
            if 'chrome' in ua:
                browsers['Chrome'] += 1
            elif 'firefox' in ua:
                browsers['Firefox'] += 1
            elif 'safari' in ua and 'chrome' not in ua:
                browsers['Safari'] += 1
            elif 'edge' in ua:
                browsers['Edge'] += 1
            elif 'msie' in ua or 'trident' in ua:
                browsers['IE'] += 1
            
            # OS detection
            if 'windows' in ua:
                os_systems['Windows'] += 1
            elif 'mac' in ua:
                os_systems['MacOS'] += 1
            elif 'linux' in ua:
                os_systems['Linux'] += 1
            elif 'android' in ua:
                os_systems['Android'] += 1
            elif 'iphone' in ua or 'ipad' in ua:
                os_systems['iOS'] += 1
            
            # Device detection
            if 'mobile' in ua:
                devices['Mobile'] += 1
            elif 'tablet' in ua:
                devices['Tablet'] += 1
            else:
                devices['Desktop'] += 1
            
            # Bot detection
            if any(bot in ua for bot in ['bot', 'crawler', 'spider']):
                bots['Bot'] += 1
            else:
                bots['Human'] += 1

        return {
            'browsers': [{'name': k, 'count': v} for k, v in browsers.most_common()],
            'os_systems': [{'name': k, 'count': v} for k, v in os_systems.most_common()],
            'devices': [{'name': k, 'count': v} for k, v in devices.most_common()],
            'bot_vs_human': [{'type': k, 'count': v} for k, v in bots.most_common()]
        }