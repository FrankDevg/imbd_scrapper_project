# app/run_scraper.py
import os
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))


from infrastructure.factory.factory import get_scraper
from infrastructure.persistence.csv_writer import init_csv_files 
from domain.scraper_interface import ScraperInterface


def main():
    print("Iniciando extracción desde IMDb...")

    # Inicializar archivos CSV vacíos con encabezados
    init_csv_files()

    # Obtener instancia del scraper según la fuente
    scraper: ScraperInterface = get_scraper("imdb")

    # Ejecutar scraper que guarda línea por línea
    scraper.scrape()

    print(f"\nResultados guardados en: data/output_movies.csv y output_actors.csv")


if __name__ == "__main__":
    main()
