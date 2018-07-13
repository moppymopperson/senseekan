import sys
import logging

def make_logger(name):
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    file_handler = logging.FileHandler(name + '.log')
    file_handler.setFormatter(formatter)

    io_handler = logging.StreamHandler(sys.stdout)
    io_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.addHandler(file_handler)
    logger.addHandler(io_handler)
    logger.setLevel(logging.DEBUG)
    return logger