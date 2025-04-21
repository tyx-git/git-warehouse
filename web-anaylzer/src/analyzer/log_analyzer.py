import re
from datetime import datetime
from collections import defaultdict
from user_agents import parse

class LogAnalyzer:
    def __init__(self):
        self.total_requests = 0
        self.unique_hosts = set()
        self.response_times = []
        self.status_codes = defaultdict(int)
        self.user_agents = defaultdict(int)
        self.anomalies = []
        self.time_series = defaultdict(int)  # 用于存储时间序列数据
        
        # 用于解析Apache/Nginx日志的正则表达式
        self.log_pattern = re.compile(
            r'(?P<host>[\d\.]+) - - \[(?P<time>.*?)\] "(?P<request>.*?)" (?P<status>\d+) (?P<bytes>\d+)'
        )
    
    def process_log(self, log_line):
        match = self.log_pattern.match(log_line)
        if not match:
            return
            
        data = match.groupdict()
        
        # 更新基本统计信息
        self.total_requests += 1
        self.unique_hosts.add(data['host'])
        
        # 更新状态码统计
        status_code = int(data['status'])
        self.status_codes[status_code] += 1
        
        # 更新时间序列数据
        try:
            log_time = datetime.strptime(data['time'], '%d/%b/%Y:%H:%M:%S %z')
            time_key = log_time.strftime('%Y-%m-%d %H:%M')
            self.time_series[time_key] += 1
        except ValueError:
            pass
        
        # 检测异常
        if status_code >= 500:
            self.anomalies.append({
                'type': '服务器错误',
                'description': f'状态码 {status_code}',
                'timestamp': data['time']
            })
    
    def get_statistics(self):
        """获取统计信息"""
        total_requests = self.total_requests
        status_distribution = [
            {
                'status': status,
                'count': count,
                'percentage': (count / total_requests * 100) if total_requests > 0 else 0
            }
            for status, count in self.status_codes.items()
        ]
        
        # 准备时间序列数据
        time_series_data = [
            {
                'time': time,
                'count': count
            }
            for time, count in sorted(self.time_series.items())
        ]
        
        return {
            'total_requests': total_requests,
            'unique_hosts': len(self.unique_hosts),
            'avg_response_time': 0,  # 在这个简化版本中，我们不计算响应时间
            'status_distribution': status_distribution,
            'time_series': time_series_data
        } 