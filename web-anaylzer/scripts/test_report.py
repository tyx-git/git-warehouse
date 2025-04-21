import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.analyzer.log_analyzer import LogAnalyzer
from src.analyzer.report_generator import ReportGenerator

def test_report_generation():
    # 创建日志分析器
    analyzer = LogAnalyzer()
    
    # 添加一些测试数据，包含不同的时间点
    test_logs = [
        '127.0.0.1 - - [01/Jan/2024:00:00:01 +0000] "GET / HTTP/1.1" 200 1234',
        '127.0.0.1 - - [01/Jan/2024:00:00:02 +0000] "GET /about HTTP/1.1" 200 2345',
        '127.0.0.2 - - [01/Jan/2024:00:00:03 +0000] "GET /contact HTTP/1.1" 404 123',
        '127.0.0.1 - - [01/Jan/2024:00:00:04 +0000] "GET / HTTP/1.1" 200 1234',
        '127.0.0.3 - - [01/Jan/2024:00:00:05 +0000] "GET / HTTP/1.1" 500 1234',
        '127.0.0.1 - - [01/Jan/2024:00:01:00 +0000] "GET / HTTP/1.1" 200 1234',
        '127.0.0.2 - - [01/Jan/2024:00:02:00 +0000] "GET /about HTTP/1.1" 200 2345',
        '127.0.0.3 - - [01/Jan/2024:00:03:00 +0000] "GET /contact HTTP/1.1" 404 123',
        '127.0.0.1 - - [01/Jan/2024:00:04:00 +0000] "GET / HTTP/1.1" 200 1234',
        '127.0.0.2 - - [01/Jan/2024:00:05:00 +0000] "GET / HTTP/1.1" 500 1234',
    ]
    
    for log in test_logs:
        analyzer.process_log(log)
    
    # 创建报告生成器
    report_generator = ReportGenerator(analyzer)
    
    # 确保输出目录存在
    output_dir = project_root / 'var' / 'reports'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # 生成报告
    output_path = output_dir / 'test_report.html'
    report_generator.generate_report(
        output_path=str(output_path),
        time_range='测试时间范围'
    )
    
    print(f'测试报告已生成：{output_path}')
    print('请打开生成的HTML文件查看报告内容')

if __name__ == '__main__':
    test_report_generation() 