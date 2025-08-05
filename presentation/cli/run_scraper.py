
import os
import sys
from pathlib import Path
# Define la ruta raíz del proyecto (3 niveles arriba de este archivo)
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

# Agrega la raíz al sys.path si no está presente, para permitir imports absolutos desde cualquier carpeta
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
    
from infrastructure.factory.dependency_container import DependencyContainer
from shared.config import config 
import logging

logger = logging.getLogger(__name__)

def main():
    logger.info("Inicializando contenedor de dependencias...")
    container = DependencyContainer(config)
    
    try:
        logger.info("Construyendo scraper...")
        scraper = container.get_scraper()
        
        logger.info("Iniciando proceso de scraping...")
        scraper.scrape()
        logger.info("Proceso de scraping finalizado exitosamente.")

    except Exception as e:
        logger.critical(f"Ha ocurrido un error fatal en la aplicación: {e}", exc_info=True)
    finally:
        logger.info("Cerrando recursos...")
        container.close_db_connection()

if __name__ == "__main__":
    main()