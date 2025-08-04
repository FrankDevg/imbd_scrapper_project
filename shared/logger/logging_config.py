import logging
import os

def setup_logger(name: str) -> logging.Logger:
    """
    Configura un logger con salida tanto a consola como a archivo.

    Args:
        name (str): Nombre del logger.

    Returns:
        logging.Logger: Instancia configurada del logger.
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)  # Nivel mínimo de log: INFO

    # Evita agregar múltiples handlers si ya están configurados
    if not logger.handlers:
        # Formato común para los logs
        formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')

        # Handler de consola: imprime los logs en tiempo real
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        # Handler de archivo: guarda los logs en 'logs/scraper.log'
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)  # Crea carpeta si no existe
        file_handler = logging.FileHandler(f"{log_dir}/scraper.log", encoding='utf-8')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
