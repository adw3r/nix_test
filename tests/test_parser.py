import httpx
import pytest

from src import schemas, parser


@pytest.fixture
def input_data(inp_data_as_dict):
    input_data = schemas.InputDataWithProxyCheck(**inp_data_as_dict)
    return input_data


@pytest.fixture
def inp_data_as_dict():
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


def test_extract_urls():
    html = '''
    <html>
        <div class="search-title">
            <a href=""></a>
        <div class="search-title">
            <a href=""></a>
        <div class="search-title">
            <a href=""></a>
    </html>
    '''
    urls = parser.extract_urls(html)
    assert urls == ['https://github.com', 'https://github.com', 'https://github.com']


def test_format_urls():
    urls = ['https://github.com']
    formatted_urls = parser.simple_format_urls(urls)
    assert formatted_urls == [{'url': 'https://github.com'}]


def test_get_extras(gh_client):
    urls = ['https://github.com/atuldjadhav/DropBox-Cloud-Storage',
            'https://github.com/michealbalogun/Horizon-dashboard']
    results: list[httpx.Response] = parser.get_extras(gh_client, urls)
    assert type(results[0]) is httpx.Response


def test_init_GithubParser():
    session = httpx.Client()
    gh_pars = parser.GitParser(session=session)
    assert gh_pars.session is session


def test_extract_owner():
    url = 'https://github.com/atuldjadhav/DropBox-Cloud-Storage'
    assert parser.extract_owner(url) == 'atuldjadhav'


def test_format_with_extras(gh_client):
    urls = ['https://github.com/atuldjadhav/DropBox-Cloud-Storage']
    results: list[httpx.Response] = parser.get_extras(gh_client, urls)
    formatted_results = parser.extras_format_urls(results)
    print(formatted_results)
    assert [
               {'url': 'https://github.com/atuldjadhav/DropBox-Cloud-Storage',
                'extra': {'owner': 'atuldjadhav', 'language_stats': {'CSS': 52.0, 'JavaScript': 47.2, 'HTML': 0.8}}},
           ] == formatted_results


def test_retrieve_info_with_wiki():
    input_data_with_wiki = {
        "keywords": [
            "openstack",
            "nova",
            "css"
        ],
        "proxies": [
            "eu3030339:hKjxGgrgkt@194.61.9.17:7952",
            "eu3030339:hKjxGgrgkt@46.8.202.81:7952"
        ],
        "type": "Wikis"
    }
    result = parser.retrieve_info(input_data_with_wiki)
    ref_result = [{'url': 'https://github.com/salesforce/WikiSQL'},
                  {'url': 'https://github.com/noobcfy/wikis'},
                  {'url': 'https://github.com/ethereum/wiki'},
                  {'url': 'https://github.com/JW0914/Wikis'},
                  {'url': 'https://github.com/BonzaiThePenguin/WikiSort'},
                  {'url': 'https://github.com/requarks/wiki'},
                  {'url': 'https://github.com/Shadowsocks-Wiki/shadowsocks'},
                  {'url': 'https://github.com/TheWizWikii/WIKISTORE'},
                  {'url': 'https://github.com/vimwiki/vimwiki'},
                  {'url': 'https://github.com/ArduPilot/ardupilot_wiki'}]

    assert result == ref_result


def test_retrieve_info_with_repo():
    input_data_repo = {
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
    results = parser.retrieve_info(input_data_repo)

    for result in results:
        assert result.get('url') is not None
        assert result.get('extra') is not None
        assert result['extra']['owner'] is not None
        assert result['extra']['language_stats'] is not None
        language_stats_ = result['extra']['language_stats']
        for stat in language_stats_:
            assert type(language_stats_[stat]) is float
