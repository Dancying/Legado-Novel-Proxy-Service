import time

from core.browser_handler import close_all_edge
from core.browser_handler import get_edge_cdp_version
from core.browser_handler import launch_edge_with_cdp
from core.file_handler import save_cookies
from core.playwright_handler import get_domain_cookies
from core.playwright_handler import open_verification_page
from core.playwright_handler import solve_cloudflare_turnstile


def browser_start_stop_test():
    launch_edge_with_cdp()
    time.sleep(3)
    close_all_edge()
    return None


def multiple_website_verification_test():
    validation_url_list = [
        # ("https://www.69shuba.com/modules/article/search.php", ".container>div:last-of-type>div:last-of-type"),
        ("https://twkan.com/", "#JnAv0"),
    ]
    for url, selector in validation_url_list:
        if not get_edge_cdp_version():
            launch_edge_with_cdp()
        open_verification_page(url)
        # with sync_playwright() as p:
        #     browser = p.chromium.connect_over_cdp(f"{settings.BROWSER_CDP_HOST}:{settings.BROWSER_CDP_PORT}")
        #     context = browser.contexts[0]
        #     page = context.pages[0]
        #     page.goto(url, wait_until="commit")
        #     page.reload(wait_until="commit")
        #     browser.close()
        solve_cloudflare_turnstile(url, selector)
        cookies = get_domain_cookies("twkan.com")
        save_cookies(cookies, "twkan.com")
    close_all_edge()
    return None


if __name__ == '__main__':
    # multiple_website_verification_test()
    launch_edge_with_cdp()

    # import requests
    #
    # header = {
    #     "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36 Edg/124.0.0.0"}
    # cookies = load_cookies("twkan.com")
    # r = requests.get("https://twkan.com/book/80643.html", headers=header, cookies=cookies)
    # print(r.text)
    #
    # # r = requests.get(f"{settings.BROWSER_CDP_HOST}:{settings.BROWSER_CDP_PORT}/json/version")
    # # print(r.text)

    print(get_edge_cdp_version())
