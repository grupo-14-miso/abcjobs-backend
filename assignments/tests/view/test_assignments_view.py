
def test_ping(client):
        response_valid = client.get("/assignments/ping")
        assert response_valid.json == "Pong"