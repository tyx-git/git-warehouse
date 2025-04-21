from datetime import datetime
from src.storage.connectors.mysql_conn import MySQLConnector


class ApacheLog:
    def __init__(self):
        self.db = MySQLConnector()
        self.table = "apache_logs"

    def create_table(self):
        query = f"""
        CREATE TABLE IF NOT EXISTS {self.table} (
            id INT AUTO_INCREMENT PRIMARY KEY,
            host VARCHAR(255),
            user_ident VARCHAR(255),
            auth_user VARCHAR(255),
            timestamp DATETIME,
            request TEXT,
            status INT,
            bytes_sent INT,
            referrer TEXT,
            user_agent TEXT,
            processing_time FLOAT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_timestamp (timestamp),
            INDEX idx_status (status)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """
        self.db.execute_query(query)

    def insert_log(self, log_data):
        query = f"""
        INSERT INTO {self.table} (
            host, user_ident, auth_user, timestamp, 
            request, status, bytes_sent, 
            referrer, user_agent, processing_time
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = (
            log_data.get('host'),
            log_data.get('user_ident'),
            log_data.get('auth_user'),
            log_data.get('timestamp'),
            log_data.get('request'),
            log_data.get('status'),
            log_data.get('bytes_sent'),
            log_data.get('referrer'),
            log_data.get('user_agent'),
            log_data.get('processing_time')
        )
        return self.db.execute_query(query, params)

    def get_logs_by_time_range(self, start_time, end_time, limit=1000):
        query = f"""
        SELECT * FROM {self.table} 
        WHERE timestamp BETWEEN %s AND %s
        ORDER BY timestamp DESC
        LIMIT %s
        """
        return self.db.execute_query(query, (start_time, end_time, limit), fetch=True)
