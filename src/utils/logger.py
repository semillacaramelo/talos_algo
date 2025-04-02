import logging
import os

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

    # Add the file handler to the logger
    logger.addHandler(file_handler)

    # Create a stream handler for console output
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    # Add the stream handler to the logger
    logger.addHandler(stream_handler)

    return logger