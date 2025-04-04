
import logging
import os
from collections import deque
from datetime import datetime

# Global log queue with max size
log_queue = deque(maxlen=1000)

def setup_logger():
    # Define log file path
    log_dir = 'logs'
    log_file = os.path.join(log_dir, 'bot.log')

    # Ensure the logs directory exists
    os.makedirs(log_dir, exist_ok=True)

    # Get a logger instance
    logger = logging.getLogger("DerivBot")
    logger.setLevel(logging.INFO)

    # Check if the logger already has handlers to avoid duplicate handlers
    if logger.hasHandlers():
        return logger

    # Create a file handler
    file_handler = logging.FileHandler(log_file)

    # Create a formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Custom handler to add logs to our queue
    class QueueHandler(logging.Handler):
        def emit(self, record):
            log_entry = {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'level': record.levelname,
                'message': record.getMessage()
            }
            log_queue.append(log_entry)

    queue_handler = QueueHandler()
    queue_handler.setFormatter(formatter)

    # Add all handlers
    logger.addHandler(file_handler)
    logger.addHandler(queue_handler)

    # Create a stream handler for console output
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    return logger

def get_recent_logs(last_id=None):
    """Get recent logs after the specified ID"""
    if last_id is None:
        return list(log_queue)
    return list(log_queue)[last_id:]
