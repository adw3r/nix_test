import pytest
from src import schemas


def test_schema_validators_check_multiple_proxies():
    proxy = 'http://eu3030339:hKjxGgrgkt@194.61.9.17:7952'
    res = schemas.InputDataWithProxyCheck._InputDataWithProxyCheck__check_proxy(proxy)
    print(res)
    assert res == proxy


def test_failed_schema_validators_check_multiple_proxies():
    proxy = 'http://easdasdasd:1234'
    res = schemas.InputDataWithProxyCheck._InputDataWithProxyCheck__check_proxy(proxy)
    print(res)
    assert res is None


def test_schema_validators_check_proxy():
    proxies = [
        'http://eu3030339:hKjxGgrgkt@194.61.9.17:7952',
        'http://eu3030339:hKjxGgrgkt@46.8.202.81:7952',
    ]
    res: list[str] = schemas.InputDataWithProxyCheck._InputDataWithProxyCheck__check_multiple_proxies(proxies)
    print(res)
    assert res == proxies


def test_failed_schema_validators_check_proxy():
    proxies = [
        'http://eu30ssss30339:hKjxGgrgkt@194.61.9.17:7952',
        'http://eu3030sssss339:hKjxGgrgkt@46.8.202.81:7952',
    ]
    res: list[str] = schemas.InputDataWithProxyCheck._InputDataWithProxyCheck__check_multiple_proxies(proxies)
    print(res)
    assert res == []


def test_input_data_schema_proxies():
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
    input_data = schemas.InputDataWithProxyCheck(**input_data)
    assert input_data is not None


def test_input_data_schema_empty_proxies():
    input_data = {
        "keywords": [  # check is not implemented
            "openstack",
            "nova",
            "css"
        ],
        "proxies": [  # check implemented
        ],
        "type": "Repositories"  # checking implemented
    }
    with pytest.raises(ValueError):
        schemas.InputDataWithProxyCheck(**input_data)
