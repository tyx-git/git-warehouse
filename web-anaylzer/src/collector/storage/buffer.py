from collections import deque
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
import threading
import time


class LogBuffer:
    def __init__(self, max_size: int = 10000, flush_interval: int = 60):
        self.buffer = deque(maxlen=max_size)
        self.max_size = max_size
        self.flush_interval = flush_interval
        self.last_flush = datetime.now()
        self.lock = threading.Lock()
        self.running = True
        self.flush_thread = threading.Thread(target=self._flush_loop, daemon=True)
        self.flush_thread.start()

    def add(self, log_entry: Dict[str, Any]) -> None:
        """Add a log entry to the buffer"""
        with self.lock:
            self.buffer.append({
                'timestamp': datetime.now(),
                'data': log_entry
            })

    def get_recent(self, count: int = 100) -> List[Dict[str, Any]]:
        """Get recent log entries"""
        with self.lock:
            return list(self.buffer)[-count:]

    def get_by_time_range(
        self,
        start_time: datetime,
        end_time: datetime
    ) -> List[Dict[str, Any]]:
        """Get log entries within a time range"""
        with self.lock:
            return [
                entry for entry in self.buffer
                if start_time <= entry['timestamp'] <= end_time
            ]

    def get_stats(self) -> Dict[str, Any]:
        """Get buffer statistics"""
        with self.lock:
            return {
                'current_size': len(self.buffer),
                'max_size': self.max_size,
                'oldest_entry': self.buffer[0]['timestamp'] if self.buffer else None,
                'newest_entry': self.buffer[-1]['timestamp'] if self.buffer else None
            }

    def _flush_loop(self) -> None:
        """Background thread to periodically flush old entries"""
        while self.running:
            current_time = datetime.now()
            if (current_time - self.last_flush).total_seconds() >= self.flush_interval:
                self._flush_old_entries()
                self.last_flush = current_time
            time.sleep(1)

    def _flush_old_entries(self) -> None:
        """Remove entries older than flush_interval"""
        cutoff_time = datetime.now() - timedelta(seconds=self.flush_interval)
        with self.lock:
            while self.buffer and self.buffer[0]['timestamp'] < cutoff_time:
                self.buffer.popleft()

    def stop(self) -> None:
        """Stop the flush thread"""
        self.running = False
        self.flush_thread.join()
