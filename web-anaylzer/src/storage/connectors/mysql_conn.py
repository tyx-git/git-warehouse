import mysql.connector
from mysql.connector import pooling
import yaml
from pathlib import Path


class MySQLConnector:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._init_pool()
        return cls._instance

    def _init_pool(self):
        config_path = Path(__file__).parent.parent.parent / 'config' / 'database' / 'mysql_config.yaml'
        with open(config_path) as f:
            config = yaml.safe_load(f)['mysql']

        self.pool = pooling.MySQLConnectionPool(
            pool_name="web_log_pool",
            pool_size=config['pool_size'],
            pool_reset_session=True,
            host=config['host'],
            port=config['port'],
            user=config['user'],
            password=config['password'],
            database=config['database'],
            charset=config['charset']
        )

    def get_connection(self):
        return self.pool.get_connection()

    def execute_query(self, query, params=None, fetch=False):
        conn = self.get_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            cursor.execute(query, params or ())
            if fetch:
                return cursor.fetchall()
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            cursor.close()
            conn.close()