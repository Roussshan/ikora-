"""
Logger Utility
"""
import logging
from datetime import datetime
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

class Logger:
    def __init__(self, name='ikora'):
        self.logger = logging.getLogger(name)
    
    def info(self, message):
        self.logger.info(message)
    
    def error(self, message, error=None):
        if error:
            self.logger.error(f'{message}: {error}')
        else:
            self.logger.error(message)
    
    def warning(self, message):
        self.logger.warning(message)
    
    def warn(self, message):
        self.warning(message)
    
    def debug(self, message):
        self.logger.debug(message)
    
    @staticmethod
    def get_timestamp():
        return datetime.utcnow().isoformat() + 'Z'

# Global logger instance
logger = Logger()
