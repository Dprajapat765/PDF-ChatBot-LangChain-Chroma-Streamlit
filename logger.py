import logging

def get_logger(name=__name__):
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
        level=logging.INFO  # Can change to DEBUG, ERROR, etc.
    )
    return logging.getLogger(name)