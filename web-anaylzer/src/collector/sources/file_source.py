import gzip
import bz2
from pathlib import Path


class FileSource:
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self._validate_file()

    def _validate_file(self):
        if not self.file_path.exists():
            raise FileNotFoundError(f"Log file not found: {self.file_path}")
        if not self.file_path.is_file():
            raise ValueError(f"Path is not a file: {self.file_path}")

    def read_lines(self):
        openers = {
            '.gz': gzip.open,
            '.bz2': bz2.open,
            '': open
        }

        suffix = self.file_path.suffixes[-1] if self.file_path.suffixes else ''
        opener = openers.get(suffix, open)

        with opener(self.file_path, 'rt', encoding='utf-8') as f:
            for line in f:
                yield line.strip()