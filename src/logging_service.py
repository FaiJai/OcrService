import logging

logger = logging.getLogger(__name__)

if __debug__:
    logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)
