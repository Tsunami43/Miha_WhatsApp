import logging


def target_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    error_handler = logging.FileHandler(f'logs/{name}_error.log')
    error_handler.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s \n')
    error_handler.setFormatter(formatter)

    logger.addHandler(error_handler)

    return logger


def main_logger():
    logging.basicConfig(
        level=logging.INFO,
        filename='logs/main.log',
        filemode="w",
        format="%(asctime)s - [%(levelname)s] -  %(name)s - " +
            "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s \n"
    )