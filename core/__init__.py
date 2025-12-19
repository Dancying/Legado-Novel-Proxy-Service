import settings

settings.TEMP_DIR.mkdir(parents=True, exist_ok=True)
settings.CACHE_DIR.mkdir(parents=True, exist_ok=True)
settings.COOKIES_DIR.mkdir(parents=True, exist_ok=True)
settings.LOGS_DIR.mkdir(parents=True, exist_ok=True)
settings.BROWSER_PROFILE_DIR.mkdir(parents=True, exist_ok=True)
