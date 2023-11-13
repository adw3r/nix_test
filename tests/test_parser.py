import httpx
import pytest

from src import schemas, parser


def test_parse_searching_page():
    input_data = {
        "keywords": [
            "openstack",
            "nova",
            "css"
        ],
        "proxies": [
            'eu3030339:hKjxGgrgkt@194.61.9.17:7952',
            'eu3030339:hKjxGgrgkt@46.8.202.81:7952',
        ],
        "type": "Repositories"
    }
    input_data = schemas.InputDataWithProxyCheck(**input_data)
    gh_client = parser.GitParser(httpx.Client(proxies=input_data.proxies[0]))

    query = ' '.join(input_data.keywords)
    request_type = input_data.type
    searching_page_response: httpx.Response = gh_client.get_searching_page(query, request_type)
    print(searching_page_response)
    assert searching_page_response is not None


def test_check_extras(input_data):
    gh_parser = parser.GitParser(httpx.Client(proxies=input_data.proxies[0]))

    url = 'https://github.com/atuldjadhav/DropBox-Cloud-Storage'
    response: httpx.Response = gh_parser.check_extras(url)
    assert response is not None
