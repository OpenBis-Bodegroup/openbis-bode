import logging
import sys
import time
from functools import wraps
from pathlib import Path

import yaml  # type: ignore
from pdf2image import convert_from_path

from bode_loader.path import CONFIG_PATH


def timeit(logger):
    def _timeit(func):
        @wraps(func)
        def timeit_wrapper(*args, **kwargs):
            start_time = time.perf_counter()
            result = func(*args, **kwargs)
            end_time = time.perf_counter()
            total_time = end_time - start_time
            logger.info(
                f"Function {func.__name__} {kwargs.keys()} Took {total_time:.4f} seconds = {total_time/60:.1f} mins"
            )
            return result

        return timeit_wrapper

    return _timeit


def get_bode_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """get logger

    Args:
        name (str): name of the logger
        level (int, optional): logging level. Defaults to logging.INFO.

    Returns:
        logging.Logger: logger
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    log_formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d:%(funcName)s] %(message)s"
    )
    for handler in logger.handlers:
        logger.removeHandler(handler)
    handler_out = logging.StreamHandler(sys.stdout)
    handler_out.setFormatter(log_formatter)
    logger.addHandler(handler_out)
    return logger


def pdf2img(pdf_path: Path, img_dir: Path):
    """convert pdf to image and save in img_dir

    Args:
        pdf_path (Path): path to the pdf file
        img_dir (Path): path to the directory to save the images
    """
    pages = convert_from_path(pdf_path, 500)
    for i, page in enumerate(pages):
        page.save(img_dir / f"{str(pdf_path.name).split('.')[0]}_{i}.png", "PNG")


def get_config(config_path: Path = CONFIG_PATH / "config.yaml"):
    """get config from yaml file

    Args:
        config_path (Path, optional): path to the config file. Defaults to CONFIG_PATH/"config.yaml".

    Returns:
        dict: config
    """
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    return config


CONFIG = get_config()
