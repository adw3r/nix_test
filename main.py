from concurrent.futures import ThreadPoolExecutor
import bs4

import httpx

from src import parser, schemas


def extract_links(html: str) -> list[dict]:  # test
    soup = bs4.BeautifulSoup(html, 'lxml')
    rows = soup.find_all('div', {'class': 'search-title'})
    repo_hrefs = [
        {'url': 'https://github.com%s' % i.find('a')['href']} for i in rows
    ]
    return repo_hrefs


def main(input_data: dict):
    input_data = schemas.InputDataWithProxyCheck(**input_data)
    session = httpx.Client(proxies=input_data.proxies[0])
    response: httpx.Response = parser.parse_searching_page(session, input_data)

    repo_hrefs = extract_links(response.text)
    if input_data.type == 'repositories':
        with ThreadPoolExecutor() as pool:
            results = pool.map(parser.check_extras, [repo['url'] for repo in repo_hrefs])
            return results
    else:
        return repo_hrefs


if __name__ == '__main__':
    input_data = {
        "keywords": [  # check is not implemented
            "openstack",
            "nova",
            "css"
        ],
        "proxies": [  # check implemented
            'eu3030339:hKjxGgrgkt@194.61.9.17:7952',
            'eu3030339:hKjxGgrgkt@46.8.202.81:7952',
        ],
        "type": "Repositories"  # checking implemented
    }
    repo_hrefs = main(input_data)
    print(repo_hrefs)
