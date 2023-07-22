import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


def info(message: str) -> None:
    logger.info(message)


def debug(message: str) -> None:
    logger.debug(message)


def warn(message: str) -> None:
    logger.warning(message)


def err(message: str) -> None:
    logger.error(message)
