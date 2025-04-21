from src.storage.connectors.mysql_conn import MySQLConnector


class AnalysisResult:
    def __init__(self):
        self.db = MySQLConnector()
        self.table = "analysis_results"

    def save_result(self, analysis_type, time_period_start, time_period_end, metrics):
        """Save analysis results to database"""
        query = f"""
        INSERT INTO {self.table} (
            analysis_type, time_period_start, time_period_end, metrics
        ) VALUES (%s, %s, %s, %s)
        """
        return self.db.execute_query(
            query,
            (analysis_type, time_period_start, time_period_end, metrics)
        )

    def get_recent_results(self, limit=5):
        """Get recent analysis results"""
        query = f"""
        SELECT * FROM {self.table}
        ORDER BY created_at DESC
        LIMIT %s
        """
        return self.db.execute_query(query, (limit,), fetch=True)