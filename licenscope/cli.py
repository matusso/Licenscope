from __future__ import annotations

import argparse
import sys

from licenscope.app import LicenseChecker
from licenscope.config.loader import load_config
from licenscope.core.errors import LicenscopeError
from licenscope.notifications import build_registry as build_notification_registry
from licenscope.parsers import build_registry as build_parser_registry
from licenscope.util.logging import get_logger, setup_logging


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Licenscope license monitor")
    parser.add_argument(
        "-c", "--config", default="licenscope.toml", help="Path to config"
    )
    parser.add_argument(
        "--log-level",
        default="INFO",
        help="Logging level (DEBUG, INFO, WARNING, ERROR)",
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable ANSI color in logs",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    setup_logging(args.log_level.upper(), use_color=not args.no_color)
    logger = get_logger("licenscope")
    try:
        config = load_config(args.config)
        checker = LicenseChecker(
            parser_registry=build_parser_registry(),
            notification_registry=build_notification_registry(),
        )
        checker.run(config)
    except LicenscopeError as exc:
        logger.error("Licenscope failed: {}", exc)
        sys.exit(1)
    except Exception:
        logger.exception("Unexpected error")
        sys.exit(1)


if __name__ == "__main__":
    main()
