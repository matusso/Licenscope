from __future__ import annotations

import sys

from loguru import logger


def setup_logging(level: str, *, use_color: bool = True) -> None:
    logger.remove()
    logger.configure(extra={"component": "licenscope"})
    logger.add(
        sys.stderr,
        level=level,
        colorize=use_color,
        backtrace=False,
        diagnose=False,
    )


def get_logger(component: str):
    return logger.bind(component=component)
