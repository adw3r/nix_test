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


def test_parse_searching_page(input_data):
    client = httpx.Client(proxies=input_data.proxies[0])
    response: httpx.Response = parser.parse_searching_page(client, input_data)
    assert response is not None


def test_check_extras(input_data):
    url = 'https://github.com/atuldjadhav/DropBox-Cloud-Storage'
    client = httpx.Client(proxies=input_data.proxies[0])

    response: httpx.Response = parser.check_extras(client, url)
    assert response is not None
