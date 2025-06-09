import logging
import os
from datetime import datetime

def setup_logger(name: str) -> logging.Logger:
    # Create logs directory if it doesn't exist
    logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
    os.makedirs(logs_dir, exist_ok=True)

    # Get or create logger
    logger = logging.getLogger(name)
    
    # Only add handlers if logger doesn't have any
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)

        # Create handlers
        c_handler = logging.StreamHandler()
        current_date = datetime.now().strftime('%Y-%m-%d')
        f_handler = logging.FileHandler(
            os.path.join(logs_dir, f'ai_responses_{current_date}.log'),
            encoding='utf-8'
        )

        # Set levels
        c_handler.setLevel(logging.INFO)
        f_handler.setLevel(logging.DEBUG)

        # Create formatters
        c_format = logging.Formatter('%(levelname)s - %(message)s')
        f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # Add formatters to handlers
        c_handler.setFormatter(c_format)
        f_handler.setFormatter(f_format)

        # Add handlers to logger
        logger.addHandler(c_handler)
        logger.addHandler(f_handler)

    return logger