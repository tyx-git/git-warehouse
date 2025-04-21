import os
import json
from datetime import datetime
from jinja2 import Template, Environment
from pathlib import Path

class ReportGenerator:
    def __init__(self, analyzer):
        self.analyzer = analyzer
        self.template_dir = Path(__file__).parent / 'templates'
        
        # 创建Jinja2环境并添加tojson过滤器
        self.env = Environment()
        self.env.filters['tojson'] = json.dumps
    
    def generate_report(self, output_path, time_range='全部时间'):
        # 读取模板
        template_path = self.template_dir / 'report.html'
        with open(template_path, 'r', encoding='utf-8') as f:
            template = self.env.from_string(f.read())
        
        # 获取统计数据
        stats = self.analyzer.get_statistics()
        
        # 准备报告数据
        report_data = {
            'title': 'Web日志分析报告',
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'time_range': time_range,
            'stats': stats,
            'anomalies': self.analyzer.anomalies,
            'user_agent_stats': {
                'browsers': []  # 在这个简化版本中，我们不统计浏览器信息
            }
        }
        
        # 生成报告
        html_content = template.render(**report_data)
        
        # 确保输出目录存在
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # 保存报告
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)