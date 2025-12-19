import json
import os.path

import settings
from core.logger_handler import get_logger

logger = get_logger()


def read_json(filepath: str) -> dict:
    with open(file=filepath, mode="r", encoding="UTF-8") as f:
        result = json.load(f)
    return result


def write_json(data: dict, filepath: str) -> None:
    with open(file=filepath, mode="w", encoding="UTF-8") as f:
        json.dump(data, f, indent=4, sort_keys=True, ensure_ascii=False)
    return None


def load_cookies(filename: str) -> dict:
    cookies_filepath = os.path.join(settings.COOKIES_DIR, filename)
    if os.path.isfile(cookies_filepath):
        result = read_json(cookies_filepath)
        logger.debug(f"Cookies loaded: {result}")
        return result
    logger.warning(f"Cookies file missing: {cookies_filepath}")
    return {}


def save_cookies(cookies: dict, filename: str) -> None:
    cookies_filepath = os.path.join(settings.COOKIES_DIR, filename)
    logger.debug(f"Cookies data to write: {cookies}")
    write_json(cookies, cookies_filepath)
    logger.info(f"Cookies written to file: {cookies_filepath}")
    return None
