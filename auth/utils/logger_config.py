from loguru import logger
import sys
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def configure_logger():
    logger.remove()

    log_dir = BASE_DIR / "logs"
    os.makedirs(log_dir, exist_ok=True)

    log_format = (
        "<cyan>{time:YYYY-MM-DD HH:mm:ss}</cyan> | "
        "<blue>{name}</blue> | "
        "<level>{level}</level> | "
        "<magenta>{message}</magenta>"
    )

    logger.add(sys.stderr, level="DEBUG", format=log_format)

    logger.add(
        f"{log_dir}/app.log",
        rotation="1 week",
        retention="1 month",
        level="INFO",
        format=log_format,
    )

    logger.add(
        f"{log_dir}/error.log",
        level="ERROR",
        filter=lambda record: record["level"].name == "ERROR",
        rotation="500 KB",
        retention="10 days",
        format=log_format,
    )

    logger.add(
        f"{log_dir}/debug.log",
        level="DEBUG",
        filter=lambda record: record["level"].name == "DEBUG",
        rotation="500 KB",
        retention="10 days",
        format=log_format,
    )

    return logger
