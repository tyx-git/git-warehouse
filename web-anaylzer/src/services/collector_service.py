import time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from src.collector.sources.file_source import FileSource
from src.collector.processors.apache_processor import ApacheLogProcessor
from src.storage.models.apache_log import ApacheLog


class LogCollectorService:
    def __init__(self):
        self.processor = ApacheLogProcessor()
        self.storage = ApacheLog()
        self.running = False
        self.thread = None
        self.processed_files = set()

    def start(self, watch_dir=None, interval=5):
        """Start the collector service"""
        if watch_dir:
            self._start_file_watcher(watch_dir)
        else:
            self._start_interval_check(interval)

    def _start_file_watcher(self, watch_dir):
        """Watch directory for new log files"""
        self.running = True

        class LogFileHandler(FileSystemEventHandler):
            def on_modified(self, event):
                if not event.is_directory and event.src_path.endswith('.log'):
                    self.process_log_file(event.src_path)

        self.observer = Observer()
        self.observer.schedule(LogFileHandler(), watch_dir, recursive=True)
        self.observer.start()

    def _start_interval_check(self, interval):
        """Check for new logs at regular intervals"""
        self.running = True
        self.thread = threading.Thread(target=self._run_interval_check, args=(interval,))
        self.thread.daemon = True
        self.thread.start()

    def _run_interval_check(self, interval):
        while self.running:
            # In a real implementation, this would check various sources
            time.sleep(interval)

    def stop(self):
        """Stop the collector service"""
        self.running = False
        if hasattr(self, 'observer'):
            self.observer.stop()
            self.observer.join()
        if self.thread:
            self.thread.join()

    def process_log_file(self, file_path):
        """Process a single log file"""
        if file_path in self.processed_files:
            return

        source = FileSource(file_path)
        for line in source.read_lines():
            try:
                if self.processor.validate_line(line):
                    parsed = self.processor.process_line(line)
                    if parsed:
                        self.storage.insert_log(parsed)
            except Exception as e:
                print(f"Error processing line: {e}")

        self.processed_files.add(file_path)