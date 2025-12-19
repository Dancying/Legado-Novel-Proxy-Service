from core.logger_handler import get_logger


def logger_message_test():
    logger = get_logger()
    logger.info("Info Message")
    logger.info("Info Message")
    logger.info("Info Message")
    logger.debug("Debug Message")
    logger.warning("Warning Message")
    logger.error("Error Message")
    logger.error("Error Message")
    logger.error("Error Message")


if __name__ == '__main__':
    logger_message_test()
