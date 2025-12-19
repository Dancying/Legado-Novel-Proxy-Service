import time

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright

import settings
from core.logger_handler import get_logger

logger = get_logger()
endpoint_url = f"{settings.BROWSER_CDP_HOST}:{settings.BROWSER_CDP_PORT}"


def open_verification_page(validation_url: str) -> str:
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(endpoint_url)
        page = browser.contexts[0].new_page()
        page.goto(validation_url, wait_until="commit")
        page.reload(wait_until="commit")
        logger.info(f"URL opened in browser: {validation_url}")
        result = page.url
        browser.close()
    return result


def solve_cloudflare_turnstile(validation_url: str,
                               selector: str = ".main-content>div:first-of-type",
                               delay_seconds: int = 8) -> bool:
    logger.info(f"Starting Cloudflare Turnstile verification for {validation_url} after {delay_seconds}s")
    time.sleep(delay_seconds)
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(endpoint_url)
        context = browser.contexts[0]
        page = next((i for i in context.pages if i.url == validation_url), None)
        if page is None:
            logger.error(f"Browser page not found: {validation_url}")
            return False
        try:
            logger.debug(f"Locating element: {selector}...")
            cf_verify_box = page.locator(selector).bounding_box()
            x_coordinate = cf_verify_box["x"] + 75
            y_coordinate = cf_verify_box["y"] + (cf_verify_box["height"] / 2)
            page.mouse.click(x_coordinate, y_coordinate)
            logger.debug("Checking whether verification passed...")
            page.locator(selector).wait_for(state="hidden", timeout=delay_seconds * 1000)
        except PlaywrightTimeoutError:
            logger.warning(f"Timeout locating element {selector}. Validation failed.")
            return False
    logger.info("Cloudflare Turnstile verification successful.")
    return True


def get_domain_cookies(domain: str, clear_cookies: bool = False, delay_seconds: int = 3) -> dict:
    logger.info(f"Extract cookies for {domain} after {delay_seconds}s")
    time.sleep(delay_seconds)
    result = {}
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(endpoint_url)
        context = browser.contexts[0]
        context_cookies = context.cookies()
        logger.debug(f"Retrieved cookies from context: {context_cookies}")
        for cookie in context_cookies:
            if cookie.get("domain") and cookie["domain"].endswith(domain):
                result[cookie["name"]] = cookie["value"]
        logger.info(f"Cookies for {domain}: {result}")
        if clear_cookies:
            logger.info(f"Clearing cookies for {domain}")
            context.clear_cookies(domain=domain)
    return result
