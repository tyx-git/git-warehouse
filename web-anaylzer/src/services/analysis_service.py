from datetime import datetime, timedelta
from src.analyzer.apache_analyzer import ApacheAnalyzer
from src.storage.models.analysis_result import AnalysisResult


class AnalysisService:
    def __init__(self):
        self.apache_analyzer = ApacheAnalyzer()
        self.result_storage = AnalysisResult()

    def run_daily_analysis(self):
        """Run daily analysis and store results"""
        end_time = datetime.now()
        start_time = end_time - timedelta(days=1)

        # Run Apache analysis
        apache_stats = self.apache_analyzer.get_request_stats(24)
        anomaly_results = self.apache_analyzer.detect_anomalies()

        # Store results
        self.result_storage.save_result(
            analysis_type="daily_apache",
            time_period_start=start_time,
            time_period_end=end_time,
            metrics={
                "request_stats": apache_stats,
                "anomalies": anomaly_results
            }
        )

        return {
            "apache": apache_stats,
            "anomalies": anomaly_results
        }

    def get_recent_analysis(self, limit=5):
        """Get recent analysis results"""
        return self.result_storage.get_recent_results(limit)