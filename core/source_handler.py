import json
import os.path
import threading

import requests

import settings
from core.file_handler import read_json
from core.file_handler import write_json
from core.logger_handler import get_logger

logger = get_logger()


def get_latest_source() -> str:
    source_info_url = "https://github.com/Dancying/Legado-Adaptation-Plan/tree-commit-info/main/src"
    source_info_data = requests.get(url=source_info_url, headers={"Accept": "application/json"}).json()
    logger.info("Successfully downloaded latest source information from GitHub.")
    source_cache_filepaths = _get_book_source_cache_paths(source_info_data)
    result = _read_book_source_jsons(source_cache_filepaths)
    result.sort(key=lambda item: item.get("customOrder", float("inf")))
    return json.dumps(result, indent=4, sort_keys=True, ensure_ascii=False)


def _read_book_source_jsons(json_filepaths: list) -> list[dict]:
    result = []
    for path in json_filepaths:
        logger.info(f"Reading book source file: {path}")
        result.append(read_json(path))
    return result


def _download_book_source_to_json(url: str, filepath: str) -> None:
    response = requests.get(url, headers={"Accept": "application/json, text/html"})
    logger.info(f"Book source download finished: {url}")
    parent_dir_path = os.path.dirname(filepath)
    if not os.path.isdir(parent_dir_path):
        os.mkdir(parent_dir_path)
    write_json(response.json(), filepath)
    logger.info(f"Book source saved to: {filepath}")
    return None


def _get_book_source_cache_paths(book_source_info: dict) -> list:
    thread_list = []
    source_filepaths = []
    for filename, value in book_source_info.items():
        if "_" in filename and filename.endswith(".json"):
            filepath = os.path.join(settings.CACHE_DIR, value["oid"], filename)
            source_filepaths.append(filepath)
            if not os.path.isfile(filepath):
                logger.warning(f"Book source file missing: {filepath}")
                source_url = f"https://github.com/Dancying/Legado-Adaptation-Plan/raw/refs/heads/main/src/{filename}"
                th = threading.Thread(target=_download_book_source_to_json, args=(source_url, filepath))
                th.start()
                thread_list.append(th)
    for th in thread_list:
        th.join()
    return source_filepaths
