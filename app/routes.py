from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import request

import settings
from core.logger_handler import get_logger
from core.scrapers.fly_sky_scraper import FlySkyScraper
from core.scrapers.shu_x_scraper import ShuXScraper
from core.scrapers.six_nine_scraper import SixNineScraper
from core.scrapers.tw_kan_scraper import TwKanScraper
from core.source_handler import get_latest_source

legado_api = Blueprint("legado_api", __name__, url_prefix=settings.API_PREFIX, template_folder="templates")

logger = get_logger()

SEARCH_ROUTE = "/search"
PROXY_ROUTE = "/proxy"

website_scraper_mapping = {
    "sixnine": SixNineScraper(),
    "flysky": FlySkyScraper(),
    "twkan": TwKanScraper(),
    "shux": ShuXScraper(),
}


@legado_api.route("/", methods=["GET"])
def legado_api_index():
    return redirect("https://git.dancying.cn/Dancying/NovelService/src/master/README.md", code=301)


@legado_api.route(SEARCH_ROUTE, methods=["POST"])
def legado_search():
    logger.info(f"Request from [{request.remote_addr}]: {request.form}")
    keyword = request.form.get("keyword")
    site = request.form.get("site")
    html_data = website_scraper_mapping.get(site).search(keyword)
    return html_data


@legado_api.route(PROXY_ROUTE, methods=["GET"])
def legado_proxy():
    logger.info(f"Request from [{request.remote_addr}]: {request.args}")
    url = request.args.get("url")
    site = request.args.get("site")
    html_data = website_scraper_mapping.get(site).proxy(url)
    return html_data


@legado_api.route("/BookSource.json", methods=["GET"])
def legado_book_source():
    logger.info(f"Access from [{request.remote_addr}]: Returning BookSource.json")
    target_url = f"{settings.BASE_URL}{settings.API_PREFIX}"
    result = get_latest_source()
    result = result.replace("https://api.dancying.cn/legado/search", f"{target_url}{SEARCH_ROUTE}")
    result = result.replace("https://api.dancying.cn/legado/proxy", f"{target_url}{PROXY_ROUTE}")
    return result


@legado_api.app_errorhandler(404)
def handle_404(e):
    logger.warning(f"404 Not Found within API: [{request.remote_addr}] {request.path}")
    site = request.form.get("site") or request.args.get("site")
    return render_template("404.html", url=request.url, site=site), 404
