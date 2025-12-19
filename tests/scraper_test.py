from core.scrapers.fly_sky_scraper import FlySkyScraper
from core.scrapers.shu_x_scraper import ShuXScraper
from core.scrapers.six_nine_scraper import SixNineScraper
from core.scrapers.tw_kan_scraper import TwKanScraper

sixnine = SixNineScraper()
flysky = FlySkyScraper()
twkan = TwKanScraper()
shux = ShuXScraper()


def search():
    keyword = "系統"
    r = sixnine.search(keyword)
    print(r)
    input()
    r = flysky.search(keyword)
    print(r)
    return None


def proxy():
    url_list = [
        "https://www.69shuba.com/book/85042.htm",
        "https://www.piaotia.com/html/3/3756/2554553.html",
    ]
    r = sixnine.proxy(url_list[0])
    print(r)
    input()
    r = flysky.proxy(url_list[1])
    print(r)
    return None


if __name__ == '__main__':
    # r = shux.search("系统")
    r = shux.proxy("https://69shux.co/book/59794.html")
    print(r)
    # search()
    # proxy()
