import logging
import os
import sys
sys.path.append(os.path.abspath('.'))

def config_logging():
    os.makedirs("logs", exist_ok=True)
    
    logger = logging.getLogger("my_logger")

    # Clear existing handlers to prevent duplicates
    if logger.hasHandlers():
        return logger

    # Basic configuration for the default log file
    logging.basicConfig(
            filename='logs/logs.txt',  # Log file name
            level=logging.INFO,  # Minimum logging level to capture
            format='[%(asctime)s - %(levelname)s] %(message)s'
    )
    
    logger.setLevel(logging.DEBUG)

    # Handlers
    debug_handler = logging.FileHandler("logs/debug.txt")
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(logging.Formatter('[%(asctime)s - %(levelname)s] %(message)s'))

    info_handler = logging.FileHandler("logs/info.txt")
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(logging.Formatter('[%(asctime)s - %(levelname)s] %(message)s'))

    # Stream handler to output logs to the terminal
    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.DEBUG)
    stream_handler.setFormatter(logging.Formatter('[%(asctime)s - %(levelname)s] %(message)s'))

    # Attach handlers to logger
    logger.addHandler(debug_handler)
    logger.addHandler(info_handler)
    logger.addHandler(stream_handler)

    return logger