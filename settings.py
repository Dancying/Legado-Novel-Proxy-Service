from pathlib import Path

# Basic path settings
PROJECT_ROOT = Path(__file__).resolve().parent
TEMP_DIR = PROJECT_ROOT / "temp"
CACHE_DIR = TEMP_DIR / "cache"
COOKIES_DIR = TEMP_DIR / "cookies"
LOGS_DIR = TEMP_DIR / "logs"
BROWSER_PROFILE_DIR = TEMP_DIR / "profile"

# Logs settings
LOGS_LEVEL = "DEBUG"
LOGS_FORMAT = "%(asctime)s | %(levelname)-8s | %(module)-20s:%(lineno)-3d - %(message)s"

# Browser cdp settings
BROWSER_CDP_HOST = "http://localhost"
BROWSER_CDP_PORT = 9222

# Proxy settings
BASE_URL = "https://api.dancying.cn"
API_PREFIX = "/legado"
