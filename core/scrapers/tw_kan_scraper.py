import os.path
import threading
import time

import requests
from filelock import FileLock
from filelock import Timeout as FileLockTimeoutError

import settings
from core.browser_handler import close_all_edge
from core.browser_handler import get_edge_cdp_version
from core.browser_handler import launch_edge_with_cdp
from core.file_handler import load_cookies
from core.file_handler import read_json
from core.file_handler import save_cookies
from core.file_handler import write_json
from core.playwright_handler import get_domain_cookies
from core.playwright_handler import open_verification_page
from core.playwright_handler import solve_cloudflare_turnstile
from core.scrapers.base_web_scraper import BaseWebScraper


class TwKanScraper(BaseWebScraper):

    def __init__(self):
        super().__init__()
        self._encoding = "UTF-8"
        self.domain = "twkan.com"
        self._search_url = "https://twkan.com/search"
        self._search_lock = FileLock(os.path.join(settings.TEMP_DIR, "twkan_search.lock"), timeout=10)
        self._proxy_lock = FileLock(os.path.join(settings.TEMP_DIR, "twkan_proxy.lock"), timeout=20)
        self._update_cookies_lock = FileLock(os.path.join(settings.TEMP_DIR, "twkan_update_cookies.lock"), timeout=0)
        self._browser_cdp_version_file_path = os.path.join(settings.TEMP_DIR, "twkan_browser_cdp_version")

    def search(self, keyword: str) -> str:
        try:
            with self._search_lock:
                cookies = load_cookies(self.domain)
                if cookies:
                    data = {"searchkey": keyword, "searchtype": "all"}
                    self.__set_headers()
                    response = requests.post(url=self._search_url, data=data, headers=self._headers, cookies=cookies)
                    response.encoding = self._encoding
                    response_text = response.text
                    failure_text = "Just a moment..."
                    if failure_text not in response_text:
                        return response_text
                    self._logger.warning("Twkan cookies expired")
                    save_cookies({}, self.domain)
                threading.Thread(target=self.update_cookies).start()
                return "Updating cookies (approx. 30s)"
        except FileLockTimeoutError:
            return "Server is busy. Please retry later."

    def proxy(self, url: str) -> str:
        try:
            with self._proxy_lock:
                cookies = load_cookies(self.domain)
                if cookies:
                    whitelist = ["https://twkan.com"]
                    self.__set_headers()
                    response = self._get_page_content(url, whitelist, self._encoding, self._headers, cookies)
                    failure_text = "Just a moment..."
                    if failure_text not in response:
                        return response
                    self._logger.warning("Twkan cookies expired")
                    save_cookies({}, self.domain)
                threading.Thread(target=self.update_cookies).start()
                return "Updating cookies (approx. 30s)"
        except FileLockTimeoutError:
            return "Server is busy. Please retry later."

    def update_cookies(self) -> None:
        try:
            with self._update_cookies_lock:
                self._logger.info("Twkan cookies update task starting")
                cookies = {}
                self._increment_browser_task_count()
                if not get_edge_cdp_version():
                    launch_edge_with_cdp()
                validation_url = open_verification_page(self._search_url)
                for i in range(0, 3):
                    is_verified = solve_cloudflare_turnstile(validation_url, "div.main-content>div:first-of-type")
                    if is_verified:
                        cookies = get_domain_cookies(self.domain, True)
                        break
                write_json(get_edge_cdp_version(), self._browser_cdp_version_file_path)
                self._logger.debug("Twkan CDP version info saved")
                save_cookies(cookies, self.domain)
                task_count = self._decrement_browser_task_count()
                if task_count == 0:
                    close_all_edge()
                time.sleep(3)
                self._logger.info("Twkan cookies update task finished")
        except FileLockTimeoutError:
            self._logger.warning("Twkan cookies update task is already running")
        except Exception as e:
            self._logger.error(f"An unexpected error occurred: {e}")
            self._decrement_browser_task_count()
        return None

    def __set_headers(self) -> dict:
        if os.path.isfile(self._browser_cdp_version_file_path):
            user_agent = read_json(self._browser_cdp_version_file_path)["User-Agent"]
            self._headers["User-Agent"] = user_agent
            self._logger.debug(f"Set User-Agent to: {user_agent}")
        return self._headers
