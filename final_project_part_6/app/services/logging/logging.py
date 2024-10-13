import logging

def get_logger(level = logging.DEBUG, logger_name = "default logger") -> logging.Logger:
    logging.basicConfig(level = level)

    handler = logging.FileHandler('myapp.log')
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger = logging.getLogger()
    logger.addHandler(handler)
    logger.setLevel(level)

    return logger
