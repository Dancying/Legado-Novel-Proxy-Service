import requests

from core.scrapers.base_web_scraper import BaseWebScraper


class FlySkyScraper(BaseWebScraper):

    def __init__(self):
        super().__init__()
        self.domain = "piaotia.com"
        self._search_url = "https://www.piaotia.com/modules/article/search.php"

    def search(self, keyword: str) -> str:
        data = {"searchtype": "articlename", "searchkey": keyword.encode("gbk"), "Submit": "+%CB%D1+%CB%F7+"}
        response = requests.post(url=self._search_url, data=data, headers=self._headers)
        response.encoding = self._encoding
        return response.text

    def proxy(self, url: str) -> str:
        whitelist = ["https://www.piaotia.com"]
        return self._get_page_content(url, whitelist, self._encoding, self._headers)
