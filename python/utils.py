import sys
import logging

def make_logger(name):
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    io_handler = logging.StreamHandler(sys.stdout)
    io_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.addHandler(io_handler)
    logger.setLevel(logging.INFO)
    return logger