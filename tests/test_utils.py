from src import utils


def test_get_data():
    reference = {
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

    file_path = 'input_file.json'
    res = utils.get_data(file_path)
    assert reference == res
