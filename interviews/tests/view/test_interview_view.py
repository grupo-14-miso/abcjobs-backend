
def test_ping(client):
        response_valid = client.get("/interview/ping")
        assert response_valid.json == "Pong"