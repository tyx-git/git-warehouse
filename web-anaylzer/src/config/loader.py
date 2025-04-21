import yaml
from pathlib import Path


class ConfigLoader:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        config_path = Path(__file__).parent.parent / 'config' / 'app_config.yaml'
        with open(config_path) as f:
            self.app_config = yaml.safe_load(f)

        db_config_path = Path(__file__).parent.parent / 'config' / 'database' / 'mysql_config.yaml'
        with open(db_config_path) as f:
            self.db_config = yaml.safe_load(f)

    def get_app_config(self, key, default=None):
        return self.app_config.get(key, default)

    def get_db_config(self, key, default=None):
        return self.db_config['mysql'].get(key, default)