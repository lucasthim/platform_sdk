import json

import pytest
from platform_sdk.domain.reader import DomainReaderApi

@pytest.fixture
def schema_settings():
    return {
        'api_url': 'http://localhost:8089/reader/api/v1/',
    }


def test_map_entities(schema_settings):
    # arrange
    uri = schema_settings
    app_name = 'SAGER_Cenario'
    map_name = 'criteriopotencia'
    _params = None
    domain_reader_api = DomainReaderApi(uri)
    expected_response = _read_json('mock_criterio_potencia.json')

    # action
    actual_response = domain_reader_api.get_entities(app_name, map_name, _params)

    # assert
    assert expected_response == actual_response.content


def _read_json(file):
    from os import getcwd
    full_path = f'{getcwd()}/tests/{file}'

    with open(full_path) as json_file:
        data = json.load(json_file)
    return data
