# shared/config/config.py
import os
import os
from dotenv import load_dotenv

load_dotenv()
# --- Configuración base de IMDb ---
BASE_URL = "https://www.imdb.com"
CHART_TOP_PATH = "/chart/top/"
TITLE_DETAIL_PATH = "/title/{id}/"

# --- GraphQL IMDb ---
GRAPHQL_URL = "https://caching.graphql.imdb.com/"
GRAPHQL_HASH = "2db1d515844c69836ea8dc532d5bff27684fdce990c465ebf52d36d185a187b3"
GRAPHQL_OPERATION = "Top250MoviesPagination"
GRAPHQL_LOCALE = "en-US"
GRAPHQL_VERSION = 1
NUM_MOVIES = 250
TOR_WAIT_AFTER_ROTATION = 12  # segundos de espera tras rotar IP TOR

# --- User-Agent Rotation ---
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/88.0.4324.96 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 6.0; Nexus 5) AppleWebKit/537.36 Chrome/90.0.4430.91 Mobile Safari/537.36"
]

# --- Proxy Config ---
PROXY_HOST = os.getenv("PROXY_HOST")
PROXY_PORT = os.getenv("PROXY_PORT")
PROXY_USER = os.getenv("PROXY_USER")
PROXY_PASS = os.getenv("PROXY_PASS")

TOR_PROXY = {
    "http": "socks5h://tor:9050",
    "https": "socks5h://tor:9050"
}

PROXY_HOST = os.getenv("PROXY_HOST")
PROXY_PORT = os.getenv("PROXY_PORT")
PROXY_USER = os.getenv("PROXY_USER")
PROXY_PASS = os.getenv("PROXY_PASS")
PROXY_LIST = [ ]
USE_CUSTOM_PROXY = all([PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS])
USE_TOR =not USE_CUSTOM_PROXY
MAX_RETRIES = 3
RETRY_DELAYS = [1, 3, 5]
REQUEST_TIMEOUT = 10
MAX_THREADS = 50
BLOCK_CODES = [202,403, 404, 429]

# --- GraphQL Config ---
GRAPHQL_URL = "https://caching.graphql.imdb.com/"
GRAPHQL_HASH = "2db1d515844c69836ea8dc532d5bff27684fdce990c465ebf52d36d185a187b3"
# --- HTML Selectors ---
SELECTORS = {
    "title": '[data-testid="hero__primary-text"]',
    "year": 'ul.ipc-inline-list li a[href*="releaseinfo"]',
    "rating": '[data-testid="hero-rating-bar__aggregate-rating__score"] span',
    "duration_container": 'ul.ipc-inline-list--show-dividers',
    "metascore": "span.metacritic-score-box",
    "actors": "a[data-testid='title-cast-item__actor']"
}
 # PostgreSQL config
POSTGRES_DB = os.getenv("POSTGRES_DB", "imdb_scraper")
POSTGRES_USER = os.getenv("POSTGRES_USER", "aruiz")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "@ndresruiz@123")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "localhost")  # Cambia a "postgres" si usas docker-compose
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
