import os

from pony import orm
from platform_sdk.reader.domain_reader import *

db = orm.Database()

# todo: remove
sqlite_path = os.path.join(os.path.abspath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), os.pardir)), 'db.sqlite3')
if os.path.exists(sqlite_path):
    os.remove(sqlite_path)

db.bind(provider='sqlite', filename='..\\db.sqlite3', create_db=True)
with orm.db_session():
    db.execute(
        'create table tb_usina (id integer primary key autoincrement, nome_longo text, desc text);')
    db.execute(
        'insert into tb_usina (nome_longo, desc) values ("angra 1", "descricao 1");')
    db.execute(
        'insert into tb_usina (nome_longo, desc) values ("angra 2", "descricao 2");')


def test_init_domain_reader():
    # arrange
    domain_reader = DomainReader(db)

    # assert
    assert domain_reader.schema_api is not None


def test_get_model():
    # arrange
    domain_reader = DomainReader(db)
    api_response = {
        "model": {"name": "Usina", "table": "tb_usina"},
        "fields": [
            {"name": "nome_longo", "alias": "nome", "type": "str"},
            {"name": "desc", "alias": "descricao", "type": "str"}
        ],
        "filter": {"name": "byName", "expression": 'nome = :nome'}
    }

    # action
    model = domain_reader._get_model(
        api_response['model'], api_response['fields'])

    # assert
    assert model.name == "Usina"
    assert model.table == "tb_usina"
    assert model.fields[0].name == "nome"
    assert model.fields[0].field_type == str
    assert model.fields[0].column == "nome_longo"


def test_get_fields():
    # arrange
    fields_dict = [{'name': 'field_1', 'alias': 'alias_1'}]

    # action
    domain_reader = DomainReader(db)
    fields = domain_reader._get_fields(fields_dict)

    # assert
    assert len(fields) == 1


def test_get_response_data():
    # arrange
    domain_reader = DomainReader(db)
    api_response = {
        "model": {"name": "Usina", "table": "tb_usina"},
        "fields": [
            {"name": "nome_longo", "alias": "nome", "type": "str"},
            {"name": "desc", "alias": "descricao", "type": "str"}
        ],
        "filter": {"name": "byName", "expression": 'nome = :nome'}
    }

    # action
    class Usina:
        def __init__(self, nome, descricao):
            self.nome = nome
            self.descricao = descricao

    usina1 = Usina('angra 1', 'descricao 1')
    usina2 = Usina('angra 2', 'descricao 2')
    data = domain_reader._get_response_data(
        list([usina1, usina2]), api_response['fields'])

    # assert
    assert data[0]['nome'] == 'angra 1'
    assert data[0]['descricao'] == 'descricao 1'

    assert data[1]['nome'] == 'angra 2'
    assert data[1]['descricao'] == 'descricao 2'


def test_get_data_with_no_api_response():
    # arrange
    app = 'teif'
    solution = 'sager'
    _map = 'usinaDTO'
    domain_reader = DomainReader(db)

    # action
    data = domain_reader.get_data(solution, app, _map)

    # assert
    assert data == None
