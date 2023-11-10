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


def parse_searching_page(session: httpx.Client, arguments: schemas.InputData) -> httpx.Response:
    params = {
        'q': ' '.join(arguments.keywords),
        'type': arguments.type,
    }
    response = session.get('https://github.com/search',
                           params=params,
                           headers=REQUEST_HEADERS,
                           proxies={'all://': arguments.proxies[0]})
    return response


def check_extras(session, url: str) -> httpx.Response:
    response = session.get(url, headers=REQUEST_HEADERS)
    return response
