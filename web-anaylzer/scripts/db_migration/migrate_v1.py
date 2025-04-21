import mysql.connector
from datetime import datetime
from src.storage.connectors.mysql_conn import MySQLConnector


def migrate_v1():
    """Initial database migration"""
    conn = MySQLConnector().get_connection()
    cursor = conn.cursor()

    try:
        # Create Apache logs table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS apache_logs (
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
            INDEX idx_status (status),
            INDEX idx_host (host)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """)

        # Create Nginx logs table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS nginx_logs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            remote_addr VARCHAR(255),
            remote_user VARCHAR(255),
            timestamp DATETIME,
            request TEXT,
            status INT,
            body_bytes_sent INT,
            http_referer TEXT,
            http_user_agent TEXT,
            http_x_forwarded_for TEXT,
            request_time FLOAT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_timestamp (timestamp),
            INDEX idx_status (status),
            INDEX idx_remote_addr (remote_addr)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """)

        # Create statistics table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS analysis_results (
            id INT AUTO_INCREMENT PRIMARY KEY,
            analysis_type VARCHAR(255),
            time_period_start DATETIME,
            time_period_end DATETIME,
            metrics JSON,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_analysis_type (analysis_type),
            INDEX idx_time_period (time_period_start, time_period_end)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
        """)

        conn.commit()
        print("Database migration completed successfully.")
    except Exception as e:
        conn.rollback()
        print(f"Migration failed: {e}")
        raise
    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    migrate_v1()