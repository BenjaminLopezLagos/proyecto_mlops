from streaming_api import app

def test_get():
    client = app.test_client()
    response = client.get('/')
    assert response.status_code == 200