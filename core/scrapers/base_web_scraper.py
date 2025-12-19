import os.path
from abc import ABC, abstractmethod

import requests
from filelock import FileLock

import settings
from core.logger_handler import get_logger


class BaseWebScraper(ABC):

    def __init__(self):
        self._logger = get_logger()
        self._encoding = "GB18030"
        self._headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Content-Type": "application/x-www-form-urlencoded",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0",
        }
        self._browser_task_count_file_path = os.path.join(settings.TEMP_DIR, "browser_task_count")
        self._browser_task_count_lock = FileLock(f"{self._browser_task_count_file_path}.lock", timeout=10)

    @abstractmethod
    def search(self, keyword: str) -> str:
        pass

    @abstractmethod
    def proxy(self, url: str) -> str:
        pass

    def _get_page_content(self,
                          url: str,
                          whitelist: list[str] = None,
                          encoding: str = None,
                          headers: dict = None,
                          cookies: dict = None) -> str:
        whitelist = ["http"] if whitelist is None else whitelist
        encoding = self._encoding if encoding is None else encoding
        headers = self._headers if headers is None else headers
        for url_prefix in whitelist:
            if url.startswith(url_prefix):
                self._logger.debug(f"Making request to: {url}")
                response = requests.get(url=url, headers=headers, cookies=cookies)
                response.encoding = encoding
                self._logger.debug(f"Successfully received response from: {url}")
                return response.text
        self._logger.warning(f"Invalid URL: {url}")
        return "Invalid URL"

    def __get_browser_task_count(self) -> int:
        if os.path.isfile(self._browser_task_count_file_path):
            with open(file=self._browser_task_count_file_path, mode="r", encoding="UTF-8") as f:
                content = f.read().strip()
            task_count = int(content) if content.isdigit() else 0
            return task_count
        self._logger.warning(f"Browser task count file not found: {self._browser_task_count_file_path}")
        return 0

    def _increment_browser_task_count(self) -> int:
        with self._browser_task_count_lock:
            self._logger.debug("Increasing browser tasks...")
            new_count = self.__get_browser_task_count() + 1
            with open(file=self._browser_task_count_file_path, mode="w", encoding="UTF-8") as f:
                f.write(str(new_count))
            self._logger.debug(f"Current browser task count: {new_count}")
        return new_count

    def _decrement_browser_task_count(self) -> int:
        with self._browser_task_count_lock:
            self._logger.debug("Decreasing browser tasks...")
            new_count = max(0, self.__get_browser_task_count() - 1)
            with open(file=self._browser_task_count_file_path, mode="w", encoding="UTF-8") as f:
                f.write(str(new_count))
            self._logger.debug(f"Current browser task count: {new_count}")
        return new_count
