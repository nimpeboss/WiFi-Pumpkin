"""Logger module for WiFi-Pumpkin-NG"""

import logging
from pathlib import Path


class Logger:
    """Simple logger wrapper to support console and file logging.

    Args:
        name: Name of the logger instance used in log messages and file output.
    """

    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)

        # Create logs directory
        Path("logs").mkdir(exist_ok=True)

        # Console handler
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )
        self.logger.addHandler(console)

        # File handler
        file_handler = logging.FileHandler(f"logs/{name}.log")
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )
        self.logger.addHandler(file_handler)

    def info(self, msg: str) -> None:
        """Log an informational message.

        Args:
            msg: Message to log.
        """
        self.logger.info(msg)

    def error(self, msg: str) -> None:
        """Log an error message.

        Args:
            msg: Message to log.
        """
        self.logger.error(msg)

    def warning(self, msg: str) -> None:
        """Log a warning message.

        Args:
            msg: Message to log.
        """
        self.logger.warning(msg)

    def debug(self, msg: str) -> None:
        """Log a debug message.

        Args:
            msg: Message to log.
        """
        self.logger.debug(msg)
