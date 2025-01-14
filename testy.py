import pytest
from app import app, database, Numbers
import json


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:password@localhost:5432/test_db'

    with app.test_client() as client:
        with app.app_context():
            database.db.create_all()
            yield client
            database.db.session.remove()
            database.db.drop_all()


# POST /api/data tests
def test_add_data_success(client):
    """Test successful data addition"""
    response = client.post('/api/data', json={'number1': 1.5, 'number2': 2.7, 'category': 3})
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'id' in data


def test_add_data_missing_field(client):
    """Test missing field validation"""
    test_cases = [
        {'number2': 2.7, 'category': 3},  # missing number1
        {'number1': 1.5, 'category': 3},  # missing number2
        {'number1': 1.5, 'number2': 2.7}  # missing category
    ]

    for test_case in test_cases:
        response = client.post('/api/data', json=test_case)
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'Missing required field' in data['error']


def test_add_data_invalid_types(client):
    """Test invalid data type validation"""
    test_cases = [
        {'number1': 'abc', 'number2': 2.7, 'category': 3},  # invalid number1
        {'number1': 1.5, 'number2': 'def', 'category': 3},  # invalid number2
        {'number1': 1.5, 'number2': 2.7, 'category': 'ghi'},  # invalid category
        {'number1': None, 'number2': 2.7, 'category': 3},  # null number1
        {'number1': 1.5, 'number2': None, 'category': 3},  # null number2
        {'number1': 1.5, 'number2': 2.7, 'category': None}  # null category
    ]

    for test_case in test_cases:
        response = client.post('/api/data', json=test_case)
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'Invalid data type' in data['error']


def test_add_data_float_category(client):
    """Test category as float validation"""
    response = client.post('/api/data',
                           json={'number1': 1.5, 'number2': 2.7, 'category': 3.6})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'error' in data
    assert 'category must be an integer' in data['error']


# DELETE /api/data/<id> tests
def test_delete_data_success(client):
    """Test successful data deletion"""
    # First add a record
    response = client.post('/api/data',
                           json={'number1': 1.5, 'number2': 2.7, 'category': 3})
    data = json.loads(response.data)
    record_id = data['id']

    # Then delete it
    response = client.delete(f'/api/data/{record_id}')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['id'] == record_id


def test_delete_data_not_found(client):
    """Test deletion of non-existent record"""
    response = client.delete('/api/data/999')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data
    assert 'Record not found' in data['error']


def test_delete_data_invalid_id(client):
    """Test deletion with invalid ID format"""
    response = client.delete('/api/data/abc')
    assert response.status_code == 404


def test_malformed_json(client):
    """Test sending malformed JSON"""
    response = client.post('/api/data',
                           data='{"invalid json',
                           content_type='application/json')
    assert response.status_code == 400