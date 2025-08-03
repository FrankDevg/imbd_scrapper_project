import os
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from infrastructure.scraper.imdb_scraper import ImdbScraper
from infrastructure.factory.use_case_factory import get_csv_use_case
from infrastructure.persistence.csv.repositories.init_csv_files import init_csv_files
def main():
    # Construimos el caso de uso con repositorios CSV
    use_case = get_csv_use_case()
    init_csv_files()
    # Creamos el scraper con el caso de uso inyectado
    scraper = ImdbScraper(use_case=use_case)
    scraper.scrape(save_use_case=use_case)

if __name__ == "__main__":
    main()
