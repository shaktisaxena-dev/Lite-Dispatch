import structlog
import logging
import sys


def configure_logging():
    # 1. Configure standard python logging to use structlog
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO,
    )
    # 2. Configure structlog processors
    structlog.configure(
        processors=[
            structlog.stdlib.add_log_level,
            structlog.stdlib.add_logger_name,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer(),  # Renders everything as JSON!
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
    )


# Create a global logger
logger = structlog.get_logger()
