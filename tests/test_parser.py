import httpx
import pytest

from src import schemas, parser


@pytest.fixture
def input_data():
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
    return input_data


@pytest.fixture
def gh_client(input_data):
    gh_client = parser.GitParser(httpx.Client(proxies=input_data.proxies[0]))
    return gh_client


def test_parse_searching_page(gh_client, input_data):
    query = ' '.join(input_data.keywords)
    request_type = input_data.type
    searching_page_response: httpx.Response = gh_client.get_searching_page(query, request_type)
    assert searching_page_response is not None


def test_check_extras(gh_client, input_data):
    url = 'https://github.com/atuldjadhav/DropBox-Cloud-Storage'
    response: httpx.Response = gh_client.check_extras(url)
    assert response is not None
