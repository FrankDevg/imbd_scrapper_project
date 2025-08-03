# shared/config/config.py

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
NUM_MOVIES = 150
# --- User-Agent Rotation ---
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/88.0.4324.96 Safari/537.36",
    "Mozilla/5.0 (Linux; Android 6.0; Nexus 5) AppleWebKit/537.36 Chrome/90.0.4430.91 Mobile Safari/537.36"
]

# --- Proxy Config ---
PROXY_LIST = [
    "http://123.45.67.89:8080",
    "http://98.76.54.32:3128"
]

TOR_PROXY = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050',
}

USE_TOR = True
MAX_RETRIES = 3
RETRY_DELAYS = [1, 3, 5]
REQUEST_TIMEOUT = 10

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