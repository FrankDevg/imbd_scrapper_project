# shared/logger/logging_config.py

import logging
import os

def setup_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

        # Handler para consola
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # Handler para archivo
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)  # crea carpeta si no existe
        file_handler = logging.FileHandler(f"{log_dir}/scraper.log", encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
