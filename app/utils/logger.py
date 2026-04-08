import logging

def setup_logger():
    """
    Configure application-wide logging
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )

def get_logger(name: str):
    """
    Get a logger instance for a module
    """
    return logging.getLogger(name)