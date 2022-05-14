from loguru import logger
from elasticapm.handlers.logging import Formatter
import os
from dataclasses import dataclass

def setup_logger(service_name, service_id, size=int(5e8)):
    from logging.handlers import RotatingFileHandler

    os.makedirs("logs", exist_ok=True)
    fh = RotatingFileHandler(f"logs/{service_name}-{service_id}.log", maxBytes=size)
    formatter = Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    fh.setFormatter(formatter)

    logger.add(fh, format="{message}")
