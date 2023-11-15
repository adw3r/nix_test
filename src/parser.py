import random
import typing
from concurrent.futures import ThreadPoolExecutor

import bs4
import httpx

from src import schemas

REQUEST_HEADERS = {
    'authority': 'github.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,'
              'image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9,ru;q=0.8,uk;q=0.7',
    'cache-control': 'max-age=0',
    'dnt': '1',
    'referer': 'https://github.com/',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
}


class GitParser:
    def __init__(self, session: httpx.Client):
        self.session = session

    def get_searching_page(self, query: str, searching_type: str) -> httpx.Response:
        params = {
            'q': query, 'type': searching_type
        }
        response = self.session.get('https://github.com/search', params=params, headers=REQUEST_HEADERS)
        return response

    def check_extras(self, url: str) -> httpx.Response:
        response = self.session.get(url, headers=REQUEST_HEADERS)
        return response


def extract_urls(html: str) -> list[str]:
    soup = bs4.BeautifulSoup(html, 'lxml')
    rows = soup.find_all('div', {'class': 'search-title'})
    return [f'https://github.com{i.find("a")["href"]}' for i in rows]


def simple_format_urls(urls: typing.Sequence) -> typing.Sequence[dict]:
    return [
        {'url': url} for url in urls
    ]


def get_extras(parser, urls) -> list[httpx.Response]:
    with ThreadPoolExecutor(max_workers=len(urls)) as pool:
        results = pool.map(parser.check_extras, urls)
    res = list(results)
    return res


def extract_owner(url):
    return url.removeprefix('https://github.com/').split('/')[0]


def extras_format_urls(results: list[httpx.Response]) -> list[dict]:
    data = []

    for response in results:
        language_stats = {}
        soup = bs4.BeautifulSoup(response.text, 'lxml')
        side_bar = soup.find('div', {'class': 'Layout-sidebar'})
        lis = side_bar.find_all('div')[0].find_all('li', {'class': 'd-inline'})
        spans_list = [li.find_all('span') for li in lis]
        for span_list in spans_list:
            language_stats[span_list[0].text] = float(span_list[1].text[:-1])

        repo_url = str(response.url)
        result = {
            'url': repo_url,
            "extra": {
                "owner": extract_owner(repo_url),
                "language_stats": language_stats
            }
        }

        data.append(result)

    return data


def retrieve_info(input_data: dict):
    input_data = schemas.InputDataWithProxyCheck(**input_data)
    parser = GitParser(httpx.Client(proxies=random.choice(input_data.proxies)))

    searching_page_response: httpx.Response = parser.get_searching_page(
        input_data.type, ' '.join(input_data.keywords)
    )
    urls = extract_urls(searching_page_response.text)
    if input_data.type == 'repositories':
        results: list[httpx.Response] = get_extras(parser, urls)
        if not results:
            raise Exception(results)
        return extras_format_urls(results=results)
    return simple_format_urls(urls)
