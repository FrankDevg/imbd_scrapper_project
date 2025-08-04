import os
import sys
from pathlib import Path

# Define la ruta raíz del proyecto (3 niveles arriba de este archivo)
ROOT_DIR = Path(__file__).resolve().parent.parent.parent

# Agrega la raíz al sys.path si no está presente, para permitir imports absolutos desde cualquier carpeta
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Diagnóstico opcional para verificar el entorno de ejecución
print(f"sys.path:\n{sys.path}")
print(f"ROOT_DIR:\n{ROOT_DIR}")

from infrastructure.scraper.imdb_scraper import ImdbScraper
from infrastructure.factory.use_case_factory import get_composite_use_case

def main():
    """
    Punto de entrada principal del scraper.

    Inicializa el caso de uso compuesto (CSV + PostgreSQL) y lanza el proceso de scraping
    utilizando la clase `ImdbScraper`.
    """
    use_case = get_composite_use_case()
    scraper = ImdbScraper(use_case=use_case)
    scraper.scrape(save_use_case=use_case)

if __name__ == "__main__":
    main()
