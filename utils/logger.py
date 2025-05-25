# logger.py
# Sets up logging for the Family Expense Tracker app

import logging

# Configure logging: INFO level, message format, and log file
logging.basicConfig(
    filename='tracker.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Create a logger instance that can be imported and used throughout the app
logger = logging.getLogger(__name__)